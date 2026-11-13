import pytest

from src.retrieval.busca import buscar
from tests.fakes import ColecaoFalsa

DOCUMENTOS = {
    "rede.md": "porta 8080 bloqueada pelo antivírus e firewall",
    "camera.md": "câmera ip offline mas o nvr continua pingando",
    "disco.md": "disco lotado com vídeos antigos na pasta converted",
}


def test_traz_o_trecho_mais_relevante_primeiro():
    trechos = buscar("a câmera ip está offline", k=2, colecao=ColecaoFalsa(DOCUMENTOS))
    assert trechos[0].fonte == "camera.md"
    assert trechos[0].distancia <= trechos[1].distancia


def test_nao_pede_mais_trechos_do_que_existem():
    colecao = ColecaoFalsa(DOCUMENTOS)
    trechos = buscar("firewall", k=10, colecao=colecao)
    assert len(trechos) == 3
    assert colecao.ultima_consulta["n_results"] == 3


def test_referencia_cita_arquivo_e_trecho():
    trecho = buscar("porta 8080", k=1, colecao=ColecaoFalsa(DOCUMENTOS))[0]
    assert trecho.referencia == "rede.md#0"


def test_base_vazia_devolve_lista_vazia():
    assert buscar("qualquer coisa", colecao=ColecaoFalsa({})) == []


def test_pergunta_vazia_da_erro():
    with pytest.raises(ValueError):
        buscar("   ", colecao=ColecaoFalsa(DOCUMENTOS))
