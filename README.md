# TODO

- [ ] Add install and setup section
- [ ] Add framework details and extensibilty
- [ ] Add Usage Examples
- [ ] Add todo's for initial functionality
- [ ] Build out RAG framework
- [ ] (Optional) create a front end

# Install and setup

## Ollama
If using a package manager like `brew`, Ollama should be available
- `brew install --cask ollama`

Otherwise, visit [Ollama's website](https://ollama.com/) for more information on how to install.

Once Ollama is installed, pull the `gemma3:4b` model. By default, the agent uses this mode. More on how to customize which model the base agent or helper agents use below.
- `ollama pull gemma3`

## Python Requirements

1. (Optional) Create a virtual environment (i.e. `virtualenv .venv`, `uv venv`)
2. Source the venv and install requirments
    a. `source .venv/bin/activate && pip install -r requirements.txt`

## RUN!

1. From the root directory, start the agent in your terminal:
    a. `python3 main.py`
2. Interact with the agent through your terminal just as you would any other chat.

# Framework 


# Useage Examples
