import os
from dotenv import load_dotenv
import requests
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
import operator

# Load environment
env_path = os.path.join(r'C:/Users/biswa/OneDrive/Documents/Agentic ERA/Variables.env')
load_dotenv(dotenv_path=env_path)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
AIRNOW_API_KEY = os.getenv("AIRNOW_API_KEY")

# --------- Tool implementations ---------
@tool
def get_current_weather(city: str, country: str, units: str = "metric") -> str:
    """Get the latest weather conditions for a city by calling OpenWeather API."""
    if OPENWEATHER_API_KEY is None:
        return "Weather service is not configured (missing OPENWEATHER_API_KEY)."
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    q = f"{city},{country}"
    params = {"q": q, "appid": OPENWEATHER_API_KEY, "units": units}
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        data = resp.json()
        if resp.status_code != 200:
            return f"Could not fetch weather for '{q}': {data.get('message', 'Unknown error')}."
        main = data.get("main", {})
        wind = data.get("wind", {})
        weather_list = data.get("weather", [])
        desc = weather_list[0]["description"] if weather_list else "No description" 
        temp = main.get("temp")
        feels_like = main.get("feels_like")
        humidity = main.get("humidity")
        wind_speed = wind.get("speed")
        parts = [
            f"Weather in {q}: {desc}",
            f"Temperature: {temp}° (feels like {feels_like}°)",
            f"Humidity: {humidity}%",
            f"Wind speed: {wind_speed} m/s",
        ]
        return " | ".join(parts)
    except Exception as e:
        return f"Error calling OpenWeather API: {e}"

@tool
def get_current_air_quality(zip_code: str) -> str:
    """Get the latest air quality index (AQI) for a US location by ZIP code using AirNow API."""
    if AIRNOW_API_KEY is None:
        return "AirNow service is not configured (missing AIRNOW_API_KEY)."
    base_url = "https://www.airnowapi.org/aq/observation/zipCode/current/"
    params = {"format": "JSON", "zipCode": zip_code, "API_KEY": AIRNOW_API_KEY, "distance": 25}
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        data = resp.json()
        if resp.status_code != 200:
            return f"Could not fetch air quality for ZIP '{zip_code}': HTTP {resp.status_code}"
        if not data:
            return f"No air quality observations available for ZIP '{zip_code}'."
        obs = data[0]
        aqi = obs.get("AQI", "N/A")
        category = obs.get("Category", {}).get("Name", "Unknown")
        param = obs.get("ParameterName", "Unknown")
        hour = obs.get("HourObserved", "Unknown")
        return f"Air quality at ZIP {zip_code} ({hour}:00): AQI {aqi} ({category}) for {param}"
    except Exception as e:
        return f"Error calling AirNow API: {e}"

# --------- State Definition ---------
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    tools_used: List[str]  # Track which tools were called

# --------- Agent Node with Tool Tracking ---------
def create_agent(llm, tools):
    tool_names = {tool.name: tool for tool in tools}
    
    def agent(state: AgentState):
        messages = state['messages']
        response = llm.bind_tools(tools).invoke(messages)
        
        # Track tools used in this agent call
        tools_used_this_turn = []
        if hasattr(response, 'tool_calls') and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                if tool_name in tool_names:
                    tools_used_this_turn.append(tool_name)
        
        return {
            "messages": [response],
            "tools_used": tools_used_this_turn
        }
    
    return agent

# --------- Tool Node with Enhanced Logging ---------
def create_tool_node(tools):
    tool_node = ToolNode(tools)
    
    def tracked_tool_node(state: AgentState):
        tool_results = tool_node.invoke(state)
        
        # Extract tool names from the last tool messages
        tools_used = []
        if 'messages' in tool_results:
            for msg in tool_results['messages']:
                if isinstance(msg, ToolMessage):
                    tools_used.append(msg.name)
        
        print(f"🔧 EXECUTING: {', '.join(tools_used)}")
        
        return {
            **tool_results,
            "tools_used": tools_used
        }
    
    return tracked_tool_node

# --------- Compile Graph ---------
def create_weather_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    tools = [get_current_weather, get_current_air_quality]
    
    workflow = StateGraph(state_schema=AgentState)
    
    # Add nodes
    workflow.add_node("agent", create_agent(llm, tools))
    workflow.add_node("tools", create_tool_node(tools))
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Conditional edges
    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        return END
    
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    
    return workflow.compile(), tools

# --------- Main Chat Loop with Tool Demonstration ---------
def chat_agent():
    app, tools = create_weather_agent()
    
    print("🧠 LangGraph Agent Started! (Weather + Air Quality)")
    print("📋 Available tools:", ", ".join(t.name for t in tools))
    print("=" * 60)
    
    system_msg = HumanMessage(content=(
        "You are a helpful AI assistant with access to weather and air quality tools. "
        "Use get_current_weather for weather queries (needs city, country, units). "
        "Use get_current_air_quality for US ZIP code air quality queries."
    ))
    
    while True:
        user_input = input("\n👤 You: ").strip()
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("👋 Goodbye!")
            break
        if not user_input:
            continue
        
        # Run with tracked state
        state = {"messages": [system_msg, HumanMessage(content=user_input)], "tools_used": []}
        
        print(f"\n🤖 Agent analyzing '{user_input}'...")
        
        for step, output in enumerate(app.stream(state, stream_mode="values")):
            current_tools = output.get("tools_used", [])
            if current_tools:
                print(f"🎯 AGENT SELECTED TOOL: {', '.join(current_tools)}")
            
            # Print final response
            if "messages" in output:
                last_msg = output["messages"][-1]
                if isinstance(last_msg, AIMessage) and last_msg.content:
                    print(f"\n💬 Assistant: {last_msg.content}")
                    break

if __name__ == "__main__":
    chat_agent()
