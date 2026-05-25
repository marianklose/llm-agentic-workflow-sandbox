# llm-agentic-workflow-sandbox

My personal learning sandbox for building LLM-based agentic workflows in pharmacometrics. Each numbered folder is a self-contained example; and future examples will build on what earlier ones established.

Built with [LangGraph](https://github.com/langchain-ai/langgraph) for orchestration, [LangChain](https://github.com/langchain-ai/langchain) for provider-agnostic model access, and [Pydantic](https://docs.pydantic.dev/) for structured outputs and state validation.

> This is a personal learning project, not production code. Expect rough edges and the occasional misunderstanding. My reasoning is documented in the accompanying blog posts.

## Examples

- **`01_hello_world/`** — Two linear nodes (extractor → reporter) extracting PK parameters from a short paper. The foundation everything else will build on. Blog post: [Building a Human-in-the-Loop LLM Agent Workflow for Pharmacometrics — Part 1](https://marian-klose.com/posts/hitl_llm_agentic_pmx_workflow/index.html).

More to follow soon: human-in-the-loop interrupts, conditional routing, NONMEM integration, ...

## Setup

```bash
git clone https://github.com/marianklose/llm-agentic-workflow-sandbox.git
cd llm-agentic-workflow-sandbox

python -m venv .venv
source .venv\Scripts\activate          # Other: .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file at the repo root with your API key(s):

```bash
ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...             
```

## Running an example

```bash
python 01_hello_world/main.py
```


