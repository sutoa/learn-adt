import datetime
from zoneinfo import ZoneInfo
import requests
from google.adk.agents import Agent, LlmAgent
from google.adk.models.lite_llm import LiteLlm
from .config import OPENAI_API_KEY

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


def get_post(post_id: int) -> dict:
    """Retrieves a post from JSONPlaceholder API by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        dict: status and result or error msg.
    """
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        return {
            "status": "success",
            "post": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch post {post_id}: {str(e)}"
        }

root_agent = LlmAgent(
    name="weather_time_agent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time, get_post],
)