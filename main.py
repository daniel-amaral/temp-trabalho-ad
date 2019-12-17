import random
import numpy
import queue
import auxiliar.processaeventos as processaeventos
from distribuicoes.exponencial import Exponencial
from entidades.evento import Evento
from entidades.cliente import Cliente
from enums.tipoevento import TipoEvento
from entidades.eventosbag import EventosBag

# recuperando a ultima semente utilizada pelo gerador de numeros aleatorios (se existir)
gerador_numeros_aleatorios = random
nome_arquivo_seed = 'semente/seed'
try:
    seed = open(nome_arquivo_seed, 'r').read()
    gerador_numeros_aleatorios.seed(seed)
except:
    pass

# definicao de taxas:
taxa_chegada_1 = [round(n, 2) for n in numpy.arange(.05, .91, .05)] # 0.05, 0.1, 0.15, . . . , 0.9
taxa_chegada_2 = .2
taxa_servico_1 = 1.0
taxa_servico_2 = .0

# geradores exponenciais para cada tipo de cliente
gerador_exponencial_1 = Exponencial(taxa_chegada_1[0],
                                    taxa_servico_1,
                                    gerador_numeros_aleatorios)
gerador_exponencial_2 = Exponencial(taxa_chegada_2,
                                    taxa_servico_2,
                                    gerador_numeros_aleatorios)

# instanciando cada tipo de evento
evento_chegada_1 = Evento(TipoEvento.chegada_1,
                          gerador_exponencial_1.amostra_taxa_de_chegada)
evento_chegada_2 = Evento(TipoEvento.chegada_2,
                          gerador_exponencial_2.amostra_taxa_de_chegada)
evento_saida_1 = Evento(TipoEvento.saida_1,
                        gerador_exponencial_1.amostra_taxa_de_servico)
evento_saida_2 = Evento(TipoEvento.saida_2,
                        gerador_exponencial_2.amostra_taxa_de_servico)

# estrutura para reutilizar as instâncias de eventos já criadas
eventos_bag = EventosBag(evento_chegada_1,
                         evento_chegada_2,
                         evento_saida_1,
                         evento_saida_2)

# apenas testes
processaeventos.teste()
for _ in range(6):
    print(eventos_bag.evento_chegada_2.instante)

# Inicio da fila
tempo_atual = 0.0
fila = queue.SimpleQueue()
proximo_id = 0
max_atendimentos = 1000 #
eventos_bag.evento_chegada_1.instante()
eventos_bag.evento_chegada_2.instante()


# Primeiro cliente a chegar vai direto para o servidor
if eventos_bag.tipo_proxima_chegada == TipoEvento.chegada_1:
    cliente = Cliente(proximo_id, eventos_bag.evento_chegada_1.instante())# cria o primeiro cliente
    cliente.set_instante_de_atendimento(cliente.instante_de_chegada) # inicio de atendimento igual ao de chegada
    eventos_bag.evento_saida_1.instante() # calcula o tempo de saida
else:
    cliente = Cliente(proximo_id, eventos_bag.evento_chegada_2.instante())  # cria o primeiro cliente
    cliente.set_instante_de_atendimento(cliente.instante_de_chegada)  # inicio de atendimento igual ao de chegada
    eventos_bag.evento_saida_2.instante()  # calcula o tempo de saida
proximo_id += 1

""" Construir abaixo rotina de execução da fila:

while max_atendimentos > 0:
    if eventos_bag.tipo_proxima_chegada == TipoEvento.chegada_1:
        cliente = Cliente(proximo_id, eventos_bag.evento_chegada_1.instante())

    proximo_id += 1
    max_atendimentos -= 1 # mudar esse decremento para quando um cliente sair do sistema
"""








# A semente do gerador de numeros aleatorios eh persistida em arquivo para ser utilizada na proxima execucao do programa
estado_final_do_gerador = gerador_numeros_aleatorios.getstate()
file = open(nome_arquivo_seed, 'w')
file.write(str(estado_final_do_gerador))