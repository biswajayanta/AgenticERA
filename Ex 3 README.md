<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Multi-Tool AI Agent (Weather + Air Quality)

This Python project creates a conversational AI agent using OpenAI's tool-calling API. The agent intelligently decides when to fetch live data: current weather worldwide via OpenWeatherMap or US air quality (AQI) via AirNow API.[^1][^2]

Unlike basic chat agents, this supports multiple external tools in one conversation loop, demonstrating agentic behavior where the model routes queries automatically.[^2][^3]

## Key Features

- **Dual Tools**: Weather for any city (Celsius/Fahrenheit) and AQI for US ZIP codes.
- **Auto Tool Selection**: Model chooses tool(s) based on query; handles both in one response.
- **Conversation History**: Full context maintained for natural multi-turn chats.
- **Error Handling**: Graceful fallbacks for missing keys or API failures.
- **CLI Interface**: Simple terminal chat; type 'quit' to exit.


## Prerequisites

- Python 3.10+.
- OpenAI account (gpt-4o-mini model; ~\$0.15/1M tokens).
- Free API keys:
    - OpenWeatherMap: [openweathermap.org/api](https://openweathermap.org/api).
    - AirNow: [docs.airnowapi.org](https://docs.airnowapi.org).


## Quick Setup

1. Clone/save as `agent.py`.
2. Create `Variables.env` at `C:/Users/biswa/OneDrive/Documents/Agentic ERA/Variables.env`:

```
OPENAI_API_KEY=your_openai_key_here
OPENWEATHER_API_KEY=your_openweather_key
AIRNOW_API_KEY=your_airnow_key
```

3. Install dependencies:

```
pip install openai python-dotenv requests
```

4. Run: `python agent.py`.[^4]

## Usage Examples

- Weather: "What's the weather in Bengaluru, India?"
- Air Quality: "Air quality in ZIP 10001?"
- Combined: "Weather in Paris, FR and air quality near New York ZIP 10001?"
- Non-tool: "Tell me a joke."

The agent responds with live data summaries like: "Weather in Bengaluru,IN: clear sky | Temperature: 28.5° (feels like 27.8°) | Humidity: 62% | Wind speed: 3.6 m/s". [^3]

## Code Structure

```
Main components:
├── Environment loading (.env)
├── Tool functions (get_current_weather, get_current_air_quality)
├── Tool schemas (JSON for OpenAI)
└── chat_agent() loop: model call → tool exec → final response
```

Tool calls use `tool_choice="auto"` for intelligent selection.[^2]

## Customization

| Change | Location | Example |
| :-- | :-- | :-- |
| Model | `client.chat.completions.create(model=...)` | `"gpt-4o"` for better reasoning |
| Units | `get_current_weather(..., units="imperial")` | Fahrenheit default |
| Add Tool | Append to `tools=[weather_tool, air_quality_tool, new_tool]` | World Bank population API [^5] |
| System Prompt | `messages[^0]["content"]` | "Focus on environment queries" |

## Troubleshooting

| Issue | Fix |
| :-- | :-- |
| Missing key | Check `.env` (no quotes/spaces); reload with `load_dotenv()` [^3] |
| Rate limit | Upgrade OpenAI tier or add `time.sleep(1)` |
| ZIP no data | Use valid US ZIP; AirNow covers ~3000 stations [^3] |
| Path error (Windows) | Use `r'C:\path\to\Variables.env'` [^1] |

## For Engineering Demos

Perfect for student workshops: shows tool calling, API integration, error handling. Test queries highlight agent decisions. Extend with logging: print tool names post-execution.[^6][^4]

MIT License. Built for agentic AI sessions.[^1]

<div align="center">⁂</div>

[^1]: https://www.perplexity.ai/search/262bca2f-5976-4a79-b2b2-07fe4aafc20c

[^2]: https://www.perplexity.ai/search/ca78217f-8a3a-4c29-88b9-6089cd25d24d

[^3]: https://www.perplexity.ai/search/b71fcb9b-6a09-4886-9ddc-d319f162d014

[^4]: https://www.perplexity.ai/search/cef1c2a2-88a3-4541-901a-de36ded8d0db

[^5]: https://www.perplexity.ai/search/5b3f534c-39ac-42ed-aa4e-f6ece66a6fe9

[^6]: https://www.perplexity.ai/search/9c8cd964-ae29-4d4c-9d01-a2fc8f1a969c

