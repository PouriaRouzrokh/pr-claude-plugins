---
name: generate-video
description: Generates, edits, and extends short videos (3-10 s clips with audio) with Google's Gemini Omni Flash model through the Gemini API - text-to-video, image-to-video (first frame, first and last frame, reference images), editing an uploaded or previously generated clip, and extending clips up to 40 s. Use when the user asks for a video, clip, animation, b-roll, product demo loop, social reel, or wants to animate an image or edit a video. Requires a paid-tier GEMINI_API_KEY.
argument-hint: "[description of the video to generate or edit]"
allowed-tools: Bash(uv run ${CLAUDE_SKILL_DIR}/scripts/generate_video.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/generate_video.py *)
---

# Generate Video (Gemini Omni Flash)

Generate and edit video by running the bundled script, which calls `gemini-omni-1.1-flash` through the Interactions API. Veo 3.1 previews shut down on 2026-10-22; Omni Flash is Google's current video model.

**Cost**: about $0.10 per second of 720p output (paid tier only; ai.google.dev pricing, checked 2026-10-30). The script prints an estimate from the saved clip's length after each run. Confirm with the user before generating long, high-resolution, or many clips.

## Run the Script

Generation takes one to several minutes. Run it with the Bash tool's `run_in_background` option (or a 600000 ms timeout) and wait for completion rather than polling.

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/generate_video.py - -o media/hero-loop.mp4 -a 16:9 <<'PROMPT'
Slow dolly-in across a sunlit ceramics studio at golden hour. Dust motes drift through a
shaft of window light; a potter's hands shape a spinning bowl in the foreground, softly in
focus. Warm, filmic color grade, shallow depth of field. Ambient sound of the wheel humming.
PROMPT
```

The script retries only HTTP 429 and 503 (twice, after 15 s and 45 s). Other server errors are not retried, because a 500, 502 or 504 can arrive after the clip was already rendered and billed; check the output folder and your usage before running again.

`uv run` installs dependencies automatically. Without uv, use `python3` (3.10+) after `python3 -m pip install -U "google-genai>=2.3,<3"`.

| Flag | Values | Notes |
|------|--------|-------|
| `-o` | path ending `.mp4` | Default `generated_video.mp4`. Never overwrites. |
| `-a` | `16:9` (default), `9:16` | Use 9:16 for Reels, Shorts, and Stories. |
| `-r` | `360p`, `720p` (default), `1080p`, `4k` | 1080p and 4k are upscaled and delivered by URI (handled automatically). |
| `-i` | image path, repeatable | One image: first frame or style/subject reference. Two images: first and last frame. |
| `-v` | video path (10 s max) | Edit or extend an existing clip (uploaded via the Files API). |
| `--task` | `text_to_video`, `image_to_video`, `reference_to_video`, `edit`, `extend` | Optional; the model infers it from the inputs. Set it when intent is ambiguous. |
| `--continue` | interaction ID | Edit or extend the previously generated clip without re-uploading it. |
| `--timeout` | seconds | Default 900. |

## Modes

| Goal | How |
|------|-----|
| Text to video | Prompt only. |
| Animate an image | `-i still.png` + describe the motion. Make the still with `generate-image` first for full art direction. |
| Interpolate | `-i first.png -i last.png` + describe the transition. |
| Seamless loop | Use the same image as first and last frame. |
| Subject consistency | `-i character.png -i product.png` and refer to them in order (`<IMAGE_REF_0>`, `<IMAGE_REF_1>`). |
| Edit generated clip | `--continue <id>` + the change only ("make the violin invisible"). |
| Edit your own clip | `-v clip.mp4` + the change. Not available in the EEA, UK, or Switzerland. |
| Extend | `--continue <id>` or `-v clip.mp4` with "Continue the scene: ...". Adds 3-10 s per turn, 40 s total. |

## Prompting

Write a short shot description, not a story. Cover:

- **Shot and camera**: wide, close-up, macro; dolly-in, tracking, crane, handheld, locked-off.
- **Subject and action**: one clear action per clip; describe motion speed ("slowly", "in one fluid motion").
- **Setting, lighting, and time of day.**
- **Style and grade**: cinematic, documentary, 16mm film, stop-motion, claymation, anime.
- **Audio**: Omni generates sound; describe ambience, effects, or dialogue in quotes. Say "no music" if needed.
- **Negatives as instructions**: "Do not show any text on screen" (there is no negative-prompt field).

Keep each clip to one shot. Build sequences by generating several clips and joining them with ffmpeg.

## Workflow

1. Confirm the purpose, aspect ratio, and length/budget with the user.
2. For art-directed results, make the keyframe with `generate-image`, review it, then animate it with `-i`.
3. Generate (in the background). Note the printed Interaction ID.
4. Review: extract a few frames with `ffmpeg -i clip.mp4 -vf fps=1 frame_%02d.png` and open them with the Read tool; report what you observed rather than assuming the clip matches the prompt.
5. Refine with `--continue <id>`, or extend the clip.
6. Post-process with ffmpeg when needed: trim (`-ss/-t`), mute (`-an`), web-optimize (`-movflags +faststart`), poster frame, GIF preview.

## Limits

- Input videos for editing or extension: 10 s max when uploaded. Video references: up to 3 clips of 3 s.
- Uploading or editing media with certain recognizable people is blocked; safety filters apply to prompts and output and vary by region.
- No YouTube URLs as inputs.
- With `delivery: uri` (1080p and 4k), the download link is only valid in the response to the create call; fetching the interaction later returns inline base64 instead. The script saves the clip right away, so this only matters if you call the API yourself.
- All output carries a SynthID watermark.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| HTTP 403 | Paid-tier key required, or the edit/extend feature is unavailable in your region. |
| Timed out | Increase `--timeout`, lower the resolution, or retry later. |
| `No video was returned` | Usually a safety block; rephrase. |
| HTTP 404 on the model | The model was retired; check https://ai.google.dev/gemini-api/docs/models and update `MODELS` in the script. |

## Related Skills

- **`generate-image`**: keyframes, first/last frames, and reference images.
- **`frontend-design`**: embedding video in pages (poster frames, `autoplay muted loop playsinline`, reduced-motion fallbacks).
