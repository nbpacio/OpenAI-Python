# ...existing code...
# -*- coding: utf-8 -*-
import os
import logging
import argparse
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a .env file (keeps API key out of source)
# Adjust path if your env file lives elsewhere; dotenv will also read OS env vars
load_dotenv(dotenv_path=r"C:\Users\Brian Pacio\source\repos\API_KEY.env")

# Get the API key from the environment (do not print or log this)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your API_KEY.env file path and contents.")

# Initialize client (do not expose the key)
client = OpenAI(api_key=api_key)

logging.basicConfig(level=logging.INFO)


def parse_response(response) -> str:
    """Extract a readable string from a Responses API response object."""
    # Prefer the convenience property if available
    text = getattr(response, "output_text", None)
    if text:
        return text
    # Fallback: try to assemble from structured output
    parts = []
    try:
        for item in getattr(response, "output", []) or []:
            # each item may have .content which is a list of dicts
            for c in item.get("content", []) if isinstance(item, dict) else getattr(item, "content", []):
                if isinstance(c, dict):
                    if "text" in c:
                        parts.append(c["text"])
                else:
                    # if content entries are objects with 'text' attribute
                    parts.append(getattr(c, "text", str(c)))
    except Exception:
        # Best-effort fallback
        parts.append(str(response))
    return "\n".join(p for p in parts if p)


def send_prompt(prompt: str, model: str):
    try:
        response = client.responses.create(model=model, input=prompt)
    except Exception as e:
        logging.exception("API request failed")
        print("Request failed:", e)
        return None
    return parse_response(response)


def main():
    parser = argparse.ArgumentParser(description="Simple OpenAI Responses CLI")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model name to use")
    parser.add_argument("--prompt", help="Single-shot prompt (non-interactive)")
    args = parser.parse_args()

    # Single-shot mode if prompt provided
    if args.prompt:
        output = send_prompt(args.prompt, args.model)
        if output:
            print("\nResponse:\n")
            print(output)
        # Pause once after output
        try:
            input("\nPress Enter to exit...")
        except (KeyboardInterrupt, EOFError):
            pass
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
                # empty input — ask again
                continue

            if prompt.lower() == "exit":
                break

            output = send_prompt(prompt, args.model)
            if output:
                print("\nResponse:\n")
                print(output)

            # After showing the response, ask the follow-up / pause question
            try:
                follow = input("\nIs there anything else I can help you with? (type 'exit' to quit): ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break

            if not follow:
                # user pressed Enter — continue to next iteration and ask main prompt again
                continue
            if follow.lower() == "exit":
                break
            # If the user typed another question, treat it as the next prompt immediately
            prompt = follow
            output = send_prompt(prompt, args.model)
            if output:
                print("\nResponse:\n")
                print(output)
            # then loop continues and will ask the follow-up again

    except Exception:
        logging.exception("Unexpected error")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
# ...existing code...