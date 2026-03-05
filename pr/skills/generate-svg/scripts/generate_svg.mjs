#!/usr/bin/env node
/**
 * Generate SVG graphics using Gemini 3.1 Pro.
 *
 * Uses gemini-3.1-pro-preview to generate SVG code as text. All parameters
 * can be controlled via a JSON prompt with a "config" key, or via CLI flags.
 *
 * JSON prompt format (config is extracted, rest sent to model):
 *   {
 *     "description": "main description",
 *     "elements": ["geometric shapes", "gradients"],
 *     "colors": {"primary": "#1e40af", "accent": "#06b6d4"},
 *     "layout": {"negative_space": "center-left for text overlay"},
 *     "style": "glassmorphic | minimal | detailed | organic",
 *     "config": {
 *       "output": "hero.svg", "type": "hero",
 *       "width": 1200, "height": 600, "optimize": true
 *     }
 *   }
 *
 * CLI flags (fallbacks if not in JSON config):
 *   --output, -o    Output filename (default: generated.svg)
 *   --type, -t      SVG type: hero, icon, illustration, logo, component
 *   --width         SVG width in pixels
 *   --height        SVG height in pixels
 *   --optimize      Run svgo optimization on output
 *
 * Environment:
 *   GEMINI_API_KEY  Required. Loaded from env, .env, .claude/.env, or ~/.claude/.env.
 *
 * Dependencies:
 *   npm install @google/genai
 */

import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { parseArgs } from "node:util";
import { execSync } from "node:child_process";

function loadEnvFile(filepath) {
  try {
    const content = fs.readFileSync(filepath, "utf-8");
    for (const line of content.split("\n")) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith("#") && trimmed.includes("=")) {
        const idx = trimmed.indexOf("=");
        const key = trimmed.slice(0, idx).trim();
        const value = trimmed.slice(idx + 1).trim();
        if (!process.env[key]) process.env[key] = value;
      }
    }
  } catch {}
}

function loadApiKey() {
  if (process.env.GEMINI_API_KEY) return;
  loadEnvFile(path.join(process.cwd(), ".env"));
  if (process.env.GEMINI_API_KEY) return;
  loadEnvFile(path.join(process.cwd(), ".claude", ".env"));
  if (process.env.GEMINI_API_KEY) return;
  loadEnvFile(path.join(os.homedir(), ".claude", ".env"));
}

const TYPE_DEFAULTS = {
  hero: { width: 1200, height: 600 },
  icon: { width: 24, height: 24 },
  illustration: { width: 800, height: 600 },
  logo: { width: 200, height: 200 },
  component: { width: 400, height: 300 },
};

const SYSTEM_INSTRUCTION = `You are an expert SVG designer. Generate production-quality SVG code.

Rules:
- Always include xmlns="http://www.w3.org/2000/svg" on the root <svg> element
- Always include a viewBox attribute matching the width and height
- Include explicit width and height attributes
- Use meaningful IDs on elements that might be animated (prefix with svg-)
- Keep paths simple — minimize anchor points, merge overlapping paths
- Include aria-hidden="true" on the root element for decorative SVGs
- Use currentColor where appropriate to support theming
- Place reusable definitions (gradients, filters, patterns) in a <defs> block
- Output ONLY the SVG code — no markdown fences, no explanations, no prose
- The SVG must be valid and render correctly in all modern browsers

Animation capabilities (use when the prompt requests animation):
- Prefer CSS @keyframes animations inside a <style> block within the SVG
- Use meaningful animation names prefixed with svg- (e.g., svg-pulse, svg-float, svg-glow-cycle)
- Common animation patterns:
  * Pulse: scale or opacity oscillation (e.g., transform: scale(1) -> scale(1.1))
  * Float: translateY oscillation for hovering elements
  * Glow: opacity or filter cycling for light effects
  * Rotate: continuous rotation for spinners or orbital elements
  * Dash: stroke-dashoffset animation for drawing/flowing line effects
  * Fade-in: opacity 0 -> 1 with staggered delays for sequential reveals
- Use animation-delay to stagger animations across similar elements
- Keep animations smooth: prefer ease-in-out timing, 2-6 second durations
- Use infinite loops for ambient/decorative animations
- Add prefers-reduced-motion media query to disable animations for accessibility:
  @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; } }
- Avoid SMIL <animate> elements — CSS animations have better browser support`;

const TYPE_INSTRUCTIONS = {
  hero: `Design a hero section illustration:
- Use rich gradients (linear and radial) for depth
- Include geometric shapes for visual interest
- Create layered compositions with foreground/background separation
- Use negative space effectively
- Ensure the design works well as a background with text overlay
- Include subtle decorative elements (dots, lines, circles)`,
  icon: `Design a clean icon:
- Use consistent stroke width throughout
- Design on a 24x24 grid with 2px padding
- Keep the design simple and recognizable at small sizes
- Use rounded line caps and joins for a friendly feel
- Test visual clarity: would this read at 16px?`,
  illustration: `Create a detailed illustration:
- Use a coherent color palette (3-5 colors max)
- Include both geometric and organic shapes
- Create visual hierarchy with size and color contrast
- Add subtle details that reward closer inspection`,
  logo: `Design a logo mark:
- Keep it simple — should work at 16px and 1000px
- Use a maximum of 2-3 colors
- Ensure it works in monochrome (single color)
- Create a distinctive, memorable shape
- Avoid fine details that disappear at small sizes`,
  component: `Create a UI component:
- Use clean, modern design language
- Include appropriate padding and spacing
- Use CSS custom properties for colors where possible
- Design for light and dark theme compatibility
- Include meaningful class names for styling`,
};

function parseArguments() {
  const options = {
    output: { type: "string", short: "o", default: "generated.svg" },
    type: { type: "string", short: "t", default: "illustration" },
    width: { type: "string" },
    height: { type: "string" },
    optimize: { type: "boolean", default: false },
    help: { type: "boolean", short: "h" },
  };

  const { values, positionals } = parseArgs({
    options,
    allowPositionals: true,
  });

  if (values.help || positionals.length === 0) {
    console.log(`
Usage: node generate_svg.mjs "prompt_or_json" [options]

Options (fallbacks if not in JSON config):
  -o, --output    Output filename (default: generated.svg)
  -t, --type      SVG type: hero, icon, illustration, logo, component
  --width         SVG width in pixels
  --height        SVG height in pixels
  --optimize      Run svgo optimization on output
  -h, --help      Show this help message
`);
    process.exit(values.help ? 0 : 1);
  }

  const svgType = values.type;
  if (!["hero", "icon", "illustration", "logo", "component"].includes(svgType)) {
    console.error(
      `Error: Invalid type '${svgType}'. Choose hero, icon, illustration, logo, or component.`
    );
    process.exit(1);
  }

  return {
    prompt: positionals[0],
    output: values.output,
    type: svgType,
    width: values.width ? parseInt(values.width, 10) : null,
    height: values.height ? parseInt(values.height, 10) : null,
    optimize: values.optimize,
  };
}

function extractConfig(promptStr) {
  try {
    const data = JSON.parse(promptStr);
    if (data && typeof data === "object" && "config" in data) {
      const config = data.config;
      delete data.config;
      return { prompt: JSON.stringify(data), config };
    }
    return { prompt: promptStr, config: {} };
  } catch {
    return { prompt: promptStr, config: {} };
  }
}

function extractSvg(text) {
  text = text.replace(/```(?:svg|xml|html)?\s*\n?/g, "");
  text = text.replace(/\n?```\s*$/g, "").trim();
  const match = text.match(/<svg[\s\S]*?<\/svg>/i);
  return match ? match[0] : null;
}

function optimizeSvg(filepath) {
  try {
    execSync(`npx svgo "${filepath}" -o "${filepath}"`, {
      stdio: "pipe",
      timeout: 30000,
    });
    console.log("SVG optimized with svgo.");
  } catch (error) {
    if (error.killed) {
      console.warn("svgo optimization timed out.");
    } else {
      console.warn("svgo not found. Install with: npm install -g svgo");
    }
  }
}

async function generate(args) {
  loadApiKey();
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.error("Error: GEMINI_API_KEY environment variable not set.");
    process.exit(1);
  }

  const { prompt: promptStr, config: jsonConfig } = extractConfig(args.prompt);

  // JSON config overrides CLI flags
  const output = jsonConfig.output || args.output;
  const svgType = jsonConfig.type || args.type;
  const width = jsonConfig.width || args.width;
  const height = jsonConfig.height || args.height;
  const doOptimize = jsonConfig.optimize ?? args.optimize;

  const defaults = TYPE_DEFAULTS[svgType] || { width: 800, height: 600 };
  const finalWidth = width || defaults.width;
  const finalHeight = height || defaults.height;

  const ai = new GoogleGenAI({ apiKey });

  const typeInstruction = TYPE_INSTRUCTIONS[svgType] || "";
  const prompt = `${typeInstruction}

Dimensions: ${finalWidth}x${finalHeight}px (viewBox="0 0 ${finalWidth} ${finalHeight}")

Description: ${promptStr}`;

  console.log(`Generating ${svgType} SVG (${finalWidth}x${finalHeight})...`);

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3.1-pro-preview",
      contents: prompt,
      config: {
        responseModalities: ["TEXT"],
        systemInstruction: SYSTEM_INSTRUCTION,
      },
    });

    const text = response.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!text) {
      console.error("No response from model. Try a different prompt.");
      process.exit(1);
    }

    const svgContent = extractSvg(text);
    if (!svgContent) {
      console.error("Could not extract SVG from response. Raw output:");
      console.error(text.slice(0, 500));
      process.exit(1);
    }

    fs.writeFileSync(output, svgContent);
    console.log(`SVG saved: ${output}`);

    if (doOptimize) {
      optimizeSvg(output);
    }
  } catch (error) {
    console.error("Error generating SVG:", error.message);
    process.exit(1);
  }
}

const args = parseArguments();
generate(args);
