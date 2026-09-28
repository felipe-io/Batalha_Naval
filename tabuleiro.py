def criar_tabuleiro() -> list:
    return [['~' for _ in range(10)] for _ in range(10)]


def exibir_tabuleiro(tabuleiro: list, esconder_navios: bool = False):
    print("   A B C D E F G H I J")
    
    for idx_linha, linha in enumerate(tabuleiro):
        numero_linha = f"{idx_linha + 1:2d}"
        elementos_linha = []
        for celula in linha:
            if celula == 'N' and esconder_navios:
                elementos_linha.append('~')
            else:
                elementos_linha.append(celula)
                
        print(f"{numero_linha} {' '.join(elementos_linha)}")
        
    print("\nLegenda: ~ agua nao jogada | N navio | X acerto | O agua jogada")


def dar_tiro(tabuleiro: list, linha: int, coluna: int) -> str:
    status_celula = tabuleiro[linha][coluna]
    
    if status_celula == '~':
        tabuleiro[linha][coluna] = 'O'
        return "Agua! Nenhum navio atingido nessa posicao."
        
    elif status_celula == 'N':
        tabuleiro[linha][coluna] = 'X'
        
        if verificar_se_navio_afundou(tabuleiro, linha, coluna):
            return "Navio afundado! Voce destruiu um navio do adversario."
            
        return "Acerto! Voce atingiu um navio inimigo."


def verificar_se_navio_afundou(tabuleiro: list, linha: int, coluna: int) -> bool:
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visitados = set()
    
    def buscar_partes(l, c):
        if (l, c) in visitados or l < 0 or l >= 10 or c < 0 or c >= 10:
            return False
        
        visitados.add((l, c))
        
        if tabuleiro[l][c] == 'N':
            return True
            
        if tabuleiro[l][c] == 'X':
            for dl, dc in direcoes:
                if buscar_partes(l + dl, c + dc):
                    return True
        return False

    return not buscar_partes(linha, coluna)


def restando_navios(tabuleiro: list) -> bool:
    for linha in tabuleiro:
        if 'N' in linha:
            return True
    return False
