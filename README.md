# PromptSlicerLlmWrapper

### Decription
TK

### Setup instructions
1. Create a file named `config.py` in the root directory and add the following:
```
API_KEY = "REDACTED"
REPO_URL = "REDACTED"
```

`API_KEY` is your key for accessing the LLM. This project uses [OpenRouter](https://openrouter.ai/) (a free-to-use platform) to interact with language models. You can generate your API key [here](https://openrouter.ai/settings/keys).

`REPO_URL` is the GitHub URL of the repository or project you want to analyze. For testing, you can use my public GitHub repo: https://github.com/akshit04/StackOverflow.

You can customize the input by either modifying the prompt content directly or updating `github_processor.py` to support additional file extensions.

2. Run the python program from root directory:
```
> python3 main.py
```


### Sample Responses
The `sample_responses` folder contains example outputs from a dry run on my own public GitHub repository: https://github.com/akshit04/StackOverflow.
