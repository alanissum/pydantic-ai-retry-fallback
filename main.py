import asyncio
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from dotenv import load_dotenv


async def main() -> None:
    load_dotenv()

    agent = Agent(
        model_settings=ModelSettings(timeout=5.0),
    )

    # MODEL
    model_name = ""
    prompt = "Who is Rick Astley?"

    # RETRY
    num_retries = 5

    for retry in range(num_retries):
        try:
            response = await agent.run(
                model=model_name,
                user_prompt=prompt,
            )
            if response:
                break

        except Exception as e:
            print(f"Error invoking API (retry {retry}/{num_retries}): {e}")
    else:
        # if the for loop doesn't break, all retries have failed
        raise ValueError(f"API call unsuccessful after {num_retries} attempts")

    print(f"API call successful: {response}")


if __name__ == "__main__":
    asyncio.run(main())
