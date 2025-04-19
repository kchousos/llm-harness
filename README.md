<h1 align='center'>🚧⚠️ Under Construction ⚠️🚧</h1>

This project uses LLMs to automatically generate fuzzing harnesses for your
C/C++ project.

## Installation

### Dependencies

- Python >=3.10
- [uv](https://docs.astral.sh/uv/)

    ```bash
    pipx install uv
    ```

### Installation Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/kchousos/llm-harness.git
    ```

2. Install the project:

    ```bash
    uv sync
    ```

## Execution

1. Add an OpenAI API key in `.env`, such as:

    ```bash
    # cat .env
    OPENAI_API_KEY=<API-key-here>
    ```
2. Execute the main script:

    ```bash
    uv run python main.py dateparse
    ```