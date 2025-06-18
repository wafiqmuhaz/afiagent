import logging
from src.config import TEAM_MEMBERS
from src.graph import build_graph
from src.crawler.llm_client import LLMClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default level is INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def enable_debug_logging():
    """Enable debug level logging for more detailed execution information."""
    logging.getLogger("src").setLevel(logging.DEBUG)


logger = logging.getLogger(__name__)

# Create the graph
graph = build_graph()


def run_agent_workflow(user_input: str, debug: bool = False, use_local_model_for_lightweight_tasks: bool = False):
    """
    Run the agent workflow with the given user input.

    Args:
        user_input: The user's query or request
        debug: If True, enables debug level logging
        use_local_model_for_lightweight_tasks: If True, routes selected lightweight tasks to the local model.

    Returns:
        The final state after the workflow completes
    """
    if not user_input:
        raise ValueError("Input could not be empty")

    if debug:
        enable_debug_logging()

    logger.info(f"Starting workflow with user input: {user_input}")

    if use_local_model_for_lightweight_tasks:
        logger.info("Routing lightweight tasks to local model.")
        llm_client = LLMClient()
        response_content = llm_client.generate_response(user_input, use_local_model=True)
        result = {"messages": [{"role": "assistant", "content": response_content}]}
    else:
        result = graph.invoke(
            {
                # Constants
                "TEAM_MEMBERS": TEAM_MEMBERS,
                # Runtime Variables
                "messages": [{"role": "user", "content": user_input}],
                "deep_thinking_mode": True,
                "search_before_planning": True,
            },
            config={"recursion_limit": 100} # Increase recursion limit
        )
    logger.debug(f"Final workflow state: {result}")
    logger.info("Workflow completed successfully")
    return result


if __name__ == "__main__":
    print(graph.get_graph().draw_mermaid())

