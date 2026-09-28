import os

ARQUIVO_ESTATISTICAS = os.path.join("data", "estatisticas.txt")

def garantir_diretorio_e_arquivo():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(ARQUIVO_ESTATISTICAS):
        with open(ARQUIVO_ESTATISTICAS, "w", encoding="utf-8") as f:
            f.write("0,0,0")


def registrar_partida(houve_vitoria: bool, acertos_partida: int, total_tiros_partida: int):
    garantir_diretorio_e_arquivo()
    
    with open(ARQUIVO_ESTATISTICAS, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()
        partidas, acertos, tiros = map(int, conteudo.split(","))
    
    partidas += 1
    acertos += acertos_partida
    tiros += total_tiros_partida
    
    with open(ARQUIVO_ESTATISTICAS, "w", encoding="utf-8") as f:
        f.write(f"{partidas},{acertos},{tiros}")


def exibir_estatisticas():
    garantir_diretorio_e_arquivo()
    
    with open(ARQUIVO_ESTATISTICAS, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()
        partidas, acertos, tiros = map(int, conteudo.split(","))
    
    aproveitamento = 0.0
    if tiros > 0:
        aproveitamento = (acertos / tiros) * 100

    print("\n" + "=" * 50)
    print("ESTATÍSTICAS DE DESEMPENHO")
    print("=" * 50)
    print(f"Total de partidas jogadas : {partidas}")
    print(f"Total de tiros disparados : {tiros}")
    print(f"Total de acertos em navios: {acertos}")
    print(f"Aproveitamento Geral     : {aproveitamento:.2f}%")
    print("=" * 50)
    
    input("\nPressione ENTER para voltar ao menu principal...")


def exibir_fim_de_jogo(vencedor: str, total_jogadas: int, tempo_formatado: str):
    print("\n" + "=" * 50)
    print("FIM DE JOGO")
    print("=" * 50)
    print(f"Vencedor: {vencedor}")
    print(f"Total de jogadas: {total_jogadas}")
    print(f"Tempo de partida: {tempo_formatado}")
    print("-" * 50)
