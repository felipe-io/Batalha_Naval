# Batalha Naval - GPTech Games

Um jogo clássico de Batalha Naval desenvolvido em Python, oferecendo duas experiências de jogo: um modo texto interativo via terminal e um modo gráfico moderno utilizando a biblioteca Tkinter.

## Instruções de Compilação e Execução

O projeto foi escrito em Python puro e utiliza bibliotecas padrão do sistema (como `tkinter`, `os`, `time`, `random`), portanto, não é necessária a instalação de dependências externas complexas via `pip` se o seu ambiente Python estiver devidamente configurado.

### Pré-requisitos
- **Python 3.x** instalado na máquina. (O suporte ao Tkinter normalmente já vem embutido nas instalações padrão do Python no Windows e macOS. No Linux, pode ser necessário instalar o pacote `python3-tk`).

### Como rodar o jogo
1. Abra o terminal ou prompt de comando.
2. Navegue até a pasta raiz onde os arquivos do projeto estão localizados.
3. Execute o arquivo principal digitando o seguinte comando:
   ```bash
   python main.py
   ```
4. O menu principal será exibido no terminal, perguntando se você deseja iniciar o **Modo Texto (Terminal)** ou o **Modo Gráfico (Interface Tkinter)**. Escolha a opção desejada e divirta-se!
   * *Nota: Se você quiser pular o menu e abrir diretamente a interface gráfica, pode executar `python gui.py`.*

## Estrutura de Pastas e Arquivos

O projeto está organizado de forma modular, separando a lógica de negócio, a interface gráfica e a persistência de dados.

```text
/
├── main.py              # Ponto de entrada principal do sistema
├── gui.py               # Interface gráfica (Tkinter) e lógica visual
├── menu.py              # Exibição e controle dos menus no modo terminal
├── jogador.py           # Interações e inputs do jogador humano
├── computador.py        # Inteligência e jogadas da CPU
├── tabuleiro.py         # Criação e manipulação da matriz do jogo
├── navios.py            # Lógica de posicionamento e validação de navios
├── estatisticas.py      # Gerenciamento de pontuações e histórico de vitórias
├── replay.py            # Sistema de gravação e reprodução de partidas
├── utils.py             # Funções utilitárias (limpar tela, conversão de coordenadas, etc)
├── logo.png             # (Opcional) Imagem de logo para a GUI
├── background.png       # (Opcional) Imagem de fundo para a GUI
└── data/                # Pasta gerada automaticamente pelo sistema
    ├── estatisticas.txt # Salva as estatísticas globais do jogador
    └── ultimo_replay.txt# Armazena o log da última partida jogada
```

## Resumo das Funções por Módulo

Abaixo está o detalhamento de cada função e classe presente no código-fonte, organizados por arquivo:

### `main.py`
Responsável pelo fluxo principal e por integrar os demais módulos.
- **`gerenciar_partida(modo_jogo: str)`**: Controla o loop principal de uma partida no modo texto, gerenciando os turnos entre jogadores/computador, chamando funções de ataque e checando condições de vitória.
- **`loop_principal_sistema()`**: Controla o menu principal do modo terminal, redirecionando o usuário para jogar, ver estatísticas, replays ou créditos.
- **`iniciar_gui()`**: Tenta importar e iniciar a interface gráfica (`gui.py`). Se falhar, faz fallback para o modo texto.

### `gui.py`
Contém a interface gráfica completa do jogo utilizando Tkinter.
- **Classes**:
  - `FrameSombreado`: Cria um contêiner estilizado com efeito de sombra.
  - `BotaoModerno`: Cria botões customizados com efeitos de hover.
  - `BatalhaNavalGUI`: A classe principal da janela do jogo.
- **Métodos da `BatalhaNavalGUI`**:
  - `__init__`: Configura a janela, fontes, variáveis de estado e chama o menu.
  - `limpar_janela`: Remove todos os widgets atuais da tela.
  - `configurar_fundo`: Aplica a imagem ou cor de fundo no Canvas.
  - `mostrar_menu`: Desenha a tela inicial com opções de Nova Partida, Estatísticas e Sair.
  - `mostrar_estatisticas`: Lê o arquivo de estatísticas e exibe um pop-up com os dados.
  - `iniciar_partida`: Prepara os tabuleiros e desenha a tela de batalha.
  - `desenhar_cabecalho_grid`: Cria as letras (A-J) acima dos tabuleiros.
  - `desenhar_grid_estatico`: Renderiza o tabuleiro do jogador (mostrando os navios) apenas para visualização.
  - `desenhar_grid_interativo`: Renderiza o tabuleiro do inimigo, adicionando eventos de clique para o jogador atirar.
  - `jogada_jogador`: Processa o clique do jogador no mapa inimigo, atualiza o visual da célula e passa o turno para a CPU.
  - `jogada_cpu`: Sorteia uma coordenada para a máquina atacar o jogador e atualiza o mapa visualmente.
  - `fim_de_jogo`: Finaliza a partida, salva os dados e exibe a mensagem do vencedor.

### `tabuleiro.py`
Gerencia a matriz de jogo.
- **`criar_tabuleiro()`**: Retorna uma matriz 10x10 preenchida com água (`~`).
- **`exibir_tabuleiro()`**: Imprime o tabuleiro formatado no terminal, com opção de ocultar navios inimigos.
- **`dar_tiro()`**: Executa a lógica de ataque em uma coordenada. Marca água (`O`) ou acerto (`X`) e verifica se afundou algo.
- **`verificar_se_navio_afundou()`**: Realiza uma busca (Flood Fill/DFS) nas células adjacentes para checar se todas as partes de um navio foram atingidas.
- **`restando_navios()`**: Verifica se ainda existe alguma letra `N` no tabuleiro (condição de fim de jogo).

### `navios.py`
Cuida da lógica de colocação de frotas.
- **`pode_posicionar()`**: Verifica se um navio cabe na posição desejada e se não sobrepõe outro navio existente.
- **`posicionar_um_navio()`**: Tenta posicionar um navio de tamanho específico aleatoriamente até encontrar um espaço válido.
- **`posicionar_todos_navios()`**: Aloca a frota inteira (2 grandes, 3 pequenos) no tabuleiro recebido.

### `jogador.py`
Trata das interações do jogador no modo texto.
- **`obter_jogada_humana()`**: Pede a coordenada ao usuário no terminal, valida o formato e checa se já não foi jogada antes.
- **`configurar_navios_jogador()`**: Exibe o tabuleiro recém-criado para o jogador conferir a posição (secreta) dos seus navios antes da partida.

### `computador.py`
Inteligência artificial básica.
- **`gerar_jogada_aleatoria()`**: Sorteia coordenadas aleatórias até achar uma que ainda não tenha sido atacada pelo histórico.
- **`gerar_jogada_inteligente()`**: Função preparada para futura expansão (IA mais avançada), atualmente funciona como um *wrapper* para a jogada aleatória.

### `estatisticas.py`
Persistência de dados de desempenho.
- **`garantir_diretorio_e_arquivo()`**: Cria a pasta `data/` e o arquivo `estatisticas.txt` caso não existam.
- **`registrar_partida()`**: Atualiza o arquivo com +1 partida, total de acertos e tiros totais dados.
- **`exibir_estatisticas()`**: Lê o arquivo, calcula o aproveitamento em % e exibe no terminal.
- **`exibir_fim_de_jogo()`**: Imprime o sumário da partida (vencedor, jogadas, tempo) no terminal.

### `replay.py`
Sistema de gravação de passos.
- **`garantir_diretorio()`**: Verifica se a pasta `data/` existe.
- **`iniciar_novo_registro()`**: Zera/cria o arquivo `ultimo_replay.txt` no começo de uma nova partida.
- **`registrar_jogada()`**: Adiciona uma linha ao arquivo com os dados da jogada atual (turno, jogador, coordenada, resultado).
- **`reproduzir_ultimo_replay()`**: Lê o arquivo de replay e exibe jogada a jogada no terminal, pausando a cada passo.

### `menu.py`
Telas estáticas do terminal.
- **`exibir_menu_principal()`**: Mostra opções de jogar, ver stats, replay, etc., e coleta a escolha do usuário.
- **`exibir_menu_modo_jogo()`**: Exibe as opções de Vs Computador ou Multi-jogador (PVP local).
- **`exibir_creditos()`**: Mostra as informações do desenvolvedor e disciplina.

### `utils.py`
Funções auxiliares gerais.
- **`limpar_tela()`**: Limpa a tela do terminal (suporta Windows e Unix).
- **`validar_formato_coordenada()`**: Checa usando validação de strings se a entrada do usuário está no formato correto (ex: A1 a J10).
- **`converter_texto_para_indices()`**: Transforma uma string como "B5" em índices de matriz (linha 4, coluna 1).
- **`converter_indices_para_texto()`**: Faz o processo inverso, recebendo índices (0, 0) e retornando "A1".