# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from your .env file
load_dotenv(dotenv_path=r"C:\Users\Brian Pacio\source\repos\API_KEY.env")

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Verify the key was found
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your API_KEY.env file path and contents.")

# Initialize the OpenAI client
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


# END OF CODE

