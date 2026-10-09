"""Shared test configuration for the plugin's Gemini scripts.

Run from the repository root:
    uv run --with pytest --with "google-genai>=2.3,<3" --with resvg-py pytest tests -q
The tests replace the Gemini client with fakes; no API key or network access is needed.
"""

import pathlib
import sys

SKILLS = pathlib.Path(__file__).resolve().parent.parent / "pr" / "skills"
sys.dont_write_bytecode = True
