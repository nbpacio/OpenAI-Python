# OpenAI-Python CLI

Small CLI wrapper to call the OpenAI Responses API from the command line.

## Usage

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run interactively (the script will attempt to load `API_KEY.env` from the repo root):

```powershell
python OpenAI_Python.py
```

Run non-interactively:

```powershell
python OpenAI_Python.py --prompt "Hello world" --model gpt-4o-mini
```

## API key (keep it secret)

Create a file named `API_KEY.env` in the repository root (one level above `OpenAI_Python.py`) with the single line:

```
OPENAI_API_KEY=sk-...your-key-here...
```

Or set the environment variable in PowerShell:

```powershell
setx OPENAI_API_KEY "sk-...your-key-here..."
```

Do NOT commit API keys to source control. Add `API_KEY.env` to `.gitignore`.

## Behavior

- The CLI prompts: "What can I help you today?"
- After printing the response it asks: "Is there anything else I can help you with? (type 'exit' to quit)"

## Running tests

Install pytest and run tests from the repo root:

```powershell
python -m pip install pytest
pytest -q
```

## Notes

- The script attempts to be defensive about response shapes returned by different SDK versions; the `parse_response` function handles `output_text`, structured `output` lists, object blocks with `.text`, and `to_dict()` fallbacks.

---

Generated: updated usage and API key instructions.
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
Linux:
OPENAI_API_KEY=sk-...your key...

Powershell:
setx OPENAI_API_KEY "sk-...your key..." 
```

Notes
- The script attempts to be defensive about response shapes returned by different SDK versions; if you see unexpected output, add `--verbose` to get more logging.
- Do NOT commit keys to git. Add `.env`/`API_KEY.env` to your `.gitignore`.

# END




