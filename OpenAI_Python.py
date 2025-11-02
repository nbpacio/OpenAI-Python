# -*- coding: utf-8 -*-
"""Small CLI wrapper around the OpenAI Responses API.

Behavior:
- Loads API key from `API_KEY.env` next to the repository root (or uses environment vars).
- Prompts: "What can I help you today?"
- After printing a response, asks: "Is there anything else I can help you with? (type 'exit' to quit)"
"""
import os
import argparse
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Try to locate API_KEY.env in the repository root (one level above this script) or fall back to default env loading
_here = os.path.dirname(os.path.abspath(__file__))
_candidate = os.path.join(os.path.dirname(_here), "API_KEY.env")
if os.path.exists(_candidate):
    load_dotenv(dotenv_path=_candidate)
else:
    # allow environment or other locations
    load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Put it in API_KEY.env or set the OPENAI_API_KEY environment variable.")

# Initialize client
client = OpenAI(api_key=api_key)
logging.basicConfig(level=logging.WARNING)


def parse_response(resp):
    """Return a readable string from a Responses API response object.

    Handles several possible shapes returned by the Responses API (convenience
    `output_text`, or structured `output` lists containing dicts/objects).
    Falls back to str(resp) when no text can be extracted.
    """
    # simple convenience property
    out_text = getattr(resp, "output_text", None)
    if out_text:
        return out_text

    parts = []

    # structured `output` (list) handling
    outputs = getattr(resp, "output", None)
    if outputs:
        for item in outputs:
            # dict-style items
            if isinstance(item, dict):
                # item may contain 'content' which is a list of pieces
                if "content" in item and isinstance(item["content"], list):
                    for piece in item["content"]:
                        if isinstance(piece, dict) and "text" in piece:
                            parts.append(str(piece["text"]))
                        else:
                            parts.append(str(getattr(piece, "text", piece)))
                elif "text" in item:
                    parts.append(str(item["text"]))
                else:
                    parts.append(str(item))
            else:
                # object-style: prefer .text attribute
                txt = getattr(item, "text", None)
                if txt:
                    parts.append(str(txt))
                else:
                    # fallback to to_dict if available, else str()
                    to_dict = getattr(item, "to_dict", None)
                    if callable(to_dict):
                        parts.append(str(to_dict()))
                    else:
                        parts.append(str(item))

    if parts:
        # combine and return found pieces
        return "\n".join(p for p in parts if p is not None)

    # fallback: if object provides to_dict(), use that
    to_dict = getattr(resp, "to_dict", None)
    if callable(to_dict):
        return str(to_dict())

    # final fallback
    return str(resp)


def send_prompt(prompt: str, model: str):
    try:
        resp = client.responses.create(model=model, input=prompt)
        return parse_response(resp)
    except Exception:
        logging.exception("API request failed")
        return None


def main():
    parser = argparse.ArgumentParser(description="Simple OpenAI Responses CLI")
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--prompt", help="Single-shot prompt (non-interactive)")
    args = parser.parse_args()

    # Single-shot
    if args.prompt:
        out = send_prompt(args.prompt, args.model)
        if out:
            print("\nResponse:\n")
            print(out)
        return 0

    # Interactive loop
    try:
        while True:
            try:
                prompt = input("What can I help you today? ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break

            if not prompt:
                continue
            if prompt.lower() == "exit":
                break

            out = send_prompt(prompt, args.model)
            if out:
                print("\nResponse:\n")
                print(out)

            try:
                follow = input("\nIs there anything else I can help you with? (type 'exit' to quit): ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break

            if not follow or follow.lower() == "exit":
                break
            # treat follow-up as next prompt
            prompt = follow

    except Exception:
        logging.exception("Unexpected error")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

