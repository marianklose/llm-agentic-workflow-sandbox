"""
Graph builder: assembles the LangGraph workflow via a factory function.

We wrap construction in a factory function so that:
  1. Tests can build the graph with a mock or in-memory checkpointer
     and run it in isolation.
  2. The checkpointer (saving the state after each step) is a parameter, not hard-coded.
      Swapping InMemorySaver for SqliteSaver or PostgresSaver becomes a
     one-line change at the call site.
  3. main.py, a future FastAPI endpoint, and a Jupyter notebook can
     all share the same construction code.
"""
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from ..nodes.extractor import extract_parameters
from ..nodes.reporter import write_report
from ..schemas.state import AgentState


# the main factory function that returns the compiled graph that can be invoked or streamed
def build_graph(checkpointer: BaseCheckpointSaver | None = None):
    """Build the workflow and return a runnable compiled graph.

    Args:
        checkpointer: Optional checkpointer instance. Defaults to
            InMemorySaver, which keeps state in process memory and is
            lost on restart. For production-style persistence, pass a
            SqliteSaver or PostgresSaver instance.

    Returns:
        A CompiledStateGraph exposing .invoke(), .stream(),
        .get_state(), and the rest of the LangGraph API.
    """
    # creating a graph skeleton while binding it to our define state schema
    # the pydantic class AgentState is defined in 01_hello_world/src/pk_agent/schemas/state.py
    workflow = StateGraph(AgentState)

    # we tell LangGraph that two nodes exist
    # the string names appear in LangSmith traces and errors, so they have
    # to be descriptive for later debugging
    workflow.add_node("extractor", extract_parameters)
    workflow.add_node("reporter", write_report)

    # now we are wiring the edges, we want to achieve:
    # START -> extractor -> reporter -> END
    # later, with conditional routing we can use add_conditional_edges()
    # here we have a simple linear workflow
    workflow.add_edge(START, "extractor")
    workflow.add_edge("extractor", "reporter")
    workflow.add_edge("reporter", END)

    # define the checkpointer, which defines where states are saved between steps
    # for our sandbox purpose, InMemorySaver() is sufficient. 
    # having a checkpointer enables later human-in-the-loop interrupts or resume-after-failure
    if checkpointer is None:
        checkpointer = InMemorySaver()

    # compile returns a runnable graph according to our config
    return workflow.compile(checkpointer=checkpointer)