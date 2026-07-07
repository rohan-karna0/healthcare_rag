from qdrant_client.http import models as qmodels


def build_filter(sources: list[str] | None) -> qmodels.Filter | None:
    if not sources:
        return None
    return qmodels.Filter(
        must=[
            qmodels.FieldCondition(
                key="source",
                match=qmodels.MatchAny(any=sources),
            )
        ]
    )
