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

 
# --------- Tool schema for the model ---------
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": (
            "Get the latest weather conditions for a city by calling an external"
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

            # IMPORTANT: include every key from properties here
            "required": ["city", "country", "units"],
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
                "You are a helpful AI assistant. "
                "You have access to a weather tool and should call it whenever the "
                "user asks about current weather in any location."
            ),
        }
    ]

    print("Chat Agent Started! (Type 'quit' to exit)")
    print("-" * 50)
 
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break
        if not user_input:
            continue 
        messages.append({"role": "user", "content": user_input})

        try:
            # First call: let the model decide whether to use a tool
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=[weather_tool],
                tool_choice="auto",  # model can choose whether to call the tool
                temperature=0.7,
                max_tokens=500,
            )

            choice = response.choices[0].message
            if choice.tool_calls:
                # The model wants to call one or more tools
                for tool_call in choice.tool_calls:
                    fn_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments or "{}")

                    if fn_name == "get_current_weather":
                        tool_result = get_current_weather(
                            city=args.get("city", ""),
                            country=args.get("country"),
                            units=args.get("units", "metric"),
                        )

                        # Add the tool call and its result to the conversation
                        messages.append(
                            {
                                "role": "assistant",
                                "tool_calls": [tool_call],
                                "content": None,
                            }
                        )
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": fn_name,
                                "content": tool_result,
                            }
                        )
 
                        # Second call: let the model respond to the user using the tool output
                        followup = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages,
                            temperature=0.7,
                            max_tokens=500,
                        )

                        assistant_message = followup.choices[0].message.content
                        messages.append(
                            {"role": "assistant", "content": assistant_message}
                        )

                        print(f"\nAssistant: {assistant_message}")
            else:
                # No tool needed; respond directly
                assistant_message = choice.content
                messages.append({"role": "assistant", "content": assistant_message})
                print(f"\nAssistant: {assistant_message}")

        except Exception as e:
            print(f"\nError: {e}")
            print("Please check your API keys, tool configuration, and internet connection.")

if __name__ == "__main__":
    chat_agent()