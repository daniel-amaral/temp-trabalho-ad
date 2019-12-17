class Evento():

    def __init__(self, tipo_de_evento, func_gera_amostra):
        self.__tipo_de_evento = tipo_de_evento
        self.__func_gera_amostra = func_gera_amostra
        self.__instante = None

    @property
    def tipo_de_evento(self):
        return self.__tipo_de_evento

    def instante(self):
        """
        Retorna o instante atual e já calcula o tempo do evento seguinte
        """
        if self.__instante is not None:
            ret = self.__instante
            self.__instante += self.__func_gera_amostra()
            return ret
        instante_atual = self.__func_gera_amostra()
        self.__instante = instante_atual + self.__func_gera_amostra()
        return instante_atual

    def set_instante(self, instante):
        self.__instante = instante

    def __lt__(self, other):
        return self.instante < other.instante