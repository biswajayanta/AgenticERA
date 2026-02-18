<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# LangGraph Multi-Tool AI Agent

This advanced Python project converts the previous OpenAI function-calling agent into a **LangGraph stateful graph workflow**. It maintains identical weather + air quality functionality while adding production-grade features like visual tool tracking, typed state management, and streaming execution.

**Key upgrade**: Uses LangGraph's graph-based architecture instead of manual message loops, making it more scalable and maintainable for complex agentic workflows.

## Key Features

- **LangGraph Architecture**: Nodes (`agent`, `tools`) + conditional edges for tool routing
- **Enhanced Tool Visibility**: Real-time logging shows "🎯 AGENT SELECTED TOOL: get_current_weather"
- **Typed State**: `AgentState` tracks messages + tools_used with type safety
- **Production Components**: Streaming, error handling, `@tool` decorators
- **Identical APIs**: Same OpenWeather + AirNow endpoints as previous versions


## Architecture Differences

| Aspect | OpenAI Function Calling | LangGraph Version |
| :-- | :-- | :-- |
| **Structure** | Manual `while True:` loop | `StateGraph` with nodes/edges |
| **Tool Binding** | JSON tool schemas | `llm.bind_tools(tools)` + `@tool` |
| **State Mgmt** | `messages` list | `TypedDict` with `Annotated` |
| **Tool Execution** | Manual `if fn_name ==` | `ToolNode` + custom tracking |
| **Visibility** | Basic 🛠️ logging | Rich 🎯🔧💬 emoji feedback |
| **Scalability** | 2-3 tools max | Unlimited tools/nodes |

## Prerequisites

```
Python 3.10+
pip install langchain langchain-openai langchain-core langgraph python-dotenv requests
API Keys (Variables.env):
OPENAI_API_KEY=sk-... (paid)
OPENWEATHER_API_KEY=... (free)
AIRNOW_API_KEY=... (free)
```


## Quick Setup

1. Save as `langgraph_agent.py`
2. Use same `Variables.env` path as previous agents
3. `pip install -r requirements.txt` (see below)
4. `python langgraph_agent.py`

## Sample Output (Demo-Ready)

```
🧠 LangGraph Agent Started! (Weather + Air Quality)
📋 Available tools: get_current_weather, get_current_air_quality

👤 You: Weather in Bengaluru + NYC air quality?
🤖 Agent analyzing 'Weather in Bengaluru + NYC air quality'...
🎯 AGENT SELECTED TOOL: get_current_weather, get_current_air_quality
🔧 EXECUTING: get_current_air_quality, get_current_weather

💬 Assistant: Weather in Bengaluru,IN: clear sky | Temperature: 28.5°... 
           Air quality ZIP 10001: AQI 42 (Good) for Ozone
```


## requirements.txt

```
langchain-openai==0.2.5
langchain-core==0.3.14
langgraph==0.2.12
openai==1.35.0
python-dotenv==1.0.1
requests==2.31.0
typing-extensions==4.12.0
```


## Code Architecture

```
Graph Flow:
START → agent (llm.bind_tools()) 
     → should_continue? → tools (ToolNode) → agent → ...
     → Final AIMessage → END

Key Components:
├── AgentState(TypedDict): messages + tools_used tracking
├── create_agent(): LLM reasoning with tool_calls extraction
├── create_tool_node(): ToolNode + execution logging
├── should_continue(): Routes to tools or END
└── chat_agent(): Streaming CLI interface
```


## Customization Guide

| Feature | Modification | Location |
| :-- | :-- | :-- |
| **Add Tool** | `@tool def new_tool():` + `tools.append(new_tool)` | `create_weather_agent()` |
| **Change LLM** | `ChatOpenAI(model="gpt-4o")` | Line in `create_weather_agent()` |
| **Persistent State** | `app.invoke({"messages": [...]})` | Replace streaming loop |
| **Custom Logging** | Modify `print()` in `tracked_tool_node` | `create_tool_node()` function |
| **Graph Visualization** | `app.get_graph().draw_png("graph.png")` | After `workflow.compile()` |

## Comparison: Evolution Path

```
1. Basic Chat → 2. OpenAI Tools → 3. OpenAI + Logging → 4. THIS (LangGraph)
   [No tools]    [Silent tools]   [🛠️ Logs]        [🎯🔧 Streaming + Typed]
```


## Troubleshooting

| Issue | Symptoms | Solution |
| :-- | :-- | :-- |
| `No module langgraph` | ImportError | `pip install langgraph` |
| `TypedDict error` | Type hints fail | `pip install typing-extensions` |
| `Stream empty` | No 🎯 logs | Check `stream_mode="values"` |
| **Windows Path** | Env not loading | `r'C:/Users/biswa/...'` (already set) |
| **Rate Limits** | 429 errors | Add `time.sleep(1)` in loop |

## Perfect for Advanced Workshops

**Why LangGraph wins for engineering students:**

- ✅ **Production Pattern**: Real apps use graphs, not while loops
- ✅ **Visual Debugging**: See exact tool flow in real-time
- ✅ **Type Safety**: `mypy` compatible, IDE autocomplete
- ✅ **Scalable**: Add 10+ tools without code changes
- ✅ **Streaming**: Feels responsive like ChatGPT

**Live Demo Flow:**

1. Basic query → see single-tool selection
2. Multi-tool → watch parallel execution
3. No-tool → observe clean END path
4. Students extend → add stock/news API

MIT License. Next-gen agentic AI education! 🚀

