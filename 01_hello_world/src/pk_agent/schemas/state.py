"""
Graph state: the data pipeline between nodes. A shared whiteboard
that all nodes read from and (partially) write to.

Each node receives an AgentState instance as input and returns a
partial update (a dict containing only the fields it wants to change).
LangGraph merges that update back into the state, validates it
against this schema, and passes the new state to the next node.

Using a Pydantic BaseModel instead of TypedDict gives us:
  - validation on every state update;
  - explicit defaults via Field(default=...);
  - editor autocomplete and type-checking on state attributes.
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from .pk_model import PKParameters

# define the AgentState class, which is the shared state object for all nodes in the workflow
class AgentState(BaseModel):
    """Shared state object for all nodes in the workflow."""

    paper_content: str = Field(
        default="",
        description="Raw text of the input paper.",
    )
    extracted_parameters: Optional[PKParameters] = Field(
        default=None,
        description="PK parameters produced by the extractor node.",
    )
    report: str = Field(
        default="",
        description="Executive summary produced by the reporter node.",
    )

    # add extra='forbid' to catch any typos or unexpected fields in the state updates
    model_config = ConfigDict(extra="forbid")