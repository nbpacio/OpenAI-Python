# OpenAI-Python CLI

Small CLI wrapper to call the OpenAI Responses API from the command line.

Usage
```
# Install dependencies
pip install -r requirements.txt

# Run interactively (loads .env from project root if present)
python OpenAI_Python.py

# Run non-interactively
python OpenAI_Python.py --prompt "Hello world" --model gpt-4.1-nano

# Use a specific .env file
python OpenAI_Python.py --env-file ./API_KEY.env

# Pause at the end (useful on Windows double-click)
python OpenAI_Python.py --pause
```

Environment
- Set `OPENAI_API_KEY` in your environment or in a `.env` file with the line:

```
OPENAI_API_KEY=sk-...your key...
```

Notes
- The script attempts to be defensive about response shapes returned by different SDK versions; if you see unexpected output, add `--verbose` to get more logging.
- Do NOT commit keys to git. Add `.env`/`API_KEY.env` to your `.gitignore`.
# OpenAI-Python

# Install Python and Python-Denv
pip install python python-denv

# Install OpenAPI
pip install openapi




