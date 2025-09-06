from dataclasses import dataclass
import datetime
from langchain.chat_models import init_chat_model

from langgraph.prebuilt import create_react_agent


from typing import Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from tools.gmail_tool import send_email
from tools.google_calendar_tool import list_calendar_events,create_calendar_event
from tools.time_table_tool import get_today_study_schedule
from tools.user_service_tool import get_user_additional_info



llm = init_chat_model("openai:gpt-4.1")


class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str

graph_builder = StateGraph(State)

tool = TavilySearch(max_results=2)
tools = [tool, list_calendar_events, create_calendar_event, get_today_study_schedule, get_user_additional_info, send_email]

# Use LangGraph's prebuilt create_react_agent for the agent node
instructions = (
    "You are a autonomous wellness agent that integrates with Google Calendar to auto-schedule mindful personalized breaks, focus sessions, and relaxation reminders for students based on their study timetable and habits. "
    "Always provide clear, concise, and accurate information. "
    "If you do not know the answer, say so honestly. "
    "When presenting calendar events, never show raw JSON. Instead, summarize the events in a user-friendly way, listing event titles, times, and key details. "
    f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}."
    "Use the provided tools to assist with user queries."
    "User system time zone always should be considered."
    "When suggesting wellness breaks, take into account the user's study schedule and preferences."
    "if required more information for creating personalized wellness plans, ask the user."
    "use get_today_study_schedule tool to get user's study schedule for today."
    "use get_user_additional_info tool to get user's additional information for wellness breaks."
    "once you have all the information, use create_calendar_event tool to schedule events in user's Google Calendar."
    "once you have created wellness break then share it with the user in a friendly format. and ask if they want to share it with others"
)
agent = create_react_agent(llm, tools, prompt=instructions)

graph_builder.add_node("agent", agent)

tool_node = ToolNode(tools=[tool, list_calendar_events])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
)
graph_builder.add_edge("tools", "agent")
graph_builder.set_entry_point("agent")
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)