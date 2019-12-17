from enums.tipoevento import TipoEvento
from .evento import Evento

class EventosBag():

    def __init__(self,
                 evento_chegada_1 : Evento,
                 evento_chegada_2 : Evento,
                 evento_saida_1 : Evento,
                 evento_saida_2 : Evento):
        self.evento_chegada_1 = evento_chegada_1
        self.evento_chegada_2 = evento_chegada_2
        self.evento_saida_1 = evento_saida_1
        self.evento_saida_2 = evento_saida_2

    @property
    def tipo_proxima_chegada(self):
        return TipoEvento.chegada_1 \
            if self.evento_chegada_1.instante() <= self.evento_chegada_2.instante() \
            else TipoEvento.chegada_2

    @property
    def tempo_proxima_chegada(self):
        return self.evento_chegada_1.instante() \
            if self.tipo_proxima_chegada == TipoEvento.chegada_1 \
            else self.evento_chegada_2.instante()

    @property
    def tipo_proximo_evento(self):
        # TODO: retornar o evento mais próximo
        pass