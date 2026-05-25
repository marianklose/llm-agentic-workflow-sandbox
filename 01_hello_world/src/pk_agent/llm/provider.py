"""
LLM provider abstraction.

Every LLM call in the project goes through get_llm(). The wrapper is
deliberately thin today, but it gives us a single chokepoint for
later additions: LiteLLM fallback routing, retry policies, request
logging, or a deterministic mock model for tests. Whatever changes,
the nodes that call get_llm() stay the same.

Allows us to use from ..llm.provider import get_llm and have this central
implementation injected at each node. Easy to change later instead of touching
hard-coded LLM calls in multiple places (harder to maintain). All nodes will use
llm = get_llm() after importing this package.
"""
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from ..config import settings

# define the key function that returns a configured LLM instance, which can be used in the nodes
def get_llm(temperature: float | None = None) -> BaseChatModel:
    """Return a configured chat model.

    Args:
        temperature: Optional override for the default temperature
            from settings/config. Useful when one node needs deterministic
            output (temperature=0) while another wants a bit of
            variation for prose.

    Returns:
        A BaseChatModel instance with the standard LangChain interface:
        .invoke(), .stream(), .with_structured_output(), and so on.
    """

    # init_chat_model directly comes from langchain
    # can be later replaced with LiteLLM logic or pydantic-ai or 
    # whatever we want to use for model calls
    return init_chat_model(
        model=settings.llm_model,
        temperature=temperature if temperature is not None else settings.llm_temperature,
    )