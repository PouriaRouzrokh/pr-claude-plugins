#!/usr/bin/env node
/**
 * Generate images using the Gemini Nano Banana API.
 *
 * Usage:
 *   node generate_image.mjs "prompt" [options]
 *
 * Options:
 *   --output, -o    Output filename (default: generated_image.png)
 *   --model, -m     Model: flash (default) or pro
 *   --aspect, -a    Aspect ratio (1:1, 16:9, 9:16, etc.)
 *   --size, -s      Image size for pro model: 1K, 2K, 4K
 *   --edit, -e      Path to input image for editing
 *   --search        Enable Google Search grounding (pro model only)
 *
 * Examples:
 *   node generate_image.mjs "A cat wearing a hat"
 *   node generate_image.mjs "A blog header" -a 16:9 -o header.png
 *   node generate_image.mjs "Add sunglasses" -e photo.jpg -o edited.png
 *   node generate_image.mjs "Current weather in NYC" -m pro --search
 *
 * Environment:
 *   GEMINI_API_KEY  Required. Your Gemini API key.
 *
 * Dependencies:
 *   npm install @google/genai
 */

import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";
import * as path from "node:path";
import { parseArgs } from "node:util";

function parseArguments() {
  const options = {
    output: { type: "string", short: "o", default: "generated_image.png" },
    model: { type: "string", short: "m", default: "flash" },
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
Usage: node generate_image.mjs "prompt" [options]

Options:
  -o, --output   Output filename (default: generated_image.png)
  -m, --model    Model: flash (default) or pro
  -a, --aspect   Aspect ratio (1:1, 16:9, 9:16, etc.)
  -s, --size     Image size for pro model: 1K, 2K, 4K
  -e, --edit     Path to input image for editing
  --search       Enable Google Search grounding (pro model only)
  -h, --help     Show this help message

Examples:
  node generate_image.mjs "A cat wearing a hat"
  node generate_image.mjs "A blog header" -a 16:9 -o header.png
  node generate_image.mjs "Add sunglasses" -e photo.jpg -o edited.png
`);
    process.exit(values.help ? 0 : 1);
  }

  return {
    prompt: positionals[0],
    output: values.output,
    model: values.model,
    aspect: values.aspect,
    size: values.size,
    edit: values.edit,
    search: values.search,
  };
}

function getModelName(modelChoice) {
  return modelChoice === "pro"
    ? "gemini-3-pro-image-preview"
    : "gemini-2.5-flash-image";
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

function buildConfig(args) {
  const config = {
    responseModalities: ["TEXT", "IMAGE"],
  };

  const imageConfig = {};
  if (args.aspect) {
    imageConfig.aspectRatio = args.aspect;
  }
  if (args.size && args.model === "pro") {
    imageConfig.imageSize = args.size;
  }

  if (Object.keys(imageConfig).length > 0) {
    config.imageConfig = imageConfig;
  }

  if (args.search && args.model === "pro") {
    config.tools = [{ googleSearch: {} }];
  }

  return config;
}

async function generate(args) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.error("Error: GEMINI_API_KEY environment variable not set.");
    process.exit(1);
  }

  const ai = new GoogleGenAI({ apiKey });
  const modelName = getModelName(args.model);

  const contents = [];
  if (args.edit) {
    contents.push(loadImage(args.edit));
  }
  contents.push({ text: args.prompt });

  const config = buildConfig(args);

  console.log(`Generating with ${modelName}...`);

  try {
    const response = await ai.models.generateContent({
      model: modelName,
      contents: contents,
      config: config,
    });

    let saved = false;
    for (const part of response.candidates[0].content.parts) {
      if (part.text) {
        console.log(part.text);
      } else if (part.inlineData) {
        const buffer = Buffer.from(part.inlineData.data, "base64");
        fs.writeFileSync(args.output, buffer);
        console.log(`Image saved: ${args.output}`);
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
