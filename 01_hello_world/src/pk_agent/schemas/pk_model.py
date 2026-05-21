"""
Domain models: pharmacokinetic parameters. Basically, what
extracted PK parameters should look like.

A single Pydantic class serves three purposes at once:

  1. Structured-output contract: when an LLM is asked to produce a
     PKParameters object, LangChain translates this schema into the
     provider's tool-calling format, forcing the model to return
     conforming data.

  2. Validation: fields are checked against constraints (e.g. volume
     must be > 0). Bad LLM output raises an error here instead of
     silently corrupting downstream nodes.

  3. Documentation: each Field's description is included in the
     schema sent to the LLM, so the model understands what each
     parameter means without us repeating the explanation in the
     prompt.
"""
from pydantic import BaseModel, ConfigDict, Field


class PKParameters(BaseModel):
    """PK parameters of a one-compartment IV model."""

    drug_name: str = Field(
        ...,
        description="Name of the investigated drug (INN or code name).",
    )
    volume_of_distribution: float = Field(
        ...,
        # has to be greater than 0 to be physiologically plausible.
        gt=0,
        # helps the model to understand what this parameter means and what units to use.
        description=(
            "Volume of distribution V in liters (L). If the source "
            "reports a different unit, convert to L before returning."
        ),
    )
    clearance: float = Field(
        ...,
        gt=0,
        description=(
            "Clearance CL in L/h. Convert other units if needed "
            "(1 mL/min = 0.06 L/h)."
        ),
    )

    # extra='forbid' rejects any unexpected fields. Catches typos and
    # hallucinated keys at the boundary instead of letting them through.
    model_config = ConfigDict(extra="forbid")