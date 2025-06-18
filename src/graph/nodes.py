# import logging
# import json
# from copy import deepcopy
# from typing import Literal
# from langchain_core.messages import HumanMessage
# from langgraph.types import Command
# from langgraph.graph import END

# from src.agents import research_agent, coder_agent, browser_agent
# from src.agents.llm import get_llm_by_type
# from src.config import TEAM_MEMBERS
# from src.config.agents import AGENT_LLM_MAP
# from src.prompts.template import apply_prompt_template
# from src.tools.search import tavily_tool
# from .types import State, Router

# logger = logging.getLogger(__name__)

# RESPONSE_FORMAT = "Response from {}:\n\n<response>\n{}\n</response>\n\n*Please execute the next step.*"


# def research_node(state: State) -> Command[Literal["supervisor"]]:
#     """Node for the researcher agent that performs research tasks."""
#     logger.info("Research agent starting task")
#     result = research_agent.invoke(state)
#     logger.info("Research agent completed task")
#     logger.debug(f"Research agent response: {result["messages"][-1].content}")
#     return Command(
#         update={
#             "messages": [
#                 HumanMessage(
#                     content=RESPONSE_FORMAT.format(
#                         "researcher", result["messages"][-1].content
#                     ),
#                     name="researcher",
#                 )
#             ]
#         },
#         goto="supervisor",
#     )


# def code_node(state: State) -> Command[Literal["supervisor"]]:
#     """Node for the coder agent that executes Python code."""
#     logger.info("Code agent starting task")
#     result = coder_agent.invoke(state)
#     logger.info("Code agent completed task")
#     logger.debug(f"Code agent response: {result["messages"][-1].content}")
#     return Command(
#         update={
#             "messages": [
#                 HumanMessage(
#                     content=RESPONSE_FORMAT.format(
#                         "coder", result["messages"][-1].content
#                     ),
#                     name="coder",
#                 )
#             ]
#         },
#         goto="supervisor",
#     )


# # def browser_node(state: State) -> Command[Literal["supervisor"]]:
# #     """Node for the browser agent that performs web browsing tasks."""
# #     logger.info("Browser agent starting task")
# #     result = browser_agent.invoke(state)
# #     logger.info("Browser agent completed task")
# #     logger.debug(f"Browser agent response: {result["messages"][-1].content}")
# #     return Command(
# #         update={
# #             "messages": [
# #                 HumanMessage(
# #                     content=RESPONSE_FORMAT.format(
# #                         "browser", result["messages"][-1].content
# #                     ),
# #                     name="browser",
# #                 )
# #             ]
# #         },
# #         goto="supervisor",
# #     )
# # 
# # 
# # 
# # def browser_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
# #     """Node for the browser agent that performs web browsing tasks."""
# #     logger.info("Browser agent starting task")
# #     result = browser_agent.invoke(state)
# #     logger.info("Browser agent completed task")

# #     content = result["messages"][-1].content
# #     logger.debug(f"Browser agent response: {content}")

# #     # Check if result indicates completion
# #     is_done = "✅ Task completed" in content or "done" in content.lower()
# #     goto = "__end__" if is_done else "supervisor"

# #     return Command(
# #         update={
# #             "messages": [
# #                 HumanMessage(
# #                     content=RESPONSE_FORMAT.format("browser", content),
# #                     name="browser",
# #                 )
# #             ]
# #         },
# #         goto=goto,
# #     )
# def browser_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
#     logger.info("Browser agent starting task")
#     result = browser_agent.invoke(state)
#     logger.info("Browser agent completed task")

#     content = result["messages"][-1].content
#     logger.debug(f"Browser agent response: {content}")

#     # Deteksi selesai
#     is_done = "✅ Task completed" in content or '"done"' in content.lower()

#     # Update state dengan flag done
#     updates = {
#         "messages": [
#             HumanMessage(
#                 content=RESPONSE_FORMAT.format("browser", content),
#                 name="browser",
#             )
#         ]
#     }
#     if is_done:
#         updates["browser_done"] = True

#     return Command(
#         update=updates,
#         goto="supervisor",  # Biarkan supervisor memutuskan end
#     )



# # def supervisor_node(state: State) -> Command[Literal[*TEAM_MEMBERS, "__end__"]]:
# #     """Supervisor node that decides which agent should act next."""
# #     logger.info("Supervisor evaluating next action")
# #     messages = apply_prompt_template("supervisor", state)
# #     response = (
# #         get_llm_by_type(AGENT_LLM_MAP["supervisor"])
# #         .with_structured_output(Router)
# #         .invoke(messages)
# #     )
# #     goto = response.next
# #     logger.debug(f"Current state messages: {state["messages"]}")
# #     logger.debug(f"Supervisor response: {response}")

# #     if goto == "FINISH":
# #         goto = "__end__"
# #         logger.info("Workflow completed")
# #     else:
# #         logger.info(f"Supervisor delegating to: {goto}")

# #     return Command(goto=goto, update={"next": goto})

# def supervisor_node(state: State) -> Command[Literal[*TEAM_MEMBERS, "__end__"]]:
#     logger.info("Supervisor evaluating next action")
#     messages = apply_prompt_template("supervisor", state)
#     response = (
#         get_llm_by_type(AGENT_LLM_MAP["supervisor"])
#         .with_structured_output(Router)
#         .invoke(messages)
#     )
#     goto = response.next
#     logger.debug(f"Current state messages: {state['messages']}")
#     logger.debug(f"Supervisor response: {response}")

#     # Jangan ulangi browser jika sudah selesai
#     if goto == "browser" and state.get("browser_done"):
#         logger.info("Browser already completed. Finishing workflow.")
#         goto = "__end__"

#     if goto == "FINISH":
#         goto = "__end__"
#         logger.info("Workflow completed")
#     else:
#         logger.info(f"Supervisor delegating to: {goto}")

#     return Command(goto=goto, update={"next": goto})


# # def planner_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
# #     """Planner node that generate the full plan."""
# #     logger.info("Planner generating full plan")
# #     messages = apply_prompt_template("planner", state)
# #     # whether to enable deep thinking mode
# #     llm = get_llm_by_type("basic")
# #     if state.get("deep_thinking_mode"):
# #         llm = get_llm_by_type("reasoning")
# #     if state.get("search_before_planning"):
# #         searched_content = tavily_tool.invoke({"query": state["messages"][-1].content})
# #         messages = deepcopy(messages)
# #         messages[
# #             -1
# #         ].content += f"\n\n# Relative Search Results\n\n{json.dumps([{"titile": elem["title"], "content": elem["content"]} for elem in searched_content], ensure_ascii=False)}"
# #     stream = llm.stream(messages)
# #     full_response = ""
# #     for chunk in stream:
# #         full_response += chunk.content
# #     logger.debug(f"Current state messages: {state["messages"]}")
# #     logger.debug(f"Planner response: {full_response}")

# #     if full_response.startswith("```json"):
# #         full_response = full_response.removeprefix("```json")

# #     if full_response.endswith("```"):
# #         full_response = full_response.removesuffix("```")

# #     goto = "supervisor"
# #     try:
# #         json.loads(full_response)
# #     except json.JSONDecodeError:
# #         logger.warning("Planner response is not a valid JSON")
# #         goto = "__end__"

# #     return Command(
# #         update={
# #             "messages": [HumanMessage(content=full_response, name="planner")],
# #             "full_plan": full_response,
# #         },
# #         goto=goto,
# #     )

# def planner_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
#     logger.info("Planner generating full plan")

#     # Step 1: Generate messages from prompt template
#     messages = apply_prompt_template("planner", state)
#     llm = get_llm_by_type("basic")
#     if state.get("deep_thinking_mode"):
#         llm = get_llm_by_type("reasoning")

#     # Step 2: Normalize last user message (important fix!)
#     user_msg = messages[-1]
#     if isinstance(user_msg.content, list):
#         # If user content is a list (multimodal), combine texts
#         combined_text = "\n".join(
#             item.get("text", "") for item in user_msg.content if isinstance(item, dict)
#         )
#         user_msg.content = combined_text

#     if not isinstance(user_msg.content, str):
#         logger.warning(f"Planner: Unexpected user message format: {user_msg.content}")
#         user_msg.content = str(user_msg.content)

#     # Step 3: Optionally append search result
#     if state.get("search_before_planning"):
#         searched_content = tavily_tool.invoke({"query": user_msg.content})
#         messages = deepcopy(messages)

#         try:
#             search_snippets = [
#                 {
#                     "title": elem.get("title", ""),
#                     "content": elem.get("content", ""),
#                 }
#                 for elem in searched_content
#                 if isinstance(elem, dict)
#             ]
#             relative_text = json.dumps(search_snippets, ensure_ascii=False, indent=2)
#             messages[-1].content += f"\n\n# Relative Search Results\n\n{relative_text}"
#         except Exception as e:
#             logger.error(f"Failed to attach search results: {e}")

#     # Step 4: Call LLM planner
#     stream = llm.stream(messages)
#     full_response = ""
#     for chunk in stream:
#         full_response += chunk.content

#     logger.debug(f"Current state messages: {state['messages']}")
#     logger.debug(f"Planner response: {full_response}")

#     # Step 5: Clean JSON code block
#     if full_response.startswith("```json"):
#         full_response = full_response.removeprefix("```json")
#     if full_response.endswith("```"):
#         full_response = full_response.removesuffix("```")

#     # Step 6: Validate JSON
#     goto = "supervisor"
#     try:
#         json.loads(full_response)
#     except json.JSONDecodeError:
#         logger.warning("Planner response is not a valid JSON")
#         goto = "__end__"

#     # Step 7: Return updated state
#     return Command(
#         update={
#             "messages": [HumanMessage(content=full_response, name="planner")],
#             "full_plan": full_response,
#         },
#         goto=goto,
#     )


# def coordinator_node(state: State) -> Command[Literal["planner", "__end__"]]:
#     """Coordinator node that communicate with customers."""
#     logger.info("Coordinator talking.")
#     messages = apply_prompt_template("coordinator", state)
#     response = get_llm_by_type(AGENT_LLM_MAP["coordinator"]).invoke(messages)
#     logger.debug(f"Current state messages: {state["messages"]}")
#     logger.debug(f"reporter response: {response}")

#     goto = "__end__"
#     if "handoff_to_planner" in response.content:
#         goto = "planner"

#     return Command(
#         goto=goto,
#     )


# def reporter_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
#     """Reporter node that write a final report."""
#     logger.info("Reporter write final report")
#     messages = apply_prompt_template("reporter", state)
#     response = get_llm_by_type(AGENT_LLM_MAP["reporter"]).invoke(messages)
#     logger.debug(f"Current state messages: {state["messages"]}")
#     logger.debug(f"reporter response: {response}")

#     return Command(
#         update={
#             "messages": [
#                 HumanMessage(
#                     content=RESPONSE_FORMAT.format("reporter", response.content),
#                     name="reporter",
#                 )
#             ]
#         },
#         goto="supervisor",
#     )


# ///////////////////////////////////////////////////////////////////////////NODE BARU 


import logging
import json
from copy import deepcopy
from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import END

from src.agents import research_agent, coder_agent, browser_agent
from src.agents.llm import get_llm_by_type
from src.config import TEAM_MEMBERS
from src.config.agents import AGENT_LLM_MAP
from src.prompts.template import apply_prompt_template
from src.tools.search import tavily_tool
from .types import State, Router

logger = logging.getLogger(__name__)

RESPONSE_FORMAT = "Response from {}:\n\n<response>\n{}\n</response>\n\n*Please execute the next step.*"


def research_node(state: State) -> Command[Literal["supervisor"]]:
    logger.info("Research agent starting task")
    result = research_agent.invoke(state)
    logger.info("Research agent completed task")
    logger.debug(f"Research agent response: {result['messages'][-1].content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format("researcher", result["messages"][-1].content),
                    name="researcher",
                )
            ]
        },
        goto="supervisor",
    )


def code_node(state: State) -> Command[Literal["supervisor"]]:
    logger.info("Code agent starting task")
    result = coder_agent.invoke(state)
    logger.info("Code agent completed task")
    logger.debug(f"Code agent response: {result['messages'][-1].content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format("coder", result["messages"][-1].content),
                    name="coder",
                )
            ]
        },
        goto="supervisor",
    )


def browser_node(state: State) -> Command[Literal["supervisor"]]:
    logger.info("Browser agent starting task")
    result = browser_agent.invoke(state)
    logger.info("Browser agent completed task")

    content = result["messages"][-1].content
    logger.debug(f"Browser agent response: {content}")

    updates = {
        "messages": [
            HumanMessage(
                content=RESPONSE_FORMAT.format("browser", content),
                name="browser",
            )
        ]
    }

    updates["current_task_index"] = state.get("current_task_index", 0) + 1

    return Command(update=updates, goto="supervisor")


def supervisor_node(state: State) -> Command[Literal[*TEAM_MEMBERS, "__end__"]]:
    logger.info("Supervisor evaluating next action")

    plan = state.get("full_plan", {})
    steps = plan.get("steps", [])
    index = state.get("current_step_index", 0)

    if not steps or index >= len(steps):
        logger.info("All steps completed. Ending workflow.")
        return Command(goto="__end__")

    current_step = steps[index]
    agent = current_step.get("agent_name", "").strip()

    # Browser should not be reused
    if agent == "browser" and state.get("browser_done"):
        logger.info("Skipping already completed browser task.")
        return Command(goto="__end__")

    logger.info(f"Delegating to agent: {agent} (Step {index + 1}/{len(steps)})")
    return Command(
        update={"next": agent, "current_step_index": index + 1},
        goto=agent,
    )



def planner_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
    logger.info("Planner generating full plan")

    messages = apply_prompt_template("planner", state)
    llm = get_llm_by_type("reasoning" if state.get("deep_thinking_mode") else "basic")

    user_msg = messages[-1]
    if isinstance(user_msg.content, list):
        combined_text = "\n".join(
            item.get("text", "") for item in user_msg.content if isinstance(item, dict)
        )
        user_msg.content = combined_text
    if not isinstance(user_msg.content, str):
        user_msg.content = str(user_msg.content)

    if state.get("search_before_planning"):
        searched_content = tavily_tool.invoke({"query": user_msg.content})
        messages = deepcopy(messages)
        try:
            search_snippets = [
                {
                    "title": elem.get("title", ""),
                    "content": elem.get("content", ""),
                }
                for elem in searched_content if isinstance(elem, dict)
            ]
            relative_text = json.dumps(search_snippets, ensure_ascii=False, indent=2)
            messages[-1].content += f"\n\n# Relative Search Results\n\n{relative_text}"
        except Exception as e:
            logger.error(f"Failed to attach search results: {e}")

    # Run the LLM
    full_response = "".join([chunk.content for chunk in llm.stream(messages)]).strip()
    logger.debug(f"Planner raw response: {full_response}")

    # Clean up code block
    if full_response.startswith("```json"):
        full_response = full_response.removeprefix("```json")
    if full_response.endswith("```"):
        full_response = full_response.removesuffix("```")

    # Parse the plan
    try:
        parsed_plan = json.loads(full_response)
        steps = parsed_plan.get("steps", [])
        if not isinstance(steps, list) or not all("agent_name" in step for step in steps):
            raise ValueError("Planner response is not a valid list of subtasks")
    except Exception as e:
        logger.warning(f"Planner response invalid: {e}")
        return Command(goto="__end__", update={"messages": [HumanMessage(content="Failed to generate valid plan.", name="planner")]})

    logger.info("Planner created a valid plan")
    return Command(
        update={
            "messages": [HumanMessage(content=full_response, name="planner")],
            "full_plan": parsed_plan,
            "current_step_index": 0,
            "browser_done": False,  # reset any lingering state
        },
        goto="supervisor",
    )



def coordinator_node(state: State) -> Command[Literal["planner", "__end__"]]:
    logger.info("Coordinator talking.")
    messages = apply_prompt_template("coordinator", state)
    response = get_llm_by_type(AGENT_LLM_MAP["coordinator"]).invoke(messages)
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"reporter response: {response}")

    goto = "__end__"
    if "handoff_to_planner" in response.content:
        goto = "planner"

    return Command(goto=goto)


def reporter_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
    logger.info("Reporter write final report")
    messages = apply_prompt_template("reporter", state)
    response = get_llm_by_type(AGENT_LLM_MAP["reporter"]).invoke(messages)
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"reporter response: {response}")

    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=RESPONSE_FORMAT.format("reporter", response.content),
                    name="reporter",
                )
            ]
        },
        goto="supervisor",
    )
