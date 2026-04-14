import random

from structures import ArrayClassico

class Carro:
    def __init__(self, x, y, max_avarias):
        self.x = x
        self.y = y
        self.avarias = 0
        self.max_avarias = max_avarias
        self.escudo = 0
        self.passos_dados = 0
        self.bombas_explodidas = 0
        self.modo_pulo = False

    def sofrer_dano(self):
        self.bombas_explodidas += 1
        if self.escudo > 0:
            self.escudo -= 1 
            return False 
        else:
            self.avarias += 1
            if self.avarias >= self.max_avarias:
                return True 
            return False

class Mapa:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.grid = ArrayClassico(tamanho)
        for i in range(tamanho):
            linha = ArrayClassico(tamanho, 0)
            self.grid.definir(i, linha)
            
        self.inicio_x, self.inicio_y = 0, 0
        self.fim_x, self.fim_y = tamanho - 1, tamanho - 1
        
        self.popular_mapa()

    def popular_mapa(self):
        self.grid.obter(self.inicio_y).definir(self.inicio_x, 3)
        self.grid.obter(self.fim_y).definir(self.fim_x, 4)

        qtd_bombas = int((self.tamanho * self.tamanho) * 0.15)
        qtd_escudos = int((self.tamanho * self.tamanho) * 0.05)

        self._espalhar_itens(1, qtd_bombas)
        self._espalhar_itens(2, qtd_escudos)

    def _espalhar_itens(self, tipo, quantidade):
        colocados = 0
        while colocados < quantidade:
            rx = random.randint(0, self.tamanho - 1)
            ry = random.randint(0, self.tamanho - 1)
            if self.grid.obter(ry).obter(rx) == 0:
                self.grid.obter(ry).definir(rx, tipo)
                colocados += 1
