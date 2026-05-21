"""
Graph builder: assembles the LangGraph workflow.

We wrap construction in a factory function so that:
  1. Tests can build the graph with a mock or in-memory checkpointer
     and run it in isolation.
  2. The checkpointer is a parameter, not hard-coded. Swapping
     InMemorySaver for SqliteSaver or PostgresSaver becomes a
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
    # 1. Create the graph skeleton, binding it to our state schema.
    workflow = StateGraph(AgentState)

    # 2. Register each node under a string name. The names appear in
    #    LangSmith traces and error messages, so make them descriptive.
    workflow.add_node("extractor", extract_parameters)
    workflow.add_node("reporter", write_report)

    # 3. Wire the edges: START -> extractor -> reporter -> END.
    #    For conditional routing or parallel fan-out, LangGraph
    #    provides add_conditional_edges() and the Send primitive,
    #    but a linear flow is all we need here.
    workflow.add_edge(START, "extractor")
    workflow.add_edge("extractor", "reporter")
    workflow.add_edge("reporter", END)

    # 4. Choose a checkpointer. The checkpointer controls where state
    #    is persisted between steps. It also enables human-in-the-loop
    #    interrupts, resume-after-failure, and time-travel debugging.
    if checkpointer is None:
        checkpointer = InMemorySaver()

    # 5. Compile freezes the topology and returns a runnable graph.
    return workflow.compile(checkpointer=checkpointer)