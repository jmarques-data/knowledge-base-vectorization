from src.ingestion.vetorizar_base import fragmentar_texto


def test_texto_curto_vira_um_unico_trecho():
    assert fragmentar_texto("abc", tamanho_chunk=10, sobreposicao=2) == ["abc"]


def test_trechos_tem_sobreposicao():
    texto = "".join(str(i % 10) for i in range(25))
    trechos = fragmentar_texto(texto, tamanho_chunk=10, sobreposicao=3)
    # Cada trecho começa com os 3 últimos caracteres do anterior.
    for anterior, atual in zip(trechos, trechos[1:]):
        assert atual[:3] == anterior[-3:]


def test_nenhum_caractere_se_perde():
    texto = "a" * 7 + "b" * 7 + "c" * 7
    trechos = fragmentar_texto(texto, tamanho_chunk=8, sobreposicao=2)
    reconstruido = trechos[0] + "".join(t[2:] for t in trechos[1:])
    assert reconstruido == texto
