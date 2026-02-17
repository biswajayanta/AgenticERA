# Tool-Enhanced Weather Chat Agent

This project extends the basic conversational agent by adding **tool calling** capabilities so the model can fetch live weather data from OpenWeather and use it in its replies.

***

## Key Difference vs. Basic Conversation Agent

The earlier **Basic Conversation Agent** only used the OpenAI model and its internal knowledge to chat; it could not access real-time data.

This **Weather Chat Agent** introduces:

- A Python **tool function** (`get_current_weather`) that calls the OpenWeather API.
- A **tool schema** (`weather_tool`) passed to the model.
- A two-step **tool calling loop**:
    - First call: the model decides whether to call the weather tool.
    - Second call: the model uses the tool output and responds to the user.

In short, the basic agent is *pure LLM chat*, while this agent is an **LLM + external API tool** integration that can answer current weather queries with live data.

***

## Features

- **Live Weather Lookups** using OpenWeather API.
- **Automatic Tool Use**: the model decides when to call the weather tool.
- **Full Conversation History** for contextual responses.
- **Command-line Interface** with graceful exit (`quit`, `exit`, `bye`).
- **Configurable Units**: metric (Celsius) or imperial (Fahrenheit).

***

## Prerequisites

- Python 3.8+
- OpenAI API key
- OpenWeather API key
- Installed packages:
    - `openai`
    - `python-dotenv`
    - `requests`

Install dependencies:

```bash
pip install openai python-dotenv requests
```


***

## Environment Variables

The script expects a `.env` (or equivalent) file, loaded from:

```python
env_path = r'C:/Users/biswa/OneDrive/Documents/Agentic ERA/Variables.env'
```

That file should define:

```env
OPENAI_API_KEY=your-openai-key
OPENWEATHER_API_KEY=your-openweather-key
```

Adjust `env_path` in the code if your path differs.

***

## How It Works

1. **Weather tool implementation**
    - `get_current_weather(city, country, units)` calls the OpenWeather Current Weather API.
    - It returns a compact text summary like:
        - `Weather in Paris,FR: clear sky | Temperature: 18° (feels like 17°) | Humidity: 60% | Wind speed: 3 m/s`
2. **Tool schema**
    - `weather_tool` describes the function to the model:
        - Name, description.
        - Parameters: `city`, `country`, `units` (`metric` or `imperial`).
        - Marked `strict: True` and with `required` fields.
3. **Chat loop with tool calling**
    - System prompt tells the model it **has a weather tool** and should use it for current weather questions.
    - First OpenAI call:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=[weather_tool],
    tool_choice="auto",
    temperature=0.7,
    max_tokens=500,
)
```

    - If `choice.tool_calls` is present, the code:
        - Parses `tool_call.function.arguments`.
        - Calls `get_current_weather(...)` in Python.
        - Appends the tool call and its result to `messages` (`role: "tool"`).
    - Second OpenAI call uses updated `messages` so the model can craft a final, user-friendly answer that includes the live weather data.
    - If no tool is needed, it just responds directly like the basic agent.

***

## Running the Agent

Save the script (for example as `weather_chat_agent.py`), then run:

```bash
python weather_chat_agent.py
```

You’ll see:

```text
Chat Agent Started! (Type 'quit' to exit)
--------------------------------------------------
```

Example interaction:

```text
You: What's the current weather in Paris, France in Celsius?
Assistant: It’s currently clear sky in Paris, France. The temperature is about 18° (feels like 17°), with around 60% humidity and light winds at about 3 m/s.
```

You can still use it as a general chat assistant:

```text
You: Also, explain how this tool works in simple terms.
Assistant: ...
```

Type `quit`, `exit`, or `bye` to end the session.

***

## Customization

- **Change model**: switch `gpt-4o-mini` to `gpt-4o` for higher quality.
- **Default units**: change the fallback `"metric"` in the tool call.
- **Additional tools**: define more tool schemas and functions, then add them to the `tools=[...]` list.
- **System behavior**: tweak the system message to refine how aggressively the model uses the tool.

***

Would you like a side‑by‑side comparison section (table) between this agent and the basic one for inclusion in a GitHub README?

