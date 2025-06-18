"""
Code Server Tool for Afiagent Agents

This tool provides Code Server functionality for the Afiagent multi-agent system.
"""

from langchain_core.tools import tool
from typing import Dict, Any, Optional
import logging

from .code_server_manager import (
    code_server_manager,
    detect_code_request,
    ensure_code_server_running,
    get_code_server_status,
    collect_generated_code,
    package_code_for_delivery
)

logger = logging.getLogger(__name__)


@tool
def start_code_server() -> str:
    """
    Start Code Server for web-based code editing and execution.
    
    Returns:
        str: Status message indicating success or failure
    """
    try:
        if code_server_manager.start():
            status = get_code_server_status()
            return f"Code Server started successfully on {status['url']}"
        else:
            return "Failed to start Code Server"
    except Exception as e:
        logger.error(f"Error starting Code Server: {e}")
        return f"Error starting Code Server: {str(e)}"


@tool
def stop_code_server() -> str:
    """
    Stop the running Code Server instance.
    
    Returns:
        str: Status message indicating success or failure
    """
    try:
        if code_server_manager.stop():
            return "Code Server stopped successfully"
        else:
            return "Failed to stop Code Server"
    except Exception as e:
        logger.error(f"Error stopping Code Server: {e}")
        return f"Error stopping Code Server: {str(e)}"


@tool
def check_code_server_status() -> str:
    """
    Check the current status of Code Server.
    
    Returns:
        str: JSON string containing Code Server status information
    """
    try:
        status = get_code_server_status()
        import json
        return json.dumps(status, indent=2)
    except Exception as e:
        logger.error(f"Error checking Code Server status: {e}")
        return f"Error checking status: {str(e)}"


@tool
def write_code_file(filename: str, content: str) -> str:
    """
    Write code content to a file in the Code Server workspace.
    
    Args:
        filename: Name of the file to create (can include subdirectories)
        content: Code content to write to the file
        
    Returns:
        str: Success or error message
    """
    try:
        # Ensure Code Server is running
        if not ensure_code_server_running():
            return "Failed to ensure Code Server is running"
        
        if code_server_manager.write_file(filename, content):
            return f"Successfully wrote code to {filename}"
        else:
            return f"Failed to write code to {filename}"
    except Exception as e:
        logger.error(f"Error writing code file: {e}")
        return f"Error writing code file: {str(e)}"


@tool
def read_code_file(filename: str) -> str:
    """
    Read code content from a file in the Code Server workspace.
    
    Args:
        filename: Name of the file to read
        
    Returns:
        str: File content or error message
    """
    try:
        content = code_server_manager.read_file(filename)
        if content is not None:
            return content
        else:
            return f"File {filename} not found or could not be read"
    except Exception as e:
        logger.error(f"Error reading code file: {e}")
        return f"Error reading code file: {str(e)}"


@tool
def list_workspace_files() -> str:
    """
    List all files in the Code Server workspace.
    
    Returns:
        str: JSON string containing list of files
    """
    try:
        files = code_server_manager.get_workspace_files()
        import json
        return json.dumps({"files": files, "count": len(files)}, indent=2)
    except Exception as e:
        logger.error(f"Error listing workspace files: {e}")
        return f"Error listing files: {str(e)}"


@tool
def collect_all_code() -> str:
    """
    Collect all generated code files from the Code Server workspace.
    
    Returns:
        str: JSON string containing all code files and their content
    """
    try:
        files = collect_generated_code()
        package = package_code_for_delivery(files)
        import json
        return json.dumps(package, indent=2)
    except Exception as e:
        logger.error(f"Error collecting code: {e}")
        return f"Error collecting code: {str(e)}"


@tool
def cleanup_workspace() -> str:
    """
    Clean up the Code Server workspace by removing all files.
    
    Returns:
        str: Success or error message
    """
    try:
        if code_server_manager.cleanup_workspace():
            return "Workspace cleaned up successfully"
        else:
            return "Failed to clean up workspace"
    except Exception as e:
        logger.error(f"Error cleaning up workspace: {e}")
        return f"Error cleaning up workspace: {str(e)}"


@tool
def detect_code_task(user_message: str) -> str:
    """
    Detect if a user message is requesting a code-related task.
    
    Args:
        user_message: The user's message to analyze
        
    Returns:
        str: "true" if code-related, "false" otherwise
    """
    try:
        is_code_request = detect_code_request(user_message)
        return "true" if is_code_request else "false"
    except Exception as e:
        logger.error(f"Error detecting code task: {e}")
        return "false"


# Export tools for use in agents
CODE_SERVER_TOOLS = [
    start_code_server,
    stop_code_server,
    check_code_server_status,
    write_code_file,
    read_code_file,
    list_workspace_files,
    collect_all_code,
    cleanup_workspace,
    detect_code_task
]

