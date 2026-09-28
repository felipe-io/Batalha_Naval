def exibir_menu_principal() -> str:
    while True:
        print("=" * 50)
        print("BATALHA NAVAL - GPTECH GAMES")
        print("=" * 50)
        print("1 - NOVA PARTIDA")
        print("2 - VER ESTATISTICAS")
        print("3 - ASSISTIR REPLAY DA ULTIMA PARTIDA")
        print("4 - CREDITOS")
        print("5 - SAIR")
        print("-" * 50)

        opcao = input("Escolha uma opção: ").strip()
        if opcao in ["1", "2", "3", "4", "5"]:
            return opcao

        print("\n[ERRO] Opção inválida!")

def exibir_menu_modo_jogo() -> str:
    while True:
        print("\nSELECIONE O MODO DE JOGO:")
        print("[1] - JOGADOR VS COMPUTADOR")
        print("[2] - DOIS JOGADORES")
        print("[0] - VOLTAR AO MENU")

        opcao = input(">> ").strip()
        if opcao in ["1", "2", "0"]:
            return opcao

        print("\n[ERRO] Opção inválida!")

def exibir_creditos():
    print("\n" + "=" * 50)
    print("CRÉDITOS")
    print("=" * 50)
    print("Desenvolvedor: Felipe Vieira")
    print("Empresa: GPTech Games")
    print("Disciplina: Programação em Python - CEFET-MG")
    print("=" * 50)
    input("\nPressione ENTER para voltar...")






