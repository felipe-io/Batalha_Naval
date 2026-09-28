import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import time
import os

import tabuleiro
import navios
import computador
import estatisticas

CORES = {
    "bg": "#1e272e",          
    "panel_bg": "#2f3542",    
    "shadow_dark": "#15191d", 
    "shadow_light": "#3d4650",
    "text": "#f1f2f6",
    "text_muted": "#a4b0be",
    "primary": "#0abde3",      
    "danger": "#ff6b6b",      
    "agua": "#48dbfb",         
    "acerto": "#ff9f43",       
    "miss": "#576574",         
    "navio_proprio": "#1dd1a1" 
}

ARQUIVO_LOGO = "logo.png"
ARQUIVO_BG = "background.png"  

class FrameSombreado(tk.Frame):
    def __init__(self, parent, **kwargs):
        bg_color = kwargs.pop('bg', CORES["panel_bg"])
        p_x = kwargs.pop('padx', 0)
        p_y = kwargs.pop('pady', 0)
        
        super().__init__(parent, bg=CORES["shadow_dark"], padx=2, pady=2, **kwargs)
        
        self.inner_frame = tk.Frame(self, bg=bg_color, bd=0, highlightthickness=0, padx=p_x, pady=p_y)
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 2), pady=(0, 2))

class BotaoModerno(tk.Button):
    def __init__(self, parent, **kwargs):
        color = kwargs.pop('fg_color', CORES["primary"])
        super().__init__(parent, 
                         font=("Montserrat", 12, "bold"),
                         fg="white", 
                         bg=color,
                         activebackground=CORES["text"],
                         activeforeground="black",
                         relief=tk.RAISED,
                         bd=4,
                         cursor="hand2",
                         **kwargs)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.off_hover)

    def on_hover(self, event):
        self.config(relief=tk.FLAT)

    def off_hover(self, event):
        self.config(relief=tk.RAISED)

class BatalhaNavalGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPTech Games - Batalha Naval")
        
        self.geometry("1600x900")
        self.resizable(True, True) 
        self.configure(bg=CORES["bg"])
        
        try:
            self.state('zoomed')
        except:
            pass
        
        self.font_titulo = tkfont.Font(family="Montserrat", size=44, weight="bold")
        self.font_subtitulo = tkfont.Font(family="Open Sans", size=16)
        self.font_grid = tkfont.Font(family="Consolas", size=14, weight="bold")
        
        self.tabuleiro_p1 = None
        self.tabuleiro_cpu = None
        self.historico_p1 = set()
        self.historico_cpu = set()
        
        self.labels_cpu = []
        self.labels_p1 = [] 
        
        self.total_jogadas = 0
        self.tiros_certos = 0
        self.tempo_inicio = 0
        
        self.img_logo = None 
        self.img_bg = None
        self.canvas = None
        
        self.mostrar_menu()

    def limpar_janela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def configurar_fundo(self):
        self.canvas = tk.Canvas(self, bg=CORES["bg"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.update_idletasks()
        
        if os.path.exists(ARQUIVO_BG):
            try:
                self.img_bg = tk.PhotoImage(file=ARQUIVO_BG)
                self.canvas.create_image(self.winfo_width()//2, self.winfo_height()//2, image=self.img_bg, anchor=tk.CENTER)
            except Exception as e:
                print(f"[ERRO GUI] Falha ao carregar a imagem de fundo: {e}")

    def mostrar_menu(self):
        self.limpar_janela()
        self.configurar_fundo() 
        
        cx = self.winfo_width() // 2
        y_pos = 250 
        
        if os.path.exists(ARQUIVO_LOGO):
            try:
                self.img_logo = tk.PhotoImage(file=ARQUIVO_LOGO)
                self.canvas.create_image(cx, y_pos, image=self.img_logo, anchor=tk.CENTER)
                y_pos += self.img_logo.height() // 2 + 30
            except Exception:
                pass
                
        self.canvas.create_text(cx, y_pos, text="© GPTech Games Studio", font=self.font_subtitulo, fill=CORES["text_muted"])
        
        y_pos += 100
        
        btn_nova = BotaoModerno(self.canvas, text="NOVA PARTIDA (VS CPU)", width=40, height=2, command=self.iniciar_partida)
        self.canvas.create_window(cx, y_pos, window=btn_nova, anchor=tk.CENTER)
        
        y_pos += 80
        btn_stats = BotaoModerno(self.canvas, text="VER ESTATÍSTICAS", width=40, height=2, fg_color="#485e74", command=self.mostrar_estatisticas)
        self.canvas.create_window(cx, y_pos, window=btn_stats, anchor=tk.CENTER)
        
        y_pos += 80
        btn_sair = BotaoModerno(self.canvas, text="SAIR", width=40, height=2, fg_color=CORES["danger"], command=self.destroy)
        self.canvas.create_window(cx, y_pos, window=btn_sair, anchor=tk.CENTER)

    def mostrar_estatisticas(self):
        estatisticas.garantir_diretorio_e_arquivo()
        arquivo = os.path.join("data", "estatisticas.txt")
        texto_stats = "Nenhuma partida registada."
        
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                if conteudo:
                    p, a, t = map(int, conteudo.split(","))
                    aprov = (a / t * 100) if t > 0 else 0
                    texto_stats = f"Partidas: {p}\nTiros: {t}\nAcertos: {a}\nAproveitamento: {aprov:.1f}%"
        except Exception:
            texto_stats = "Erro ao ler as estatísticas."
        
        messagebox.showinfo("GPTech Games - Estatísticas", texto_stats)

    def iniciar_partida(self):
        self.limpar_janela()
        self.configurar_fundo() 
        
        self.tabuleiro_p1 = tabuleiro.criar_tabuleiro()
        self.tabuleiro_cpu = tabuleiro.criar_tabuleiro()
        navios.posicionar_todos_navios(self.tabuleiro_p1)
        navios.posicionar_todos_navios(self.tabuleiro_cpu)
        
        self.historico_p1 = set()
        self.historico_cpu = set()
        self.total_jogadas = 0
        self.tiros_certos = 0
        self.tempo_inicio = time.time()
        
        cx = self.winfo_width() // 2
        cy = self.winfo_height() // 2
        
        container_fundo = FrameSombreado(self.canvas, padx=40, pady=40)
        self.canvas.create_window(cx, cy, window=container_fundo, anchor=tk.CENTER)
        
        jogo_container = container_fundo.inner_frame
        
        game_header = tk.Frame(jogo_container, bg=CORES["panel_bg"], pady=15)
        game_header.pack(fill=tk.X)
        
        self.lbl_info = tk.Label(game_header, text="A SUA VEZ! Clique no tabuleiro inimigo.", 
                                 font=("Montserrat", 20, "bold"), fg=CORES["primary"], bg=CORES["panel_bg"])
        self.lbl_info.pack()
        
        play_area = tk.Frame(jogo_container, bg=CORES["panel_bg"], padx=30, pady=30)
        play_area.pack(expand=True, fill=tk.BOTH)
        
        panel_p1 = FrameSombreado(play_area, padx=25, pady=25, bg=CORES["bg"])
        panel_p1.pack(side=tk.LEFT, padx=30, expand=True)
        self.desenhar_grid_estatico(panel_p1.inner_frame, "SEU MAPA", self.tabuleiro_p1)
        
        panel_cpu = FrameSombreado(play_area, padx=25, pady=25, bg=CORES["bg"])
        panel_cpu.pack(side=tk.LEFT, padx=30, expand=True)
        self.desenhar_grid_interativo(panel_cpu.inner_frame, "MAPA INIMIGO")
            
        footer = tk.Frame(jogo_container, bg=CORES["panel_bg"], pady=20)
        footer.pack(fill=tk.X)
        BotaoModerno(footer, text="DESISTIR E VOLTAR", width=25, fg_color=CORES["danger"], command=self.mostrar_menu).pack()

    def desenhar_cabecalho_grid(self, container):
        colunas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for i in range(10):
            tk.Label(container, text=colunas[i], font=self.font_grid, 
                     fg=CORES["text_muted"], bg=container.cget("bg")).grid(row=1, column=i+1, padx=4, pady=8)

    def desenhar_grid_estatico(self, container, titulo, matriz):
        tk.Label(container, text=titulo, font=("Montserrat", 16, "bold"), 
                 fg="white", bg=container.cget("bg")).grid(row=0, column=0, columnspan=11, pady=(0, 20))
        
        self.desenhar_cabecalho_grid(container)
        self.labels_p1 = [] 
        
        for l in range(10):
            tk.Label(container, text=f"{l+1:2d}", font=self.font_grid, 
                     fg=CORES["text_muted"], bg=container.cget("bg")).grid(row=l+2, column=0, padx=(0, 10))
            
            linha_labels = []
            for c in range(10):
                celula = matriz[l][c]
                cor = CORES["agua"]
                txt = ""
                if celula == "N": 
                    cor = CORES["navio_proprio"]
                    txt = "N"

                lbl = tk.Label(container, text=txt, font=self.font_grid, width=5, height=2, 
                               fg="white", bg=cor, relief=tk.FLAT)
                lbl.grid(row=l+2, column=c+1, padx=2, pady=2)
                linha_labels.append(lbl)
            self.labels_p1.append(linha_labels)

    def desenhar_grid_interativo(self, container, titulo):
        tk.Label(container, text=titulo, font=("Montserrat", 16, "bold"), 
                 fg=CORES["danger"], bg=container.cget("bg")).grid(row=0, column=0, columnspan=11, pady=(0, 20))
        
        self.desenhar_cabecalho_grid(container)
        self.labels_cpu = []
        
        def on_enter(e):
            if e.widget.cget("bg") == CORES["agua"]:
                e.widget.config(bg=CORES["shadow_light"])

        def on_leave(e):
            if e.widget.cget("bg") == CORES["shadow_light"]:
                e.widget.config(bg=CORES["agua"])
        
        for l in range(10):
            tk.Label(container, text=f"{l+1:2d}", font=self.font_grid, 
                     fg=CORES["text_muted"], bg=container.cget("bg")).grid(row=l+2, column=0, padx=(0, 10))
            
            linha_labels = []
            for c in range(10):
                lbl = tk.Label(container, text="", font=self.font_grid, width=5, height=2, 
                               bg=CORES["agua"], relief=tk.FLAT, bd=0, cursor="crosshair")
                lbl.grid(row=l+2, column=c+1, padx=2, pady=2)
                
                lbl.bind("<Enter>", on_enter)
                lbl.bind("<Leave>", on_leave)
                lbl.bind("<Button-1>", lambda e, row=l, col=c: self.jogada_jogador(row, col))
                
                linha_labels.append(lbl)
            self.labels_cpu.append(linha_labels)

    def jogada_jogador(self, l, c):
        colunas_letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        coord_texto = f"{colunas_letras[c]}{l+1}"
        
        if coord_texto in self.historico_p1: return
            
        self.historico_p1.add(coord_texto)
        self.total_jogadas += 1
        
        resultado = tabuleiro.dar_tiro(self.tabuleiro_cpu, l, c)
        lbl = self.labels_cpu[l][c]
        
        lbl.unbind("<Enter>")
        lbl.unbind("<Leave>")
        lbl.unbind("<Button-1>")
        lbl.config(cursor="")
        
        if "Acerto" in resultado or "afundado" in resultado:
            lbl.config(bg=CORES["acerto"], text="X", fg="white")
            self.tiros_certos += 1
            cor_msg = CORES["acerto"]
        else:
            lbl.config(bg=CORES["miss"], text="O", fg="white")
            cor_msg = CORES["text"]
            
        self.lbl_info.config(text=f"Míssil em {coord_texto}: {resultado}", fg=cor_msg)
        
        if not tabuleiro.restando_navios(self.tabuleiro_cpu):
            self.update()
            self.fim_de_jogo("Você Venceu! 🎉")
            return
            
        self.lbl_info.config(text="A aguardar resposta inimiga...", fg=CORES["text_muted"])
        self.update() 
        self.after(800, self.jogada_cpu)

    def jogada_cpu(self):
        colunas_letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        l, c = computador.gerar_jogada_aleatoria(self.historico_cpu)
        
        coord_texto = f"{colunas_letras[c]}{l+1}"
        self.historico_cpu.add(coord_texto) 
        
        tabuleiro.dar_tiro(self.tabuleiro_p1, l, c)
        
        lbl = self.labels_p1[l][c]
        if self.tabuleiro_p1[l][c] == 'X':
            lbl.config(bg=CORES["acerto"], text="X", fg="white")
        else:
            lbl.config(bg=CORES["miss"], text="O", fg="white")
        
        self.lbl_info.config(text="A sua vez de atirar!", fg=CORES["primary"])
        self.update()
        
        if not tabuleiro.restando_navios(self.tabuleiro_p1):
            self.fim_de_jogo("O Computador Venceu. 😢")

    def fim_de_jogo(self, mensagem_vencedor):
        tempo_total = int(time.time() - self.tempo_inicio)
        minutos, segundos = divmod(tempo_total, 60)
        
        estatisticas.registrar_partida(
            houve_vitoria=("Você" in mensagem_vencedor),
            acertos_partida=self.tiros_certos,
            total_tiros_partida=len(self.historico_p1)
        )
        
        msg = f"{mensagem_vencedor}\n\nJogadas: {self.total_jogadas}\nTempo: {minutos:02d}:{segundos:02d}"
        messagebox.showinfo("FIM DE PARTIDA", msg)
        self.mostrar_menu()

if __name__ == "__main__":
    app = BatalhaNavalGUI()
    app.mainloop()