from config.settings import settings
from retrieval.bm25 import BM25Retriever
from retrieval.dense import DenseRetriever
from retrieval.hybrid import HybridRetriever
from retrieval.query_expansion import expand_query
from reranking.bge_reranker import BGEReranker


class Retriever:
    def __init__(self):
        self.dense = DenseRetriever()
        self.bm25 = BM25Retriever()
        self.hybrid = HybridRetriever(self.dense, self.bm25)
        self.reranker = BGEReranker() if settings.use_reranker else None

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        sources: list[str] | None = None,
        mode: str | None = None,
        expand: bool = True,
    ):
        effective_query = expand_query(query) if expand else query
        effective_mode = mode or settings.retrieval_mode
        k = top_k or settings.top_k

        if effective_mode == "dense":
            results = self.dense.retrieve(effective_query, top_k=k, sources=sources)
        elif effective_mode == "bm25":
            results = self.bm25.retrieve(effective_query, top_k=k, sources=sources)
        else:
            results = self.hybrid.retrieve(effective_query, top_k=k, sources=sources)

        if self.reranker and results:
            results = self.reranker.rerank(query, results, top_k=k)
        return results
