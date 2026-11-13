"""Faça perguntas à base de conhecimento pelo terminal.

Exemplos:
    python perguntar.py "A câmera está offline mas o NVR pinga. O que fazer?"
    python perguntar.py --so-busca "porta 8080 bloqueada"
    python perguntar.py            (modo interativo; "sair" encerra)
"""

import argparse
import sys

import anthropic

from src import config
from src.rag.assistente import responder
from src.retrieval.busca import BaseNaoEncontradaError, abrir_colecao, buscar

AJUDA_CHAVE = (
    "\nNenhuma chave válida da API do Claude foi encontrada.\n"
    "Coloque ANTHROPIC_API_KEY no arquivo .env (nunca no código nem no GitHub)\n"
    "ou rode com --so-busca para ver só os trechos encontrados."
)


def mostrar_busca(pergunta: str, colecao) -> None:
    trechos = buscar(pergunta, colecao=colecao)
    if not trechos:
        print("Nada encontrado.")
    for t in trechos:
        print(f"\n=== {t.referencia}  (distância {t.distancia:.3f}) ===\n{t.texto.strip()}")


def mostrar_resposta(pergunta: str, colecao) -> None:
    resposta = responder(pergunta, colecao=colecao)
    print(f"\n{resposta.texto}")
    if resposta.trechos:
        print("\nTrechos usados:")
        for t in resposta.trechos:
            print(f"  - {t.referencia}  (distância {t.distancia:.3f})")
    if resposta.modelo:
        print(f"Modelo: {resposta.modelo}")


def atender(pergunta: str, colecao, so_busca: bool) -> bool:
    """Responde uma pergunta. Devolve False quando não vale a pena continuar (sem chave)."""
    if so_busca:
        mostrar_busca(pergunta, colecao)
        return True
    try:
        mostrar_resposta(pergunta, colecao)
    except anthropic.AuthenticationError:
        print(AJUDA_CHAVE)
        return False
    except TypeError as erro:
        # O SDK lança TypeError quando não acha nenhuma credencial configurada.
        if "authentication" not in str(erro).lower():
            raise
        print(AJUDA_CHAVE)
        return False
    except anthropic.RateLimitError:
        print("\nLimite de uso da API atingido. Tente de novo em alguns instantes.")
    except anthropic.APIConnectionError:
        print("\nSem conexão com a API do Claude. Confira a internet.")
    except anthropic.APIStatusError as erro:
        print(f"\nErro da API do Claude ({erro.status_code}): {erro.message}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Pergunte à base de conhecimento de TI.")
    parser.add_argument("pergunta", nargs="*", help="a pergunta (vazio = modo interativo)")
    parser.add_argument("--so-busca", action="store_true", help="mostra só os trechos, sem chamar o Claude")
    args = parser.parse_args()

    try:
        colecao = abrir_colecao()
    except BaseNaoEncontradaError as erro:
        print(erro)
        return 1

    modo = "só busca" if args.so_busca else f"RAG com {config.CLAUDE_MODEL}"
    print(f"Base carregada: {colecao.count()} trechos. Modo: {modo}")

    if args.pergunta:
        return 0 if atender(" ".join(args.pergunta), colecao, args.so_busca) else 1

    while True:
        pergunta = input("\nPergunta> ").strip()
        if pergunta.lower() in {"", "sair", "exit"}:
            return 0
        if not atender(pergunta, colecao, args.so_busca):
            return 1


if __name__ == "__main__":
    sys.exit(main())
