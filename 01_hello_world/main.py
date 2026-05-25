"""
Entry point: loads the paper and runs the workflow.
"""
import sys
import uuid
from pathlib import Path
from dotenv import load_dotenv

# make 'src' importable (sandbox convenience, later via pip install -e). 
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

# load environment variables from the repo-root .env BEFORE importing modules
load_dotenv(HERE.parent / ".env")

# importing objects from our own modules inside the pk_agent package
# imports placed after sys.path / dotenv setup are intentional;
# noqa: E402 silences the linter about that.
from pk_agent.config import settings            # noqa: E402
from pk_agent.graph.builder import build_graph  # noqa: E402

# define the main logic
def main() -> None:
    # read the pmx paper containing prose and the parameter estimates
    paper_path = settings.data_dir / "sample_paper.md"
    paper_content = paper_path.read_text(encoding="utf-8")

    # build the graph (based on our own function)
    graph = build_graph()

    # create thread_id (checkpointer stores state under this key) for this run
    # later this might be a session or user id
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # some user information
    print(f"=== Workflow started (thread_id={thread_id[:8]}...) ===\n")

    # run the graph, invoke() executes all nodes synchronously and returns the final state
    # for long-running flows, we can use stream() to receive intermediate updates.
    # we see that we have to pass the initial state to start the graph workflow
    # the intital state is based on our paper content and the config
    result = graph.invoke(
        {"paper_content": paper_content},
        config=config,
    )

    # pretty print the results
    # we see that the results are simply the final version of the updated state
    # langgraph nodes are always taking states and updating parts of the states
    params = result["extracted_parameters"]
    print("--- Extracted parameters ---")
    print(f"  Drug:        {params.drug_name}")
    print(f"  V_d:         {params.volume_of_distribution} L")
    print(f"  CL:          {params.clearance} L/h")
    print()
    print("--- Executive summary ---")
    print(result["report"])

# some special python syntax, prevents from executing the main pipeling, e.g.,
# when only the package is being loaded. only if we directly run the main file
# then it is also being executed
if __name__ == "__main__":
    main()