from utils import validar_formato_coordenada, converter_texto_para_indices
import tabuleiro

def obter_jogada_humana(historico_jogadas: set) -> tuple:
    while True:
        entrada = input("Sua jogada (ex: C5): ").strip()
        if not validar_formato_coordenada(entrada):
            print("[ERRO] Coordenada invalida! Use o formato Letra (A-J) + Numero (1-10).")
            continue

        coordenada_texto = entrada.upper()
        if coordenada_texto in historico_jogadas:
            print("[ERRO] Posição já jogada! Escolha outra!")
            continue

        linha_idx, coluna_idx = converter_texto_para_indices(coordenada_texto)
        return linha_idx, coluna_idx, coordenada_texto

def configurar_navios_jogador(matriz_tabuleiro: list) -> list:
    print("\nPosicionando seus navios secretamente no tabuleiro...")
    print("\n--- SEU TABULEIRO CONFIGURADO ---")
    tabuleiro.exibir_tabuleiro(matriz_tabuleiro, esconder_navios=False) 
    print("---------------------------------")
    
    input("Confira a posicao dos seus navios e pressione ENTER para confirmar e iniciar a partida...")
    return matriz_tabuleiro