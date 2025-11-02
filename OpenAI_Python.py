# ...existing code...
import os
import argparse
import logging
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=r"C:\Users\Brian Pacio\source\repos\API_KEY.env")
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your API_KEY.env file path and contents.")

client = OpenAI(api_key=api_key)
logging.basicConfig(level=logging.WARNING)


def parse_response(resp):
    return getattr(resp, "output_text", None) or str(resp)


def send(prompt, model):
    try:
        return parse_response(client.responses.create(model=model, input=prompt))
    except Exception as e:
        logging.exception("API request failed")
        print("Request failed:", e)
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--prompt")
    args = parser.parse_args()

    try:
        # initial prompt (either from arg or interactive)
        prompt = args.prompt or input("What can I help you today? ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        return 0

    if not prompt:
        return 0

    while True:
        if prompt.lower() == "exit":
            break

        out = send(prompt, args.model)
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
        prompt = follow

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
# ...existing code...