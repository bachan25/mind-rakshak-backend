from fastapi import APIRouter, HTTPException, Request, Header
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Dict, Any, Optional
import json
from agent import mind_rakshak_agent

router = APIRouter()

def stream_graph_updates(user_input: str, config: Dict[str, Any]):
    user_id = config["configurable"].get("user_id")
    user_input += f" (User ID: {user_id})" if user_id else ""
    events = mind_rakshak_agent.graph.stream(
        {"messages": [{"role": "user", "content": user_input}], "user_id": user_id},
        config,
        stream_mode="values",
    )
   
    for event in events:
        yield json.dumps(event["messages"][-1].dict()) + "\n"


@router.post("/stream")
async def chat_stream(
    request: Request,
    user_id: Optional[str] = Header(None, alias="user_id") 
):
    body = await request.json()
    user_input = body.get("user_input", "")
    thread_id = body.get("thread_id", "1")

    config = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user_id  # 👈 pass to agent
        }
    }

    return StreamingResponse(
        stream_graph_updates(user_input, config),
        media_type="application/json"
    )


@router.post("/invoke")
async def chat_invoke(
    request: Request,
    user_id: Optional[str] = Header(None, alias="user_id") 
):
    body = await request.json()
    user_input = body.get("user_input", "")
    thread_id = body.get("thread_id", "1")

    config = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user_id  # 👈 pass to agent
        }
    }

    user_input += f" (User ID: {user_id})" if user_id else ""
    events = mind_rakshak_agent.graph.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
    )
    return JSONResponse(events)
