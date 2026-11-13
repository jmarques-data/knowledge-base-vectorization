"""Configurações compartilhadas pelo pipeline (ingestão, busca e RAG).

Tudo pode ser trocado pelo arquivo `.env` (veja `.env.example`).
"""

import os

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KNOWLEDGE_PATH = os.getenv("KNOWLEDGE_PATH", os.path.join(ROOT_DIR, "knowledge"))
CHROMA_PATH = os.getenv("CHROMA_PATH", os.path.join(ROOT_DIR, "vector_db"))
COLLECTION_NAME = "base_conhecimento_ti"

# Quantos trechos a busca devolve para cada pergunta.
TOP_K = int(os.getenv("RAG_TOP_K", "4"))

# Modelo e nível de esforço do Claude usados na resposta.
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-5-5")
CLAUDE_EFFORT = os.getenv("CLAUDE_EFFORT", "medium")  # low | medium | high | xhigh | max
