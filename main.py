import asyncio
from typing import Awaitable, Callable, TypeVar
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName
from pydantic_ai.settings import ModelSettings

from dotenv import load_dotenv

T = TypeVar("T")


async def retry(
    func: Callable[..., Awaitable[T]],
    num_retries: int = 5,
    retry_backoff_delay: float = 1.0,
    retry_backoff_factor: float = 2.0,
) -> T:
    """
    Retry a function call with exponential backoff.

    Args:
        func: The function to call.
        num_retries: The number of retries.
        retry_backoff_delay: The initial delay between retries.
        retry_backoff_factor: The backoff factor.

    Returns:
        The result of the function call.

    Raises:
        Exception: If the function call fails after all retries.
    """
    for attempt in range(num_retries):
        try:
            return await func()
        except Exception as e:
            if attempt < num_retries - 1:
                delay = retry_backoff_delay * (retry_backoff_factor**attempt)
                print(
                    f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds..."
                )
                await asyncio.sleep(delay)

    raise Exception(f"Function call failed after {num_retries} attempts")


async def main() -> None:
    load_dotenv()

    agent = Agent(
        model_settings=ModelSettings(timeout=5.0),
    )

    # MODEL
    model_name: KnownModelName = "openai:gpt-4.1-nano"
    prompt = "Who is Rick Astley?"

    # local function to run the API call
    async def run_api_call() -> str:
        """Execute the API call to the agent."""
        result = await agent.run(
            model=model_name,
            user_prompt=prompt,
        )
        return result.output

    response = await retry(run_api_call)

    # or alternatively with a lambda, only works with sync agent
    # response = retry(
    #     lambda: agent.run_sync(model=model_name, user_prompt=prompt).output,
    # )

    print(f"API call successful: {response}")


if __name__ == "__main__":
    asyncio.run(main())
