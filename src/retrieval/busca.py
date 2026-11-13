"""Camada de busca semântica: recebe uma pergunta e devolve os trechos mais parecidos.

Fluxo:
    pergunta -> embedding da pergunta -> busca no ChromaDB -> trechos relevantes
"""

from dataclasses import dataclass

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from src import config


@dataclass
class Trecho:
    """Um pedaço de documento encontrado pela busca."""

    texto: str
    fonte: str
    chunk: int
    distancia: float

    @property
    def referencia(self) -> str:
        """Nome curto para citar o trecho, ex.: `001_Troubleshooting.md#2`."""
        return f"{self.fonte}#{self.chunk}"


class BaseNaoEncontradaError(RuntimeError):
    """A base vetorial ainda não foi criada (rode a vetorização antes)."""


def abrir_colecao(caminho: str = config.CHROMA_PATH):
    """Abre a coleção do ChromaDB criada por `src/ingestion/vetorizar_base.py`."""
    client = chromadb.PersistentClient(path=caminho, settings=Settings(anonymized_telemetry=False))
    try:
        return client.get_collection(
            config.COLLECTION_NAME,
            embedding_function=embedding_functions.DefaultEmbeddingFunction(),
        )
    except Exception as erro:  # o ChromaDB muda o tipo de erro entre versões
        raise BaseNaoEncontradaError(
            "Base vetorial não encontrada. Rode primeiro: python src/ingestion/vetorizar_base.py"
        ) from erro


def buscar(pergunta: str, k: int = config.TOP_K, colecao=None) -> list[Trecho]:
    """Devolve os `k` trechos mais próximos da pergunta, do mais para o menos relevante."""
    pergunta = pergunta.strip()
    if not pergunta:
        raise ValueError("A pergunta está vazia.")

    colecao = colecao if colecao is not None else abrir_colecao()
    total = colecao.count()
    if total == 0:
        return []

    resultado = colecao.query(query_texts=[pergunta], n_results=min(k, total))

    trechos = []
    for texto, meta, distancia in zip(
        resultado["documents"][0], resultado["metadatas"][0], resultado["distances"][0]
    ):
        trechos.append(
            Trecho(
                texto=texto,
                fonte=meta.get("fonte", "desconhecida"),
                chunk=int(meta.get("chunk", 0)),
                distancia=float(distancia),
            )
        )
    return trechos
