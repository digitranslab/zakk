from typing import TypedDict

from zakk.agents.agent_search.core_state import CoreState
from zakk.agents.agent_search.deep_search.main.states import (
    InitialAnswerUpdate,
)
from zakk.agents.agent_search.deep_search.main.states import (
    InitialQuestionDecompositionUpdate,
)
from zakk.agents.agent_search.deep_search.main.states import (
    SubQuestionResultsUpdate,
)
from zakk.context.search.models import InferenceSection


### States ###
class SubQuestionAnsweringInput(CoreState):
    exploratory_search_results: list[InferenceSection]


## Graph State
class SubQuestionAnsweringState(
    # This includes the core state
    SubQuestionAnsweringInput,
    InitialQuestionDecompositionUpdate,
    InitialAnswerUpdate,
    SubQuestionResultsUpdate,
):
    pass


## Graph Output State
class SubQuestionAnsweringOutput(TypedDict):
    log_messages: list[str]
