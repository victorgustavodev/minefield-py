import tkinter as tk
import random
import time
import os

from structures import ArrayClassico
from entities import Carro, Mapa

class AppMinesweeperCar:
    def __init__(self, root):
        self.root = root
        self.root.title("Campo Minado")
        self.root.geometry("600x750")
        
        self.tamanho_celula = 40
        self.mapa = None
        self.carro = None
        self.tempo_inicio = 0
        self.loop_id = None
        self.jogando = False
        self.visitados = None 
        
        # Correção do Caminho das Imagens (Pega a pasta exata deste script)
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.imagens = {}
        
        try:
            self.imagens['carro'] = tk.PhotoImage(file=os.path.join(diretorio_atual, "assets", "carro.png"))
            self.imagens['bomba'] = tk.PhotoImage(file=os.path.join(diretorio_atual, "assets", "bomba.png"))
            self.imagens['escudo'] = tk.PhotoImage(file=os.path.join(diretorio_atual, "assets", "escudo.png"))
            self.imagens['chao'] = tk.PhotoImage(file=os.path.join(diretorio_atual, "assets", "chao.png"))
        except tk.TclError as e:
            print(f"Aviso: Imagens PNG não encontradas ou formato inválido. Detalhe: {e}")
            print("Usando gráficos nativos aprimorados.")

        self.construir_menu()

    def construir_menu(self):
        self.limpar_tela()
        titulo = tk.Label(self.root, text="CAMPO MINADO", font=("Helvetica", 28, "bold"), fg="#d35400")
        subtitulo = tk.Label(self.root, text="IFPE CAMPUS IGARASSU", font=("Helvetica", 20, "bold"), fg="green")
        titulo.pack(pady=40)
        subtitulo.pack(pady=10)

        lbl = tk.Label(self.root, text="Selecione a dificuldade (Tamanho do Mapa):", font=("Helvetica", 14))
        lbl.pack(pady=10)

        tk.Button(self.root, text="Rápido (10x10)", font=("Helvetica", 12), width=20, bg="#2ecc71", fg="white",
                  command=lambda: self.iniciar_jogo(10)).pack(pady=5)
        tk.Button(self.root, text="Padrão (15x15)", font=("Helvetica", 12), width=20, bg="#f1c40f", fg="black",
                  command=lambda: self.iniciar_jogo(15)).pack(pady=5)
        tk.Button(self.root, text="Insano (20x20)", font=("Helvetica", 12), width=20, bg="#e74c3c", fg="white",
                  command=lambda: self.iniciar_jogo(20)).pack(pady=5)

    def iniciar_jogo(self, tamanho_mapa):
        self.limpar_tela()
        self.jogando = True
        self.mapa = Mapa(tamanho_mapa)
        self.carro = Carro(self.mapa.inicio_x, self.mapa.inicio_y, max_avarias=3)
        
        self.visitados = ArrayClassico(tamanho_mapa)
        for i in range(tamanho_mapa):
            self.visitados.definir(i, ArrayClassico(tamanho_mapa, 0))
        self.visitados.obter(self.carro.y).definir(self.carro.x, 1)

        self.tempo_inicio = time.time()
        
        self.frame_hud = tk.Frame(self.root, bg="#2c3e50", pady=10)
        self.frame_hud.pack(fill=tk.X)

        self.lbl_status = tk.Label(self.frame_hud, text="", font=("Courier", 12, "bold"), bg="#2c3e50", fg="white")
        self.lbl_status.pack()

        self.lbl_pulo = tk.Label(self.frame_hud, text="Modo Pulo (Espaço): DESATIVADO", font=("Courier", 10), bg="#2c3e50", fg="#f1c40f")
        self.lbl_pulo.pack()

        dimensao_canvas = tamanho_mapa * self.tamanho_celula
        self.canvas = tk.Canvas(self.root, width=dimensao_canvas, height=dimensao_canvas, bg="#34495e", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.root.bind("<Up>", lambda e: self.mover(0, -1))
        self.root.bind("w", lambda e: self.mover(0, -1))
        self.root.bind("<Down>", lambda e: self.mover(0, 1))
        self.root.bind("s", lambda e: self.mover(0, 1))
        self.root.bind("<Left>", lambda e: self.mover(-1, 0))
        self.root.bind("a", lambda e: self.mover(-1, 0))
        self.root.bind("<Right>", lambda e: self.mover(1, 0))
        self.root.bind("d", lambda e: self.mover(1, 0))
        self.root.bind("<space>", lambda e: self.alternar_pulo())

        self.atualizar_hud()
        self.desenhar_mapa()

    def alternar_pulo(self):
        if not self.jogando: return
        self.carro.modo_pulo = not self.carro.modo_pulo
        estado = "ATIVADO (Salto no próximo passo)" if self.carro.modo_pulo else "DESATIVADO"
        cor = "#2ecc71" if self.carro.modo_pulo else "#f1c40f"
        self.lbl_pulo.config(text=f"Modo Pulo (Espaço): {estado}", fg=cor)

    def mover(self, dx, dy):
        if not self.jogando: return

        multiplicador = 2 if self.carro.modo_pulo else 1
        novo_x = self.carro.x + (dx * multiplicador)
        novo_y = self.carro.y + (dy * multiplicador)

        if self.carro.modo_pulo:
            self.alternar_pulo() 

        tamanho = self.mapa.grid.tamanho()
        if 0 <= novo_x < tamanho and 0 <= novo_y < tamanho:
            self.carro.x = novo_x
            self.carro.y = novo_y
            self.carro.passos_dados += 1
            self.visitados.obter(novo_y).definir(novo_x, 1)
            
            self.verificar_colisao()
            self.desenhar_mapa()
            
            # CORREÇÃO AQUI: Traz os efeitos (explosão/flash) para a frente do mapa!
            self.canvas.tag_raise("efeito")

    def verificar_colisao(self):
        conteudo = self.mapa.grid.obter(self.carro.y).obter(self.carro.x)
        cx = self.carro.x * self.tamanho_celula + (self.tamanho_celula // 2)
        cy = self.carro.y * self.tamanho_celula + (self.tamanho_celula // 2)

        if conteudo == 1: 
            destruido = self.carro.sofrer_dano()
            self.mapa.grid.obter(self.carro.y).definir(self.carro.x, 0)
            
            # Adicionamos a tag "efeito" na imagem
            if 'bomba' in self.imagens:
                ex_img = self.canvas.create_image(cx, cy, image=self.imagens['bomba'], tags="efeito")
                self.root.after(600, lambda: self.canvas.delete(ex_img))
            else:
                self.animar_explosao(cx, cy, raio=5) 
            
            if destruido:
                self.jogando = False # Trava os controles para o carro não sair de cima da explosão
                self.root.after(600, lambda: self.finalizar_jogo(sucesso=False)) 
                
        elif conteudo == 2: 
            self.carro.escudo += 1
            self.mapa.grid.obter(self.carro.y).definir(self.carro.x, 0)
            
            # Adicionamos a tag "efeito" no brilho
            fundo = self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill="cyan", stipple="gray25", tags="efeito")
            self.root.after(100, lambda: self.canvas.delete(fundo))
            
        elif conteudo == 4: 
            self.finalizar_jogo(sucesso=True)

    def animar_explosao(self, x, y, raio):
        if raio > self.tamanho_celula * 1.5: return 
        cor = random.choice(["#e74c3c", "#d35400", "#f1c40f"])
        
        # Adicionamos a tag "efeito" no círculo da animação
        explosao = self.canvas.create_oval(x-raio, y-raio, x+raio, y+raio, fill=cor, outline="", tags="efeito")
        
        # Garante que os novos círculos animados fiquem no topo
        self.canvas.tag_raise("efeito") 
        
        self.root.after(50, lambda: self.canvas.delete(explosao))
        self.root.after(50, lambda: self.animar_explosao(x, y, raio + 8))

    def desenhar_mapa(self):
        self.canvas.delete("mapa")
        tamanho = self.mapa.grid.tamanho()

        for y in range(tamanho):
            for x in range(tamanho):
                x0, y0 = x * self.tamanho_celula, y * self.tamanho_celula
                x1, y1 = x0 + self.tamanho_celula, y0 + self.tamanho_celula

                visitado = self.visitados.obter(y).obter(x)
                conteudo = self.mapa.grid.obter(y).obter(x)

                if visitado == 1:
                    if 'chao' in self.imagens:
                        self.canvas.create_image(x0+20, y0+20, image=self.imagens['chao'], tags="mapa")
                    else:
                        self.canvas.create_rectangle(x0, y0, x1, y1, fill="#ecf0f1", outline="#bdc3c7", tags="mapa")
                    
                    if conteudo == 2: 
                        if 'escudo' in self.imagens:
                            self.canvas.create_image(x0+20, y0+20, image=self.imagens['escudo'], tags="mapa")
                        else:
                            self.canvas.create_polygon(x0+20, y0+5, x1-5, y0+15, x0+20, y1-5, x0+5, y0+15, fill="cyan", outline="blue", tags="mapa")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#7f8c8d", outline="#2c3e50", width=2, tags="mapa")
                    self.canvas.create_line(x0, y0, x1, y0, fill="#95a5a6", tags="mapa")
                    self.canvas.create_line(x0, y0, x0, y1, fill="#95a5a6", tags="mapa")

                if conteudo == 3: 
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#3498db", outline="", tags="mapa")
                    self.canvas.create_text(x0+20, y0+20, text="INÍCIO", font=("Arial", 8, "bold"), fill="white", tags="mapa")
                elif conteudo == 4: 
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#9b59b6", outline="", tags="mapa")
                    self.canvas.create_text(x0+20, y0+20, text="FIM", font=("Arial", 8, "bold"), fill="white", tags="mapa")

        cx0 = self.carro.x * self.tamanho_celula
        cy0 = self.carro.y * self.tamanho_celula
        
        if 'carro' in self.imagens:
            self.canvas.create_image(cx0+20, cy0+20, image=self.imagens['carro'], tags="mapa")
        else:
            self.canvas.create_rectangle(cx0+8, cy0+10, cx0+32, cy0+30, fill="#e67e22", outline="black", tags="mapa") 
            self.canvas.create_rectangle(cx0+12, cy0+15, cx0+28, cy0+25, fill="#34495e", outline="", tags="mapa") 
            self.canvas.create_rectangle(cx0+5, cy0+12, cx0+8, cy0+18, fill="black", tags="mapa") 
            self.canvas.create_rectangle(cx0+32, cy0+12, cx0+35, cy0+18, fill="black", tags="mapa") 
            self.canvas.create_rectangle(cx0+5, cy0+22, cx0+8, cy0+28, fill="black", tags="mapa") 
            self.canvas.create_rectangle(cx0+32, cy0+22, cx0+35, cy0+28, fill="black", tags="mapa") 

        if self.carro.escudo > 0:
            for i in range(self.carro.escudo): 
                offset = i * 2
                self.canvas.create_oval(cx0+2-offset, cy0+2-offset, cx0+38+offset, cy0+38+offset, outline="#00ffff", width=2, dash=(4, 4), tags="mapa")

    def atualizar_hud(self):
        if not self.jogando: return
        tempo_atual = int(time.time() - self.tempo_inicio)
        resistencia = self.carro.max_avarias - self.carro.avarias
        texto = f"⏱ Tempo: {tempo_atual}s | 🔧 Integridade: {resistencia}/{self.carro.max_avarias} | 🛡 Escudos: {self.carro.escudo}"
        self.lbl_status.config(text=texto)
        self.loop_id = self.root.after(1000, self.atualizar_hud)

    def finalizar_jogo(self, sucesso):
        self.jogando = False
        if self.loop_id:
            self.root.after_cancel(self.loop_id)

        tempo_total = int(time.time() - self.tempo_inicio)
        self.limpar_tela()

        cor_titulo = "#2ecc71" if sucesso else "#e74c3c"
        texto_titulo = "MISSÃO CUMPRIDA!" if sucesso else "VEÍCULO DESTRUÍDO!"

        tk.Label(self.root, text=texto_titulo, font=("Helvetica", 28, "bold"), fg=cor_titulo).pack(pady=40)
        
        frame_stats = tk.Frame(self.root)
        frame_stats.pack(pady=20)

        stats = [
            f"⏱ Tempo Transcorrido: {tempo_total} segundos",
            f"🛣️ Tijolos Percorridos: {self.carro.passos_dados}",
            f"💥 Bombas Explodidas: {self.carro.bombas_explodidas}",
            f"🔧 Avarias Finais: {self.carro.avarias} de {self.carro.max_avarias}"
        ]

        for st in stats:
            tk.Label(frame_stats, text=st, font=("Helvetica", 16)).pack(anchor="w", pady=8)

        tk.Button(self.root, text="Voltar à Base", font=("Helvetica", 14, "bold"), bg="#34495e", fg="white",
                  command=self.construir_menu, width=20).pack(pady=40)

    def limpar_tela(self):
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<space>")
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    janela = tk.Tk()
    app = AppMinesweeperCar(janela)
    janela.mainloop()