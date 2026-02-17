from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import json

# Load environment
env_path = os.path.join(r'C:/Users/biswa/OneDrive/Documents/Agentic ERA/Variables.env')
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
AIRNOW_API_KEY = os.getenv("AIRNOW_API_KEY")

# --------- Tool implementation (Python side) ---------
def get_current_weather(city: str, country: str, units: str):
    """
    Call OpenWeather current weather API and return a compact text summary.
    """
    if OPENWEATHER_API_KEY is None:
        return "Weather service is not configured (missing OPENWEATHER_API_KEY)."

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    q = f"{city},{country}"  # always both

    params = {
        "q": q,
        "appid": OPENWEATHER_API_KEY,
        "units": units,  # metric -> Celsius, imperial -> Fahrenheit
    }

    try:
        resp = requests.get(base_url, params=params, timeout=10)
        data = resp.json()

        if resp.status_code != 200:
            msg = data.get("message", "Unknown error")
            return f"Could not fetch weather for '{q}': {msg}."

        main = data.get("main", {})
        wind = data.get("wind", {})
        weather_list = data.get("weather", [])
        desc = weather_list[0]["description"] if weather_list else "No description" 
        temp = main.get("temp")
        feels_like = main.get("feels_like")
        humidity = main.get("humidity")
        wind_speed = wind.get("speed")

        # Build a readable summary
        parts = [
            f"Weather in {q}: {desc}",
            f"Temperature: {temp}° (feels like {feels_like}°)",
            f"Humidity: {humidity}%",
            f"Wind speed: {wind_speed} m/s",
        ]

        return " | ".join(parts)

    except Exception as e:
        return f"Error calling OpenWeather API: {e}"

def get_current_air_quality(zip_code: str):
    """
    Call AirNow API for current air quality observations by ZIP code and return a compact text summary.
    """
    if AIRNOW_API_KEY is None:
        return "AirNow service is not configured (missing AIRNOW_API_KEY). Get a free key at https://docs.airnowapi.org."

    base_url = "https://www.airnowapi.org/aq/observation/zipCode/current/"
    params = {
        "format": "JSON",
        "zipCode": zip_code,
        "API_KEY": AIRNOW_API_KEY,
        "distance":25
    }

    try:
        resp = requests.get(base_url, params=params, timeout=10)
        data = resp.json()

        if resp.status_code != 200:
            return f"Could not fetch air quality for ZIP '{zip_code}': HTTP {resp.status_code}"

        if not data:
            return f"No air quality observations available for ZIP '{zip_code}'."

        # Summarize first/recent observation (typically latest hour)
        obs = data[0]
        aqi = obs.get("AQI", "N/A")
        category = obs.get("Category", {}).get("Name", "Unknown")
        param = obs.get("ParameterName", "Unknown")
        hour = obs.get("HourObserved", "Unknown")

        summary = f"Air quality at ZIP {zip_code} ({hour}:00): AQI {aqi} ({category}) for {param}"
        return summary

    except Exception as e:
        return f"Error calling AirNow API: {e}"

# --------- Tool schemas for the model ---------
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": (
            "Get the latest weather conditions for a city by calling an external "
            "weather API. Use this whenever the user asks about current weather."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g., 'Paris'",
                },
                "country": {
                    "type": "string",
                    "description": "Country code or name, e.g., 'FR' or 'France'",
                },
                "units": {
                    "type": "string",
                    "description": "Units: 'metric' for Celsius, 'imperial' for Fahrenheit",
                    "enum": ["metric", "imperial"],
                },
            },
            "required": ["city", "country", "units"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

air_quality_tool = {
    "type": "function",
    "function": {
        "name": "get_current_air_quality",
        "description": (
            "Get the latest air quality index (AQI) for a US location by ZIP code using AirNow API. "
            "Use this for queries about air quality, pollution, or AQI."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "zip_code": {
                    "type": "string",
                    "description": "US ZIP code, e.g., '10001' for New York City",
                },
            },
            "required": ["zip_code"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

def chat_agent():
    """Main chat function that handles the conversation loop"""
    # Conversation history
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant with access to two tools: weather (for current weather by city/country) "
                "and air quality (for current AQI by US ZIP code via AirNow). "
                "Call the appropriate tool(s) based on the query. You can call both if relevant. "
                "For weather, always specify city, country, and units. For air quality, use US ZIP codes."
            ),
        }
    ]

    print("Multi-Agent Chat Started! (Weather + AirNow Air Quality. Type 'quit' to exit)")
    print("-" * 60)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break
        if not user_input:
            continue 
        
        # Track tools used in this turn
        used_tools = set()
        
        messages.append({"role": "user", "content": user_input})

        try:
            # First call: let the model decide whether to use tool(s)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=[weather_tool, air_quality_tool],
                tool_choice="auto",  # model can choose whether/how to call tools
                temperature=0.7,
                max_tokens=500,
            )

            choice = response.choices[0].message
            if choice.tool_calls:
                # Track tools called
                for tool_call in choice.tool_calls:
                    used_tools.add(tool_call.function.name)

                # The model wants to call one or more tools
                messages.append(
                    {
                        "role": "assistant",
                        "tool_calls": choice.tool_calls,
                        "content": None,
                    }
                )

                # Execute all tool calls
                for tool_call in choice.tool_calls:
                    fn_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments or "{}")

                    if fn_name == "get_current_weather":
                        tool_result = get_current_weather(
                            city=args.get("city", ""),
                            country=args.get("country"),
                            units=args.get("units", "metric"),
                        )
                    elif fn_name == "get_current_air_quality":
                        tool_result = get_current_air_quality(
                            zip_code=args.get("zip_code", "")
                        )
                    else:
                        tool_result = "Unknown tool."

                    # Add tool result to messages
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": fn_name,
                            "content": tool_result,
                        }
                    )

                # Second call: let the model respond using tool output(s)
                followup = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500,
                )

                assistant_message = followup.choices[0].message.content
                messages.append({"role": "assistant", "content": assistant_message})
                print(f"\nAssistant: {assistant_message}")
                
            else:
                # No tool needed; respond directly
                assistant_message = choice.content
                messages.append({"role": "assistant", "content": assistant_message})
                print(f"\nAssistant: {assistant_message}")

            # Log tool usage for this interaction
            print_tool_usage(used_tools)

        except Exception as e:
            print(f"\nError: {e}")
            print("Please check your API keys, tool configuration, and internet connection.")

def print_tool_usage(used_tools: set):
    """Print a summary of tools used in this turn."""
    if not used_tools:
        print("🛠️ No tools used.")
    else:
        tools_list = ", ".join(sorted(used_tools))
        print(f"🛠️ Tools used: {tools_list}")

if __name__ == "__main__":
    chat_agent()
