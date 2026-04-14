class ArrayClassico:
    def __init__(self, tamanho, valor_inicial=None):
        self._tamanho = tamanho
        self._dados = [valor_inicial] * tamanho 

# Obter posição do "Array" através do índice
    def obter(self, indice):
        if 0 <= indice < self._tamanho:
            return self._dados[indice]
        raise IndexError(f"Índice {indice} fora dos limites do array")

# Altera um valor no array
    def definir(self, indice, valor):
        if 0 <= indice < self._tamanho:
            self._dados[indice] = valor
        else:
            raise IndexError(f"Índice {indice} fora dos limites do array")

# Exibe o tamanho do array
    def tamanho(self):
        return self._tamanho