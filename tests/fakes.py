"""Objetos falsos para testar sem ChromaDB real e sem chamar a API do Claude."""

from types import SimpleNamespace


class ColecaoFalsa:
    """Imita a coleção do ChromaDB: devolve os documentos que mais compartilham palavras com a pergunta."""

    def __init__(self, documentos: dict[str, str]):
        self.documentos = documentos  # {fonte: texto}
        self.ultima_consulta = None

    def count(self) -> int:
        return len(self.documentos)

    def query(self, query_texts, n_results):
        self.ultima_consulta = {"query_texts": query_texts, "n_results": n_results}
        palavras = set(query_texts[0].lower().split())

        def distancia(texto: str) -> float:
            comuns = len(palavras & set(texto.lower().split()))
            return 1.0 / (1 + comuns)

        ordenados = sorted(self.documentos.items(), key=lambda item: distancia(item[1]))[:n_results]
        return {
            "documents": [[texto for _, texto in ordenados]],
            "metadatas": [[{"fonte": fonte, "chunk": 0} for fonte, _ in ordenados]],
            "distances": [[distancia(texto) for _, texto in ordenados]],
        }


class ClaudeFalso:
    """Imita `anthropic.Anthropic()`: guarda o pedido e devolve uma resposta pronta."""

    def __init__(self, texto="Resposta de teste [rede.md#0]", stop_reason="end_turn"):
        self.pedidos = []
        self._resposta = SimpleNamespace(
            content=[
                SimpleNamespace(type="thinking", thinking=""),
                SimpleNamespace(type="text", text=texto),
            ],
            stop_reason=stop_reason,
            model="claude-opus-5-5",
        )
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.pedidos.append(kwargs)
        return self._resposta
