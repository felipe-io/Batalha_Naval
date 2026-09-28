import random

def gerar_jogada_aleatoria(historico_jogadas: set) -> tuple:
    colunas = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    while True:
        linha_idx = random.randint(0,9)
        coluna_idx = random.randint(0,9)

        cordenada_texto = f"{colunas[coluna_idx]}{linha_idx + 1}"
        if cordenada_texto not in historico_jogadas:
            return linha_idx, coluna_idx

def gerar_jogada_inteligente(historico_jogadas: set, tabuleiro_alvo: list) -> tuple:
    return gerar_jogada_aleatoria(historico_jogadas)
