import random
NAVIO_PEQUENO = 2
NAVIO_GRANDE = 4

def pode_posicionar(tabuleiro: list, linha: int, coluna: int, tamanho: int, orientacao: str) -> bool:
    if orientacao == "H":
        if coluna + tamanho > 10:
            return False
        for c in range(coluna, coluna + tamanho):
            if tabuleiro[linha][c] == 'N':
                return False
                
    elif orientacao == "V":
        if linha + tamanho > 10:
            return False
        for l in range(linha, linha + tamanho):
            if tabuleiro[l][coluna] == 'N':
                return False
                
    return True


def posicionar_um_navio(tabuleiro: list, tamanho: int):
    colocado = False
    while not colocado:
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)
        orientacao = random.choice(["H", "V"])
        
        if pode_posicionar(tabuleiro, linha, coluna, tamanho, orientacao):
            if orientacao == "H":
                for c in range(coluna, coluna + tamanho):
                    tabuleiro[linha][c] = 'N'
            else:
                for l in range(linha, linha + tamanho):
                    tabuleiro[l][coluna] = 'N'
            colocado = True


def posicionar_todos_navios(tabuleiro: list):
    navios_para_colocar = [NAVIO_GRANDE, NAVIO_GRANDE, NAVIO_PEQUENO, NAVIO_PEQUENO, NAVIO_PEQUENO]
    
    for tamanho in navios_para_colocar:
        posicionar_um_navio(tabuleiro, tamanho)
