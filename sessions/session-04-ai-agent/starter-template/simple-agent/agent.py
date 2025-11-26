from google.adk.agents.llm_agent import Agent

# --- 1. THE TOOL ---
# In ADK, a tool is just a Python function with type hints and a docstring.
# The Agent reads the docstring to know WHEN to use it.

def get_weather(city: str) -> str:
    """
    Fetches the current weather conditions for a specific city.
    Use this tool whenever a user asks about the weather.
    """
    print(f"\n[TOOL CALLED] get_weather was triggered for: {city}")
    
    city_lower = city.lower()
    if "london" in city_lower:
        return "Rainy, 12°C, Chance of precipitation: 80%"
    elif "san francisco" in city_lower:
        return "Foggy, 15°C, Wind: 10mph"
    elif "mumbai" in city_lower:
        return "Humid, 30°C, Sunny"
    else:
        return "Sunny, 22°C (Simulated default)"

# --- 2. THE AGENT ---
# This is the "Blueprint". It connects the Model + Instructions + Tools.

root_agent = Agent(
    name="weather_bot",
    model="gemini-2.5-flash-lite",
    description="A helpful assistant that checks the weather.",
    instruction="""
    You are a friendly Weather Bot.
    - If the user asks for weather, ALWAYS use the `get_weather` tool.
    - If the tool returns data, summarize it cheerfully.
    - If the user asks anything else (like math), politely decline.
    """,
    tools=[get_weather]
)