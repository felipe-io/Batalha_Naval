import time
from utils import limpar_tela
import menu
import jogador
import computador
import tabuleiro
import navios
import estatisticas
import replay

def gerenciar_partida(modo_jogo: str):
    limpar_tela()
    print("Iniciando os preparativos da partida...")
    
    tabuleiro_p1 = tabuleiro.criar_tabuleiro()
    tabuleiro_p2 = tabuleiro.criar_tabuleiro()
    
    navios.posicionar_todos_navios(tabuleiro_p1)
    navios.posicionar_todos_navios(tabuleiro_p2)
    
    tabuleiro_p1 = jogador.configurar_navios_jogador(tabuleiro_p1)
    
    if modo_jogo == "2":
        limpar_tela()
        print("Vez do Jogador 2 conferir seu tabuleiro...")
        tabuleiro_p2 = jogador.configurar_navios_jogador(tabuleiro_p2)

    historico_tiros_p1 = set()
    historico_tiros_p2 = set()
    replay.iniciar_novo_registro()
    
    turno_jogador_1 = True
    total_jogadas = 0
    tiros_certos_humano = 0  
    
    tempo_inicio = time.time()
    
    while True:
        total_jogadas += 1
        
        if turno_jogador_1:
            limpar_tela()
            print(f"=== TURNO DO JOGADOR 1 (Jogada {total_jogadas}) ===")
            print("\nMapa de Tiros no Adversário:")
            tabuleiro.exibir_tabuleiro(tabuleiro_p2, esconder_navios=True)
            print("-" * 50)
            
            linha, coluna, coord_texto = jogador.obter_jogada_humana(historico_tiros_p1)
            historico_tiros_p1.add(coord_texto)
            
            limpar_tela()
            print(f"=== REPERCUSSÃO DA JOGADA {total_jogadas} ===")
            resultado = tabuleiro.dar_tiro(tabuleiro_p2, linha, coluna)
            print(f"\n>> {coord_texto}")
            print(resultado)
            
            if "Acerto" in resultado or "afundado" in resultado:
                tiros_certos_humano += 1
                
            replay.registrar_jogada(total_jogadas, "Jogador 1", coord_texto, resultado)
            
            if not tabuleiro.restando_navios(tabuleiro_p2):
                vencedor = "Jogador 1"
                break
                
            input("\nPressione ENTER para passar o turno...")
            
            turno_jogador_1 = False
                
        else:
            if modo_jogo == "1":
                limpar_tela()
                print(f"=== TURNO DO COMPUTADOR (Jogada {total_jogadas}) ===")
                
                linha, coluna = computador.gerar_jogada_aleatoria(historico_tiros_p2)
                
                colunas_letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
                coord_texto = f"{colunas_letras[coluna]}{linha + 1}"
                historico_tiros_p2.add(coord_texto)
                
                resultado = tabuleiro.dar_tiro(tabuleiro_p1, linha, coluna)
                print(f"\nO Computador atacou a posicao: {coord_texto}")
                print(resultado)
                
                replay.registrar_jogada(total_jogadas, "Computador", coord_texto, resultado)
                
                if not tabuleiro.restando_navios(tabuleiro_p1):
                    vencedor = "Computador"
                    break
                    
                time.sleep(2.5)
                turno_jogador_1 = True
                
            elif modo_jogo == "2":
                limpar_tela()
                print(f"=== TURNO DO JOGADOR 2 (Jogada {total_jogadas}) ===")
                print("\nMapa de Tiros no Adversário:")
                tabuleiro.exibir_tabuleiro(tabuleiro_p1, esconder_navios=True)
                print("-" * 50)
                
                linha, coluna, coord_texto = jogador.obter_jogada_humana(historico_tiros_p2)
                historico_tiros_p2.add(coord_texto)
                
                limpar_tela()
                print(f"=== REPERCUSSÃO DA JOGADA {total_jogadas} ===")
                resultado = tabuleiro.dar_tiro(tabuleiro_p1, linha, coluna)
                print(f"\n>> {coord_texto}")
                print(resultado)
                
                replay.registrar_jogada(total_jogadas, "Jogador 2", coord_texto, resultado)
                
                if not tabuleiro.restando_navios(tabuleiro_p1):
                    vencedor = "Jogador 2"
                    break
                    
                input("\nPressione ENTER para passar o turno...")
                turno_jogador_1 = True

    tempo_fim = time.time()
    tempo_total_segundos = int(tempo_fim - tempo_inicio)
    
    tempo_formatado = time.strftime('%H:%M:%S', time.gmtime(tempo_total_segundos))
    
    limpar_tela()
    estatisticas.exibir_fim_de_jogo(vencedor, total_jogadas, tempo_formatado)
    
    estatisticas.registrar_partida(
        houve_vitoria=(vencedor == "Jogador 1"),
        acertos_partida=tiros_certos_humano,
        total_tiros_partida=len(historico_tiros_p1)
    )
    
    while True:
        print("\n[1] Ver replay  [2] Nova partida  [3] Menu principal")
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            limpar_tela()
            replay.reproduzir_ultimo_replay()
            break
        elif opcao == "2":
            gerenciar_partida(modo_jogo)
            break
        elif opcao == "3":
            break

def loop_principal_sistema():
    while True:
        limpar_tela()
        opcao_menu = menu.exibir_menu_principal()
        
        if opcao_menu == "1":
            modo = menu.exibir_menu_modo_jogo()
            if modo != "0":
                gerenciar_partida(modo)
                
        elif opcao_menu == "2":
            limpar_tela()
            estatisticas.exibir_estatisticas()
            
        elif opcao_menu == "3":
            limpar_tela()
            replay.reproduzir_ultimo_replay()
            
        elif opcao_menu == "4":
            limpar_tela()
            menu.exibir_creditos()
            
        elif opcao_menu == "5":
            limpar_tela()
            print("\nObrigado por jogar Batalha Naval - GPTech Games!")
            print("Encerrando o sistema...")
            break

def iniciar_gui():
    try:
        import gui
        app = gui.BatalhaNavalGUI()
        app.mainloop()
    except ImportError:
        print("\n[ERRO] O arquivo gui.py não foi encontrado na mesma pasta.")
        input("Pressione ENTER para iniciar no modo terminal...")
        loop_principal_sistema()
    except Exception as e:
        print(f"\n[ERRO] Não foi possível iniciar a interface gráfica: {e}")
        input("Pressione ENTER para iniciar no modo terminal...")
        loop_principal_sistema()

if __name__ == "__main__":
    limpar_tela()
    print("=" * 50)
    print("BEM-VINDO AO BATALHA NAVAL - GPTECH GAMES")
    print("=" * 50)
    print("Como você deseja iniciar o jogo?")
    print("[1] - MODO TEXTO (Terminal)")
    print("[2] - MODO GRÁFICO (Interface Tkinter)")
    print("-" * 50)
    
    escolha = input("Escolha uma opção: ").strip()
    
    if escolha == "2":
        iniciar_gui()
    else:
        loop_principal_sistema()