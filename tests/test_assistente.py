from src import config
from src.rag.assistente import SEM_RESPOSTA, montar_mensagem, responder
from src.retrieval.busca import Trecho
from tests.fakes import ClaudeFalso, ColecaoFalsa

DOCUMENTOS = {
    "rede.md": "porta 8080 bloqueada pelo antivírus e firewall",
    "camera.md": "câmera ip offline mas o nvr continua pingando",
}


def test_mensagem_tem_documentos_antes_da_pergunta():
    trechos = [Trecho(texto="liberar porta 8080", fonte="rede.md", chunk=0, distancia=0.1)]
    mensagem = montar_mensagem("Sistema não abre", trechos)
    assert '<documento referencia="rede.md#0">' in mensagem
    assert "liberar porta 8080" in mensagem
    assert mensagem.index("<documentos>") < mensagem.index("Pergunta do chamado: Sistema não abre")


def test_resposta_usa_o_texto_do_claude_e_lista_os_trechos():
    claude = ClaudeFalso(texto="Libere a porta 8080 [rede.md#0]")
    resposta = responder("porta 8080 bloqueada", k=1, colecao=ColecaoFalsa(DOCUMENTOS), client=claude)
    assert resposta.texto == "Libere a porta 8080 [rede.md#0]"
    assert [t.fonte for t in resposta.trechos] == ["rede.md"]
    assert resposta.recusada is False


def test_pedido_ao_claude_usa_modelo_esforco_e_reserva():
    claude = ClaudeFalso()
    responder("câmera offline", colecao=ColecaoFalsa(DOCUMENTOS), client=claude)
    pedido = claude.pedidos[0]
    assert pedido["model"] == config.CLAUDE_MODEL
    assert pedido["output_config"] == {"effort": config.CLAUDE_EFFORT}
    assert pedido["fallbacks"] == "default"
    assert "câmera offline" in pedido["messages"][0]["content"]


def test_recusa_do_modelo_e_sinalizada():
    claude = ClaudeFalso(texto="", stop_reason="refusal")
    resposta = responder("câmera offline", colecao=ColecaoFalsa(DOCUMENTOS), client=claude)
    assert resposta.recusada is True


def test_base_vazia_nao_chama_o_claude():
    claude = ClaudeFalso()
    resposta = responder("qualquer coisa", colecao=ColecaoFalsa({}), client=claude)
    assert resposta.texto == SEM_RESPOSTA
    assert claude.pedidos == []
