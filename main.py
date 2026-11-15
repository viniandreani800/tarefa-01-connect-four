# Jogo Connect Four (Quatro em Linha) - INE5201 / UFSC
# Aluno: Vinicius

import tkinter as tk
from tkinter import messagebox

# Dimensões padrão do Connect Four (6 linhas x 7 colunas)
LINHAS = 6
COLUNAS = 7

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four - INE5201 / UFSC")
        self.root.resizable(False, False)
        
        self.turno = 1  # 1 = Jogador 1 (Vermelho), 2 = Jogador 2 (Amarelo)
        self.tabuleiro = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]
        self.jogo_ativo = True

        # Cabeçalho: Indicador de Turno
        self.label_turno = tk.Label(root, text="Turno: Jogador 1 (Vermelho)", font=("Arial", 14, "bold"), fg="red")
        self.label_turno.pack(pady=10)

        # Área gráfica do tabuleiro (Canvas)
        self.tamanho_celula = 70
        largura = COLUNAS * self.tamanho_celula
        altura = LINHAS * self.tamanho_celula
        
        self.canvas = tk.Canvas(root, width=largura, height=altura, bg="#1a3b8b") # Azul clássico do jogo
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self.clique_coluna)

        # Botão de Reiniciar Jogo
        self.btn_reiniciar = tk.Button(root, text="Reiniciar Jogo", font=("Arial", 11, "bold"), command=self.reiniciar_jogo)
        self.btn_reiniciar.pack(pady=15)

        self.desenhar_tabuleiro()

    def desenhar_tabuleiro(self):
        """Desenha a grelha e as fichas no canvas."""
        self.canvas.delete("all")
        for r in range(LINHAS):
            for c in range(COLUNAS):
                cor = "#f0f0f0" # Cor de espaço vazio (branco/cinza claro)
                if self.tabuleiro[r][c] == 1:
                    cor = "#ff3333" # Vermelho
                elif self.tabuleiro[r][c] == 2:
                    cor = "#ffcc00" # Amarelo
                
                x0 = c * self.tamanho_celula + 10
                y0 = r * self.tamanho_celula + 10
                x1 = x0 + self.tamanho_celula - 20
                y1 = y0 + self.tamanho_celula - 20
                
                self.canvas.create_oval(x0, y0, x1, y1, fill=cor, outline="#0d1b4a", width=3)

    def clique_coluna(self, event):
        """Lida com o clique do jogador numa coluna e aplica a gravidade."""
        if not self.jogo_ativo:
            return

        # Descobre qual a coluna com base na coordenada X do clique
        coluna = event.x // self.tamanho_celula
        
        if 0 <= coluna < COLUNAS:
            # Encontra a linha livre mais abaixo na coluna escolhida (gravidade)
            linha_disponivel = -1
            for r in range(LINHAS - 1, -1, -1):
                if self.tabuleiro[r][coluna] == 0:
                    linha_disponivel = r
                    break
            
            # Se a coluna não estiver cheia
            if linha_disponivel != -1:
                self.tabuleiro[linha_disponivel][coluna] = self.turno
                self.desenhar_tabuleiro()

                # Verifica se este movimento deu vitória
                if self.verificar_vitoria(self.turno):
                    vencedor = "Jogador 1 (Vermelho)" if self.turno == 1 else "Jogador 2 (Amarelo)"
                    messagebox.showinfo("Fim de Jogo", f"Parabéns! {vencedor} venceu a partida!")
                    self.jogo_ativo = False
                    return
                
                # Alterna o turno entre Jogador 1 e Jogador 2
                self.turno = 2 if self.turno == 1 else 1
                if self.turno == 1:
                    self.label_turno.config(text="Turno: Jogador 1 (Vermelho)", fg="red")
                else:
                    self.label_turno.config(text="Turno: Jogador 2 (Amarelo)", fg="#cc9900")

    def verificar_vitoria(self, jogador):
        """Verifica se há 4 fichas alinhadas na horizontal, vertical ou diagonais."""
        # Horizontal
        for r in range(LINHAS):
            for c in range(COLUNAS - 3):
                if all(self.tabuleiro[r][c+i] == jogador for i in range(4)):
                    return True
        # Vertical
        for r in range(LINHAS - 3):
            for c in range(COLUNAS):
                if all(self.tabuleiro[r+i][c] == jogador for i in range(4)):
                    return True
        # Diagonal Principal (crescente /)
        for r in range(3, LINHAS):
            for c in range(COLUNAS - 3):
                if all(self.tabuleiro[r-i][c+i] == jogador for i in range(4)):
                    return True
        # Diagonal Secundária (decrescente \)
        for r in range(LINHAS - 3):
            for c in range(COLUNAS - 3):
                if all(self.tabuleiro[r+i][c+i] == jogador for i in range(4)):
                    return True
        return False

    def reiniciar_jogo(self):
        """Limpa o tabuleiro e reinicia o estado do jogo."""
        self.tabuleiro = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]
        self.turno = 1
        self.jogo_ativo = True
        self.label_turno.config(text="Turno: Jogador 1 (Vermelho)", fg="red")
        self.desenhar_tabuleiro()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFour(root)
    root.mainloop()