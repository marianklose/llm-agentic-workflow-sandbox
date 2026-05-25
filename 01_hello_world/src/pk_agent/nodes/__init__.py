"""
Workflow nodes — the units of work in the LangGraph graph.
Each node is basically a function that takes some input,
does something (e.g. calls an LLM), and returns some output.
In our case, the nodes take the sate as input and return a dict of updates to the state.
"""