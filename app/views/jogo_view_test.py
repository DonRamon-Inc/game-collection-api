from . import jogo_view as jv

def test_serializar_jogos_deve_ordernar_jogos_por_ordem_alfabetica():
    jogos = [
        {"name": "Bioshock"},
        {"name": "Grand Theft Auto V"},
        {"name": "Crash Bandicoot"},
        {"name": "Battleblock Theather"}
    ]
    resposta = {"response": {"games": jogos, "game_count": 4}}

    resultado = jv.serializar_jogos(resposta)

    assert resultado["quantidade_jogos"] == 4
    jogos_esperados = [
        "Battleblock Theather",
        "Bioshock",
        "Crash Bandicoot",
        "Grand Theft Auto V"
    ]
    assert resultado["jogos"] == jogos_esperados
