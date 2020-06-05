# config: utf-8
import time
import utils
import collections
import numpy as np
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Ideia para o treinamento da rede
# entrada: 3 sensores adiante
# saída: acao (pula / não pula)
class ControlaDino(nn.Module):
  def __init__(self):
    super(ControlaDino, self).__init__()
    self.camada1 = nn.Linear(3, 12)
    self.camada2 = nn.Linear(12, 6)
    self.camada3 = nn.Linear(6, 1)

  def forward(self, x):
    x = F.relu(self.camada1(x))
    x = F.relu(self.camada2(x))
    x = self.camada3(x)
    return x

rede = ControlaDino()

# Critério de erros
criterion = nn.MSELoss()

# Otimizador
optimizer = optim.Adam(rede.parameters(), 1e-3)

def treina(entradas, saidas):
  for epoch in range(100):
    for i, entrada in enumerate(entradas):
      entrada = Variable(torch.FloatTensor(entrada), requires_grad=True)
      saida   = Variable(torch.FloatTensor([saidas[i]]), requires_grad=True)
      optimizer.zero_grad()
      saida_da_rede = rede(entrada)
      loss = criterion(saida_da_rede, saida)
      loss.backward()
      optimizer.step()

def get_obstaculo(screen, delta_x = 0):
  # Normaliza os pontos da tela para 0 e 1
  screen = np.ceil(screen.astype(float) / screen.max()).astype(int)
  # Soma os pontos de um retângulo (local onde aparecem os obstáculos)
  return np.sum(screen[56:65, delta_x + 43: delta_x + 49])
 
dino = utils.DinoSeleniumEnv('/usr/bin/chromedriver', 0.001)

def executa_jogo(rede):
  # armazena as ações tomadas 
  entradas = collections.deque(maxlen=100)
  saidas   = collections.deque(maxlen=100)

  # Inicia o jogo
  dino.restart_game()
  dino.resume_game()
  dino.press_up()

  while True:
    screen = dino.grab_screen()

    obstaculo0 = min(1, float(get_obstaculo(screen, -20)))
    obstaculo1 = min(1, float(get_obstaculo(screen)))
    obstaculo2 = min(1, float(get_obstaculo(screen, 20)))
    saida_rede = rede(torch.tensor([obstaculo0, obstaculo1, obstaculo2]))
    acao = saida_rede.item()

    print('ob0: {} - ob1: {} - ob2: {} - acao: {}'.format(obstaculo0, obstaculo1, obstaculo2, acao))

    if acao > 0.5:
      dino.press_up() # pula
      time.sleep(0.3) # delay
   
    if dino.is_crashed():
      return dino.get_score(), entradas, saidas
    else:
      # adiciona apenas pares de entrada/saída de sucesso
      entradas.append([obstaculo0, obstaculo1, obstaculo2])
      saidas.append(acao)
    
    time.sleep(0.1)

# Dados de treinamento iniciais
entradas = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]]
saidas   = [0, 0.1, 0.3, 1]
treina(entradas, saidas)

melhor_score = 5

while True:
  rede.eval() # desliga o modo treinamento
  print('executando outra rodada ...')
  score_rede, entradas_rede, saidas_rede = executa_jogo(rede)
  if score_rede > melhor_score:
    print('Melhor score até agora {}'.format(score_rede))
    melhor_score = score_rede
    entradas += entradas_rede
    saidas += saidas_rede
  # executa outro ciclo de treinamento
  rede.train()
  print('treinando a rede mais uma vez ...')
  treina(entradas, saidas)