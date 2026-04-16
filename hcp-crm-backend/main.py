from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import json
from datetime import datetime  # <--- NEW: Imported datetime

# --- Database Imports ---
from database import SessionLocal, InteractionLog

# --- LangChain & LangGraph Imports ---
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Load the Groq API key from .env
load_dotenv()

app = FastAPI()

# Allow the React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# --- 1. Redux State Mapping (Data Models) ---
class FormState(BaseModel):
    hcpName: str
    interactionType: str
    date: str
    time: str
    attendees: str
    topicsDiscussed: str
    materialsShared: list[str]
    samplesDistributed: list[str]
    sentiment: str
    outcomes: str
    followUpActions: list[str]

class ChatRequest(BaseModel):
    message: str
    formState: FormState


# --- 2. Define All 5 LangGraph Tools ---

@tool
def log_interaction_tool(hcpName: str, date: str, time: str, topicsDiscussed: str, sentiment: str, materialsShared: list[str]) -> dict:
    """
    TOOL 1: Use this tool ONLY when the user describes a NEW interaction. 
    It extracts the HCP Name, date, time, topics discussed, sentiment (Positive, Neutral, Negative), and materials.
    
    CRITICAL FORMATTING:
    - 'date' MUST be in 'YYYY-MM-DD' format.
    - 'time' MUST be in 'HH:MM' (24-hour) format.
    """
    print(f"\n--- TOOL TRIGGERED: log_interaction_tool for {hcpName} ---")
    return {
        "action": "OVERWRITE",
        "data": {
            "hcpName": hcpName,
            "date": date,
            "time": time,  # <--- NEW: Added time to the update payload
            "topicsDiscussed": topicsDiscussed,
            "sentiment": sentiment,
            "materialsShared": materialsShared
        }
    }

@tool
def edit_interaction_tool(field_to_update: str, new_value: str) -> dict:
    """
    TOOL 2: Use this tool when the user wants to EDIT, CORRECT, or CHANGE a specific field in the existing form.
    Examples: 'Change sentiment to positive', 'Update the date to tomorrow'.
    """
    print(f"\n--- TOOL TRIGGERED: edit_interaction_tool updating {field_to_update} ---")
    return {
        "action": "UPDATE",
        "data": {
            field_to_update: new_value
        }
    }

@tool
def fetch_hcp_history_tool(hcpName: str) -> dict:
    """
    TOOL 3: Use this tool when the user asks for history, past meetings, or background info on a specific HCP.
    """
    print(f"\n--- TOOL TRIGGERED: fetch_hcp_history_tool for {hcpName} ---")
    # Mock database lookup for history
    mock_db = {
        "Dr. Sharma": "Last met in Jan 2024. Discussed basic oncology products. Prefers digital brochures over physical samples.",
        "Dr. Smith": "Key Opinion Leader. Last met in March 2024. Very interested in clinical trial data.",
        "Dr. House": "Renowned diagnostician. Hard to impress. Prefers raw clinical data."
    }
    history = mock_db.get(hcpName, "No prior interaction history found for this HCP in the database.")
    
    return {
        "action": "MESSAGE_ONLY",
        "data": history
    }

@tool
def suggest_materials_tool(topic: str) -> dict:
    """
    TOOL 4: Use this tool to find relevant brochures, PDFs, or samples based on the topic discussed.
    """
    print(f"\n--- TOOL TRIGGERED: suggest_materials_tool for {topic} ---")
    # Mock product catalog
    topic = topic.lower()
    suggestions = []
    if "onco" in topic or "cancer" in topic or "tumor" in topic:
        suggestions = ["OncoBoost Phase III PDF", "OncoBoost Dosage Guide"]
    elif "cardio" in topic or "heart" in topic:
        suggestions = ["CardioPlus Efficacy Report", "HeartHealth Patient Sample"]
    elif "trial" in topic or "clinical" in topic:
        suggestions = ["Latest Clinical Trial Summary PDF"]
    else:
        suggestions = ["General Product Catalog 2024"]
        
    return {
        "action": "UPDATE",
        "data": {
            "materialsShared": suggestions
        }
    }

@tool
def generate_follow_ups_tool(sentiment: str, topics: str) -> dict:
    """
    TOOL 5: Use this tool at the end of logging an interaction to automatically generate appropriate follow-up actions.
    """
    print(f"\n--- TOOL TRIGGERED: generate_follow_ups_tool ---")
    actions = ["Log interaction in main CRM database"]
    
    if sentiment.lower() == "positive":
        actions.append(f"Send detailed technical specs regarding {topics}")
        actions.append("Schedule follow-up meeting in 2 weeks")
    elif sentiment.lower() == "negative":
        actions.append("Follow up with Medical Science Liaison (MSL) to address concerns")
    else:
        actions.append("Send generic thank you email")
        
    return {
        "action": "UPDATE",
        "data": {
            "followUpActions": actions
        }
    }


# --- 3. Initialize the AI Agent ---
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# The agent's complete toolbelt
tools = [
    log_interaction_tool, 
    edit_interaction_tool, 
    fetch_hcp_history_tool, 
    suggest_materials_tool, 
    generate_follow_ups_tool
]
agent_executor = create_react_agent(llm, tools)


# --- 4. The API Endpoint ---
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # --- NEW: GET CURRENT DATE AND TIME ---
    today_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")


    # Tell the AI who it is, what time it is, and what the current form looks like
    system_prompt = f"""
    You are an expert AI CRM assistant for Pharma reps. 
    IMPORTANT CONTEXT: Today's date is {today_date} and the current time is {current_time}.
    If the user says "today", use exactly {today_date}. If they don't specify a time, default to {current_time}.
    
    Current form state: {request.formState.model_dump()}
    Always use your tools to update the form when the user provides interaction details.
    
    CRITICAL RULES FOR YOUR CHAT RESPONSES:
    1. Be highly conversational, warm, and extremely brief.
    2. NEVER output raw JSON, dictionaries, or the raw "form state".
    3. DO NOT act like a robot reading a data log. NEVER repeat the exact time (like "14:44") or date back to the user unless they explicitly ask what time it is. 
    4. Example of a good response: "Got it! I've logged your positive meeting with Dr. Sharma regarding the OncoBoost trials."
    """

    # Run the LangGraph Agent
    response = agent_executor.invoke({
        "messages": [
            ("system", system_prompt),
            ("user", request.message)
        ]
    })

    # Get the AI's conversational text response
    ai_message = response["messages"][-1].content
    updated_state = None

    # Check the agent's thought process to see if it used a tool to update the form
    for msg in reversed(response["messages"]):
        if msg.type == "tool":
            try:
                tool_result = json.loads(msg.content)
                current_dict = request.formState.model_dump()
                
                # If the tool wants to update the form, apply the changes
                if tool_result.get("action") in ["UPDATE", "OVERWRITE"]:
                    current_dict.update(tool_result.get("data", {}))
                    updated_state = current_dict
                    
                break # We only need the most recent tool action
            except Exception as e:
                print("Tool processing error:", e)

    # --- 5. SAVE TO POSTGRESQL DATABASE ---
    # Only save to DB if the AI actually updated the form with new data
    if updated_state:
        try:
            db = SessionLocal()
            db_log = InteractionLog(
                hcp_name=updated_state.get("hcpName", ""),
                date=updated_state.get("date", ""),
                sentiment=updated_state.get("sentiment", ""),
                topics=updated_state.get("topicsDiscussed", ""),
                materials=json.dumps(updated_state.get("materialsShared", [])),
                follow_ups=json.dumps(updated_state.get("followUpActions", []))
            )
            db.add(db_log)
            db.commit()
            db.close()
            print("Successfully saved interaction to database!")
        except Exception as db_error:
            print(f"Database Error: {db_error}")

    return {
        "ai_message": ai_message,
        "updated_form_state": updated_state
    }