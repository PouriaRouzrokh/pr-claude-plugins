#!/usr/bin/env node
/**
 * Generate images using the Gemini Nano Banana 2 API.
 *
 * Uses gemini-3.1-flash-image-preview (Nano Banana 2). All generation
 * parameters can be controlled via a JSON prompt with a "config" key,
 * or via CLI flags as fallbacks.
 *
 * JSON prompt format (config is extracted, rest sent to model):
 *   {
 *     "task": "generate_image",
 *     "subject": {"primary": "...", "details": "..."},
 *     "style": {...}, "composition": {...}, "technical": {...},
 *     "environment": {...}, "quality": {...},
 *     "config": {
 *       "output": "filename.png", "size": "4K",
 *       "aspect_ratio": "16:9", "search": true, "edit": "input.jpg"
 *     }
 *   }
 *
 * CLI flags (fallbacks if not in JSON config):
 *   --output, -o    Output filename (default: generated_image.png)
 *   --aspect, -a    Aspect ratio (1:1, 16:9, 9:16, etc.)
 *   --size, -s      Image size: 512, 1K, 2K, 4K
 *   --edit, -e      Path to input image for editing
 *   --search        Enable image search grounding
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

const MODEL = "gemini-3.1-flash-image-preview";

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

function parseArguments() {
  const options = {
    output: { type: "string", short: "o", default: "generated_image.png" },
    aspect: { type: "string", short: "a" },
    size: { type: "string", short: "s" },
    edit: { type: "string", short: "e" },
    search: { type: "boolean", default: false },
    help: { type: "boolean", short: "h" },
  };

  const { values, positionals } = parseArgs({
    options,
    allowPositionals: true,
  });

  if (values.help || positionals.length === 0) {
    console.log(`
Usage: node generate_image.mjs "prompt_or_json" [options]

Options (fallbacks if not in JSON config):
  -o, --output   Output filename (default: generated_image.png)
  -a, --aspect   Aspect ratio (1:1, 16:9, 9:16, etc.)
  -s, --size     Image size: 512, 1K, 2K, 4K
  -e, --edit     Path to input image for editing
  --search       Enable image search grounding
  -h, --help     Show this help message
`);
    process.exit(values.help ? 0 : 1);
  }

  return {
    prompt: positionals[0],
    output: values.output,
    aspect: values.aspect,
    size: values.size,
    edit: values.edit,
    search: values.search,
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

function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
  };
  return mimeTypes[ext] || "image/png";
}

function loadImage(filePath) {
  const data = fs.readFileSync(filePath);
  return {
    inlineData: {
      mimeType: getMimeType(filePath),
      data: data.toString("base64"),
    },
  };
}

function buildConfig(size, aspect, search) {
  const config = { responseModalities: ["TEXT", "IMAGE"] };
  const imageConfig = {};
  if (aspect) imageConfig.aspectRatio = aspect;
  if (size) imageConfig.imageSize = size;
  if (Object.keys(imageConfig).length > 0) config.imageConfig = imageConfig;
  if (search) config.tools = [{ imageSearch: {} }];
  return config;
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
  const size = jsonConfig.size || args.size;
  const aspect = jsonConfig.aspect_ratio || args.aspect;
  const search = jsonConfig.search ?? args.search;
  const edit = jsonConfig.edit || args.edit;

  const ai = new GoogleGenAI({ apiKey });

  const contents = [];
  if (edit) contents.push(loadImage(edit));
  contents.push({ text: promptStr });

  const config = buildConfig(size, aspect, search);

  console.log(`Generating with ${MODEL}...`);
  if (size) console.log(`  Size: ${size}`);
  if (aspect) console.log(`  Aspect ratio: ${aspect}`);
  if (search) console.log(`  Image search: enabled`);

  try {
    const response = await ai.models.generateContent({
      model: MODEL,
      contents,
      config,
    });

    let saved = false;
    for (const part of response.candidates[0].content.parts) {
      if (part.text) {
        console.log(part.text);
      } else if (part.inlineData) {
        const buffer = Buffer.from(part.inlineData.data, "base64");
        fs.writeFileSync(output, buffer);
        console.log(`Image saved: ${output}`);
        saved = true;
      }
    }

    if (!saved) {
      console.error("No image was generated. Check your prompt and try again.");
      process.exit(1);
    }
  } catch (error) {
    console.error("Error generating image:", error.message);
    process.exit(1);
  }
}

const args = parseArguments();
generate(args);
