"""
FastAPI application for AfiAgent.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse
import asyncio
from typing import AsyncGenerator, Dict, List, Any

from src.graph import build_graph
from src.config import TEAM_MEMBERS
from src.service.workflow_service import run_agent_workflow

# Configure logging
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AfiAgent API",
    description="API for AfiAgent LangGraph-based agent workflow",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create the graph
graph = build_graph()


class ContentItem(BaseModel):
    type: str = Field(..., description="The type of content (text, image, etc.)")
    text: Optional[str] = Field(None, description="The text content if type is 'text'")
    image_url: Optional[str] = Field(
        None, description="The image URL if type is 'image'"
    )


class ChatMessage(BaseModel):
    role: str = Field(
        ..., description="The role of the message sender (user or assistant)"
    )
    content: Union[str, List[ContentItem]] = Field(
        ...,
        description="The content of the message, either a string or a list of content items",
    )


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="The conversation history")
    debug: Optional[bool] = Field(False, description="Whether to enable debug logging")
    deep_thinking_mode: Optional[bool] = Field(
        False, description="Whether to enable deep thinking mode"
    )
    search_before_planning: Optional[bool] = Field(
        False, description="Whether to search before planning"
    )


@app.post("/api/chat/stream")
async def chat_endpoint(request: ChatRequest, req: Request):
    """
    Chat endpoint for LangGraph invoke.

    Args:
        request: The chat request
        req: The FastAPI request object for connection state checking

    Returns:
        The streamed response
    """
    try:
        # Convert Pydantic models to dictionaries and normalize content format
        messages = []
        for msg in request.messages:
            message_dict = {"role": msg.role}

            # Handle both string content and list of content items
            if isinstance(msg.content, str):
                message_dict["content"] = msg.content
            else:
                # For content as a list, convert to the format expected by the workflow
                content_items = []
                for item in msg.content:
                    if item.type == "text" and item.text:
                        content_items.append({"type": "text", "text": item.text})
                    elif item.type == "image" and item.image_url:
                        content_items.append(
                            {"type": "image", "image_url": item.image_url}
                        )

                message_dict["content"] = content_items

            messages.append(message_dict)

        async def event_generator():
            try:
                async for event in run_agent_workflow(
                    messages,
                    request.debug,
                    request.deep_thinking_mode,
                    request.search_before_planning,
                ):
                    # Check if client is still connected
                    if await req.is_disconnected():
                        logger.info("Client disconnected, stopping workflow")
                        break
                    yield {
                        "event": event["event"],
                        "data": json.dumps(event["data"], ensure_ascii=False),
                    }
            except asyncio.CancelledError:
                logger.info("Stream processing cancelled")
                raise
        
        # async def event_generator() -> AsyncGenerator[Dict[str, Any], None]:
        #     try:
        #         logger.info("🌐 Starting event stream")
        #         yield {"event": "ping", "data": "🔌 Connected to stream."}

        #         async for event in run_agent_workflow(
        #             messages,
        #             request.debug,
        #             request.deep_thinking_mode,
        #             request.search_before_planning,
        #         ):
        #             if await req.is_disconnected():
        #                 logger.warning("⚠️ Client disconnected, stopping stream.")
        #                 break

        #             yield {
        #                 "event": event.get("event", "message"),
        #                 "data": json.dumps(event["data"], ensure_ascii=False),
        #             }

        #         logger.info("✅ Stream finished successfully.")
        #     except asyncio.CancelledError:
        #         logger.warning("🛑 Stream cancelled by client.")
        #     except Exception as e:
        #         logger.error(f"🔥 Unexpected error in stream: {e}", exc_info=True)
        #         yield {"event": "error", "data": f"Internal error: {str(e)}"}


        return EventSourceResponse(
            event_generator(),
            media_type="text/event-stream",
            sep="\n",
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Code Server endpoints
from src.tools.code_server_manager import code_server_manager, collect_generated_code, package_code_for_delivery

@app.get("/api/code-server/status")
async def get_code_server_status():
    """Get the current status of Code Server."""
    try:
        from src.tools.code_server_manager import get_code_server_status
        status = get_code_server_status()
        return status
    except Exception as e:
        logger.error(f"Error getting Code Server status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/code-server/start")
async def start_code_server():
    """Start Code Server."""
    try:
        from src.tools.code_server_manager import ensure_code_server_running
        success = ensure_code_server_running()
        if success:
            status = code_server_manager.get_status()
            return {"message": "Code Server started successfully", "status": status}
        else:
            raise HTTPException(status_code=500, detail="Failed to start Code Server")
    except Exception as e:
        logger.error(f"Error starting Code Server: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/code-server/stop")
async def stop_code_server():
    """Stop Code Server."""
    try:
        success = code_server_manager.stop()
        if success:
            return {"message": "Code Server stopped successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to stop Code Server")
    except Exception as e:
        logger.error(f"Error stopping Code Server: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/code-server/files")
async def list_workspace_files():
    """List all files in the Code Server workspace."""
    try:
        files = code_server_manager.get_workspace_files()
        return {"files": files, "count": len(files)}
    except Exception as e:
        logger.error(f"Error listing workspace files: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/code-server/files/{filename:path}")
async def get_file_content(filename: str):
    """Get content of a specific file from the workspace."""
    try:
        content = code_server_manager.read_file(filename)
        if content is not None:
            return {"filename": filename, "content": content}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/code-server/collect")
async def collect_code():
    """Collect all generated code files from the workspace."""
    try:
        files = collect_generated_code()
        package = package_code_for_delivery(files)
        return package
    except Exception as e:
        logger.error(f"Error collecting code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/code-server/cleanup")
async def cleanup_workspace():
    """Clean up the Code Server workspace."""
    try:
        success = code_server_manager.cleanup_workspace()
        if success:
            return {"message": "Workspace cleaned up successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clean up workspace")
    except Exception as e:
        logger.error(f"Error cleaning up workspace: {e}")
        raise HTTPException(status_code=500, detail=str(e))


