# Retry / Fallback with Pydantic-AI

This project highlights a simple way to increase robustness when working with external APIs, such as LLM APIs from OpenAi, Google or Anthropic.

## Concepts

### Retry

Call the same api multiple times if a temporary problem prevents successfull responses.

### Fallback

Calling different models in case a provider is not reachable.

## Quickstart

### Prerequisites

- [uv](https://docs.astral.sh/uv/) package manager
- API keys for desired provider, see `.env.example` for reference

### Run Project

```
uv run main.py
```

