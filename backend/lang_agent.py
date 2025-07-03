# backend/lang_agent.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from calendar_utils import book_meeting_on_calendar


# Load environment variables from .env file
load_dotenv()

# ✅ Optional: Ensure GOOGLE_API_KEY is set
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("❌ GOOGLE_API_KEY is not set. Please check your .env file.")

# Dummy calendar tool (can be replaced with real logic)
# def book_meeting_dummy(_input: str) -> str:
#     return "✅ Meeting booked from 3 PM to 4 PM!"

# Define tools
tools = [
    Tool(
        name="BookMeeting",
        func=book_meeting_on_calendar,
        description=(
        "Books a 1-hour meeting using Google Calendar. "
        "You must clearly mention the day and time, e.g., 'next Sunday at 3pm' or 'tomorrow at 9 AM'."
    )
    )
]

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.5
)

# Create agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_agent(message: str) -> dict:
    result = agent.invoke({"input": message})

    # Extract intermediate reasoning steps
    steps = [
        {
            "tool": step[0].name,
            "tool_input": step[0].tool_input,
            "observation": step[1],
        }
        for step in result.get("intermediate_steps", [])
    ]

    return {
        "steps": steps,
        "final_answer": result.get("output", "No final answer."),
    }

# def run_agent_verbose(message: str) -> dict:
#     result = agent.invoke({"input": message})

#     # Process intermediate steps
#     steps = []
#     for action, observation in result.get("intermediate_steps", []):
#         steps.append({
#             "tool": action.tool,
#             "tool_input": str(action.tool_input),
#             "observation": str(observation)
#         })

#     return {
#         "final_answer": result.get("output", ""),
#         "steps": steps
#     }
