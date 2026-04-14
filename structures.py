class ArrayClassico:
    def __init__(self, tamanho, valor_inicial=None):
        self._tamanho = tamanho
        self._dados = [valor_inicial] * tamanho 

    def obter(self, indice):
        if 0 <= indice < self._tamanho:
            return self._dados[indice]
        raise IndexError(f"Índice {indice} fora dos limites do array")

    def definir(self, indice, valor):
        if 0 <= indice < self._tamanho:
            self._dados[indice] = valor
        else:
            raise IndexError(f"Índice {indice} fora dos limites do array")

    def tamanho(self):
        return self._tamanho