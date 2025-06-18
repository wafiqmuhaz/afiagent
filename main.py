"""
Entry point script for the LangGraph Demo.
"""

import argparse
from src.workflow import run_agent_workflow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the LangGraph Demo agent workflow.")
    parser.add_argument("query", nargs="*", help="The user's query or request.")
    parser.add_argument("--local", action="store_true", help="Use local model for lightweight tasks.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")

    args = parser.parse_args()

    if args.query:
        user_query = " ".join(args.query)
    else:
        user_query = input("Enter your query: ")

    result = run_agent_workflow(user_input=user_query, debug=args.debug, use_local_model_for_lightweight_tasks=args.local)

    # Print the conversation history
    print("\n=== Conversation History ===")
    for message in result["messages"]:
        role = message["role"]
        print(f"\n[{role.upper()}]: {message["content"]}")

