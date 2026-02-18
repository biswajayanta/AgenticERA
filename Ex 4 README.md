

# Multi-Tool AI Agent with Tool Usage Logging

This enhanced Python project builds on the basic tool-calling agent by adding real-time visibility into which tools the AI selects. After each response, it displays exactly which tools were called (e.g., "🛠️ Tools used: get_current_weather"), making agent decision-making transparent for demos and debugging.

The core functionality remains identical: OpenAI's gpt-4o-mini intelligently routes weather/AQI queries to live APIs while maintaining full conversation history.

## Key Features

- **Dual External Tools**: Worldwide weather (OpenWeatherMap) + US air quality (AirNow AQI).
- **Visible Tool Selection**: `print_tool_usage()` logs every tool call per interaction.
- **Multi-Tool Support**: Handles single or combined tool calls in one response.
- **Production Error Handling**: API failures, missing keys, timeouts all gracefully managed.
- **CLI with History**: Natural multi-turn conversations; 'quit' to exit.


## Key Differences from Basic Agent

| Feature | Basic Agent | This Enhanced Agent |
| :-- | :-- | :-- |
| Tool Visibility | None (silent execution) | Prints 🛠️ summary after each response |
| Demo-Friendly | Limited transparency | Perfect for workshops - shows AI reasoning |
| Debugging | Manual message inspection | Automatic per-turn tool logging |
| Code Changes | None | Added `used_tools=set()` + `print_tool_usage()` |

## Prerequisites

- Python 3.10+ with `pip install openai python-dotenv requests`
- **API Keys** (all free except OpenAI):

```
OPENAI_API_KEY=sk-... (paid, ~$0.15/1M tokens)
OPENWEATHER_API_KEY=... (free: openweathermap.org/api)
AIRNOW_API_KEY=... (free: docs.airnowapi.org)
```


## Quick Setup

1. Save as `agent_with_logging.py`
2. Create `Variables.env` at your Windows path:

```
C:/Users/biswa/OneDrive/Documents/Agentic ERA/Variables.env
```

3. Run: `python agent_with_logging.py`

## Demo Examples \& Expected Output

```
You: Weather in Bengaluru, India?
Assistant: Weather in Bengaluru,IN: clear sky | Temperature: 28.5° (feels like 27.8°) | Humidity: 62% | Wind speed: 3.6 m/s
🛠️ Tools used: get_current_weather

You: Air quality ZIP 10001 + Paris weather?
Assistant: [Combined response with both APIs]
🛠️ Tools used: get_current_air_quality, get_current_weather

You: Tell me a joke
Assistant: Why did the computer go to therapy? It had too many bytes of emotional baggage!
🛠️ No tools used.
```


## Code Architecture

```
Core Flow (per user message):
1. Model call → tool_choice="auto" decides tools needed
2. Track used_tools=set() during tool_calls loop
3. Execute tools → add ToolMessage to history
4. 2nd model call → natural language response
5. print_tool_usage(used_tools) → transparency!
```

**New Components:**

```python
used_tools = set()  # Tracks per-turn tool selection
for tool_call in choice.tool_calls:
    used_tools.add(tool_call.function.name)  # Log decision

def print_tool_usage(used_tools: set):  # Emoji-enhanced logging
    # 🛠️ Tools used: get_current_weather, get_current_air_quality
```


## Customization Options

| Modify | Code Location | Impact |
| :-- | :-- | :-- |
| Log Format | `print_tool_usage()` | Add timestamps, file logging |
| Model | `model="gpt-4o-mini"` | Better reasoning with gpt-4o |
| Tools List | `tools=[weather_tool, air_quality_tool]` | Add population, news APIs |
| Temperature | `temperature=0.7` | 0.1=deterministic, 1.0=creative |

## Troubleshooting

| Error | Root Cause | Fix |
| :-- | :-- | :-- |
| `ModuleNotFoundError` | Missing packages | `pip install openai python-dotenv requests` |
| `Invalid API Key` | .env formatting | No quotes/spaces around keys |
| `No module named 'openai'` | Environment | Use same terminal as pip install |
| Windows path error | Raw strings | `r'C:/Users/biswa/...'` already handled |
| Rate limited | OpenAI quota | Wait 60s or check usage dashboard |

## Perfect for Engineering Workshops

- **Live Demo Value**: Students see AI "thinking" via tool logs
- **Educational**: Demonstrates OpenAI's `tool_choice="auto"` intelligence
- **Extensible**: Easy pattern for 3rd-party API integration
- **Transparent**: No black-box magic - decisions visible instantly

**Sample Workshop Flow:**

1. Run basic queries → see 🛠️ logs
2. Try ambiguous query → watch auto-routing
3. Break a key → observe graceful fallbacks
4. Students fork → add their own API tool

MIT License. Ideal for agentic AI education. Built for Bengaluru engineering sessions! 🚀


