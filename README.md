# Rede Neural + Jogo do Dinossauro do Chrome
Essa é uma implementação de uma rede neural, em PyTorch, para aprender e jogar o jogo do dinossauro do chrome.

## Instalação
Para instalar e rodar esse projeto você vai precisar:
1. Clonar esse projeto
2. Instalar as dependências
```bash
git clone https://github.com/brunogamacatao/dino_run_dnn
cd dino_run_dnn
pipenv shell
pip install -r requirements.txt
```
3. É necessário instalar o Chrome Driver do Selenium [nesse link](https://sites.google.com/a/chromium.org/chromedriver/downloads), baixe a versão correta para o seu Chrome (como ver a versão do Chrome? abra o Chrome e vá no link chrome://version)
4. Modifique o arquivo `main.py` linha 34, coloque o caminho completo para o Chrome Driver em seu computador

## Execução
```bash
pithon main.py
```
Vai ser aberta uma janela do Chrome com o jogo do dinossauro. Ele vai executar ciclos de jogo, até o dinossauro colidir com um obstáculo. Ele treinará a rede e vai jogar novamente.

## Considerações
Eu sei, eu sei, essa implementação utiliza um tipo de rede neural (totalmente conectada, não recorrente) que não é mais apropriada para esse tipo de implementação (de repente, uma rede recorrente fosse mais adequada). Eu poderia utilizar outros parâmetros (como por exemplo, a velocidade do jogo), porém, esse é um exemplo simples de como implementar um sistema de controle que aprende com os acertos.
