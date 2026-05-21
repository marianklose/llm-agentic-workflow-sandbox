"""
Entry point: loads the paper and runs the workflow.
"""
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv

# 1. Make 'src' importable. This is the only place we touch sys.path,
#    and it's a sandbox convenience. In a packaged project you would
#    install the package with `pip install -e .` instead.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

# 2. Load environment variables from the repo-root .env BEFORE importing
#    any modules that read them at import time (Settings does).
load_dotenv(HERE.parent / ".env")

# Imports placed after sys.path / dotenv setup are intentional;
# noqa: E402 silences the linter about that.
from pk_agent.config import settings        # noqa: E402
from pk_agent.graph.builder import build_graph  # noqa: E402


def main() -> None:
    # 1. Read the input paper.
    paper_path = settings.data_dir / "sample_paper.md"
    paper_content = paper_path.read_text(encoding="utf-8")

    # 2. Build the graph with default settings (in-memory checkpointer).
    graph = build_graph()

    # 3. Create a thread_id for this run. The thread_id is the key
    #    under which the checkpointer stores state. In production this
    #    would typically be derived from a session id or user id so
    #    the same workflow can be resumed later.
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print(f"=== Workflow started (thread_id={thread_id[:8]}...) ===\n")

    # 4. Run the graph. invoke() executes all nodes synchronously and
    #    returns the final state. For long-running flows, use stream()
    #    to receive intermediate updates.
    result = graph.invoke(
        {"paper_content": paper_content},
        config=config,
    )

    # 5. Pretty-print the results.
    params = result["extracted_parameters"]
    print("--- Extracted parameters ---")
    print(f"  Drug:        {params.drug_name}")
    print(f"  V_d:         {params.volume_of_distribution} L")
    print(f"  CL:          {params.clearance} L/h")
    print()
    print("--- Executive summary ---")
    print(result["report"])


if __name__ == "__main__":
    main()