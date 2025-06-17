from models.plan import ExecutionPlan
from context.context_providers import get_context_sources, get_semantic_context

def route_and_fetch(plan: ExecutionPlan) -> list[dict]:
    context = []
    for step in plan.steps:
        if step.type == "keyword":
            context += get_context_sources(step.query)
        elif step.type == "semantic":
            context += get_semantic_context(step.query)
    return context