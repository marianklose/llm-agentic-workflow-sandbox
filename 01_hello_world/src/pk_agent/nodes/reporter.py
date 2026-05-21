"""
Reporter node: produces a short executive summary.
"""
from langchain_core.messages import HumanMessage, SystemMessage

from ..llm.provider import get_llm
from ..prompts.reporter import REPORTER_SYSTEM_PROMPT
from ..schemas.state import AgentState


def write_report(state: AgentState) -> dict:
    """Read state.extracted_parameters and write the executive summary."""

    # Defensive check. With the current graph topology this branch
    # cannot be reached, but if someone reorders nodes later the error
    # message will point them straight at the cause.
    if state.extracted_parameters is None:
        raise ValueError(
            "Reporter was invoked but extracted_parameters is None. "
            "Check the node order in graph/builder.py."
        )

    p = state.extracted_parameters
    user_content = (
        f"Please write the executive summary for the following model:\n"
        f"- Drug: {p.drug_name}\n"
        f"- Volume of distribution V: {p.volume_of_distribution} L\n"
        f"- Clearance CL: {p.clearance} L/h"
    )

    # Slightly higher temperature for prose. The extractor needs 0.0
    # for deterministic structured output; here a small amount of
    # variation produces more natural writing.
    llm = get_llm(temperature=0.2)
    response = llm.invoke(
        [
            SystemMessage(content=REPORTER_SYSTEM_PROMPT),
            HumanMessage(content=user_content),
        ]
    )

    return {"report": response.content}