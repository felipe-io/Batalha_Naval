import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_formato_coordenada(coordenada_texto: str) -> bool:
    coordenada = coordenada_texto.strip().upper()
    if len(coordenada) < 2 or len(coordenada) > 3:
        return False

    letra = coordenada[0]
    numero_texto = coordenada[1:]

    if letra not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
        return False

    if not numero_texto.isdigit():
        return False

    numero = int(numero_texto)
    if numero < 1 or numero > 10:
        return False

    return True


def converter_texto_para_indices(coordenada_texto: str) -> tuple:
    coordenada = coordenada_texto.strip().upper()
    letra = coordenada[0]
    numero = int(coordenada[1:])

    colunas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    coluna_idx = colunas.index(letra)

    linha_idx = numero - 1

    return linha_idx, coluna_idx

def converter_indices_para_texto(linhas_idx: int, coluna_idx: int) -> str:
    colunas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    letra = colunas[coluna_idx]
    numero = linhas_idx + 1

    return f"{letra}{numero}"

