"""Small CLI wrapper for the OpenAI Responses API.

Improvements included:
- Optional .env loading (project root by default or `--env-file`).
- CLI flags for prompt, model, and optional pause.
- Defensive response parsing and error handling.
"""

from __future__ import annotations

import argparse
import os
import logging
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


def parse_response(resp: Any) -> str:
    """Try several common shapes returned by different SDKs and return a text string.

    The Responses API can be returned in slightly different structures depending on
    SDK versions. This helper attempts to extract usable text safely.
    """
    try:
        # Common convenience property in some SDK versions
        if hasattr(resp, "output_text") and resp.output_text:
            return str(resp.output_text)

        # Some SDKs provide `output` as a list of blocks/dicts
        out = getattr(resp, "output", None)
        if out:
            parts: list[str] = []
            # If it's not iterable, fall back to string
            try:
                iterator = iter(out)
            except TypeError:
                return str(out)

            for block in iterator:
                # block may be dict-like or an SDK object
                if isinstance(block, dict):
                    # Common nested shape: {'content': [{'text': '...'}]}
                    content = block.get("content") or []
                    if isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict):
                                text = c.get("text") or c.get("plain_text") or c.get("content")
                                if text:
                                    parts.append(str(text))
                            elif isinstance(c, str):
                                parts.append(c)
                    # Fallback to 'text' at block level
                    text = block.get("text")
                    if text:
                        parts.append(str(text))
                else:
                    # Try attributes on SDK objects
                    text = getattr(block, "text", None) or getattr(block, "content", None)
                    if isinstance(text, str):
                        parts.append(text)

            if parts:
                return "\n".join(parts)

        # Try dict-like conversion
        try:
            as_dict = getattr(resp, "to_dict", None)
            if callable(as_dict):
                return str(as_dict())
        except Exception:
            pass

        # Final fallback
        return str(resp)
    except Exception as e:
        logging.debug("parse_response failed: %s", e, exc_info=True)
        return repr(resp)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simple CLI to call the OpenAI Responses API")
    parser.add_argument("--env-file", help="Path to .env file to load (optional)")
    parser.add_argument("--prompt", help="Prompt to send to the model (if omitted, prompts interactively)")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4.1-nano"), help="Model to use")
    parser.add_argument("--pause", action="store_true", help="Pause at the end waiting for Enter")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s: %(message)s")

    # Load .env file if provided or try project root .env
    if args.env_file:
        load_dotenv(dotenv_path=args.env_file)
    else:
        load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY not found. Set it in the environment or provide --env-file pointing to a .env")
        return 2

    client = OpenAI(api_key=api_key)

    try:
        if args.prompt:
            prompt = args.prompt
        else:
            # Interactive prompt
            prompt = input("Greetings! How May I Help You Today? ")
    except (KeyboardInterrupt, EOFError):
        logging.info("Prompt cancelled by user")
        return 0

    if not prompt or not prompt.strip():
        logging.warning("Empty prompt provided; nothing to send")
        return 0

    try:
        response = client.responses.create(model=args.model, input=prompt)
    except Exception as e:
        logging.exception("API request failed")
        print("Request failed:", e)
        return 1

    output_text = parse_response(response)
    print("\nResponse:\n")
    print(output_text)

    if args.pause:
        try:
            input("\nPress Enter to exit...")
        except (KeyboardInterrupt, EOFError):
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())