"""
Extractor node: extracts PK parameters from the paper text.

In LangGraph, a node is simply a function with the signature:
    state -> dict of updates

It receives the current state (a Pydantic instance) and returns a
dictionary containing only the fields it wants to update. LangGraph
handles merging the update back into the state.
"""
from langchain_core.messages import HumanMessage, SystemMessage

from ..llm.provider import get_llm
from ..prompts.extractor import EXTRACTOR_SYSTEM_PROMPT
from ..schemas.pk_model import PKParameters
from ..schemas.state import AgentState


def extract_parameters(state: AgentState) -> dict:
    """Read state.paper_content and extract PK parameters from it."""

    # .with_structured_output(PKParameters) tells the LLM that its
    # response must conform to the PKParameters schema. LangChain
    # translates the schema into the provider's tool-calling format,
    # invokes the model, and parses the response back into a
    # PKParameters instance. Validation errors are raised here, not
    # silently passed downstream.
    llm = get_llm().with_structured_output(PKParameters)

    response: PKParameters = llm.invoke(
        [
            SystemMessage(content=EXTRACTOR_SYSTEM_PROMPT),
            HumanMessage(content=state.paper_content),
        ]
    )

    # Return only the field we want to update. LangGraph merges this
    # with the existing state — we never mutate the input state object
    # directly. Treating nodes as pure functions makes them easy to
    # test and reason about.
    return {"extracted_parameters": response}