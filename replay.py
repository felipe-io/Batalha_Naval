import os
import time

ARQUIVO_REPLAY = os.path.join("data", "ultimo_replay.txt")

def garantir_diretorio():
    if not os.path.exists("data"):
        os.makedirs("data")


def iniciar_novo_registro():
    garantir_diretorio()
    with open(ARQUIVO_REPLAY, "w", encoding="utf-8") as f:
        pass


def registrar_jogada(numero_jogada: int, jogador: str, coordenada: str, resultado: str):
    garantir_diretorio()
    linha_historico = f"{numero_jogada};{jogador};{coordenada};{resultado}\n"
    with open(ARQUIVO_REPLAY, "a", encoding="utf-8") as f:
        f.write(linha_historico)


def reproduzir_ultimo_replay():
    if not os.path.exists(ARQUIVO_REPLAY) or os.path.getsize(ARQUIVO_REPLAY) == 0:
        print("\n[AVISO] Nao ha replays gravados de partidas anteriores.")
        input("\nPressione ENTER para voltar ao menu...")
        return

    print("\n==================================================")
    print("Reproduzindo replay da ultima partida...")
    print("==================================================")

    with open(ARQUIVO_REPLAY, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    total_jogadas = len(linhas)

    for linha in linhas:
        num, jog, coord, res = linha.strip().split(";")
        print(f"Jogada {int(num):02d}/{total_jogadas:02d} - {jog} - {coord} - {res}")
        opcao = input("[ENTER] Proxima jogada [Q] Sair do replay: ").strip().upper()
        if opcao == 'Q':
            print("\nReplay encerrado pelo usuario.")
            break
            
    print("\nFim do replay!")
    input("Pressione ENTER para voltar ao menu principal...")
