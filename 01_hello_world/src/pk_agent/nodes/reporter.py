"""
Reporter node: produces a short executive summary.
"""
from langchain_core.messages import HumanMessage, SystemMessage
from ..llm.provider import get_llm
from ..prompts.reporter import REPORTER_SYSTEM_PROMPT
from ..schemas.state import AgentState

# define key function for the reporter node
def write_report(state: AgentState) -> dict:
    """Read state.extracted_parameters and write the executive summary."""

    # defensive check to ensure the extracted parameters are there
    if state.extracted_parameters is None:
        raise ValueError(
            "Reporter was invoked but extracted_parameters is None. "
            "Check the node order in graph/builder.py."
        )

    # extract parameters
    p = state.extracted_parameters

    # construct the user_message content based on the extracted parameters
    # which will be passed to the LLM as input
    user_content = (
        f"Please write the executive summary for the following model:\n"
        f"- Drug: {p.drug_name}\n"
        f"- Volume of distribution V: {p.volume_of_distribution} L\n"
        f"- Clearance CL: {p.clearance} L/h"
    )

    # get llm instance with slightly higher temperature
    llm = get_llm(temperature=0.2)

    # invoke the model with the system prompt and the user message as input
    response = llm.invoke(
        [
            SystemMessage(content=REPORTER_SYSTEM_PROMPT),
            HumanMessage(content=user_content),
        ]
    )

    # return dict with the updated field
    # which gets merged back into the state by LangGraph
    return {"report": response.content}