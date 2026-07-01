# **Sistema Jacobiano de Monitoramento de Singularidades e Controle Adaptativo para o UR10**

## **1\. Descrição do Projeto**

Este projeto implementa duas aplicações práticas baseadas no Jacobiano Geométrico do manipulador industrial UR10, utilizando Python e integração com o simulador URSim por meio da biblioteca RTDE.

O objetivo é demonstrar como propriedades matemáticas do Jacobiano podem ser aplicadas diretamente em problemas reais de controle, desempenho e segurança robótica.

As duas aplicações desenvolvidas são:

1. Sistema de monitoramento ativo de singularidades;  
2. Controle cartesiano adaptativo por pseudo-inversa amortecida do Jacobiano.

## **2\. Aplicação 1 — Monitoramento Ativo de Singularidades**

O sistema calcula continuamente o Jacobiano Geométrico do UR10 e extrai métricas matemáticas associadas à estabilidade cinemática do robô, incluindo:

* número de condição;  
* índice de manipulabilidade;  
* menor valor singular;  
* maior valor singular.

A partir dessas informações, o sistema classifica o estado operacional do robô em quatro níveis:

* NORMAL;  
* ATENÇÃO;  
* RISCO;  
* CRÍTICO.

Conforme o nível de risco identificado, o algoritmo reduz automaticamente o fator de velocidade permitido. Em condição crítica, o sistema interrompe preventivamente o movimento.

## **3\. Aplicação 2 — Controle Cartesiano Adaptativo**

O controlador cartesiano recebe uma velocidade desejada no espaço operacional e calcula as velocidades articulares necessárias por meio da pseudo-inversa amortecida do Jacobiano.

A relação utilizada é:

q\_dot \= k(kappa) J⁺ x\_dot

Nessa expressão:

* q\_dot representa as velocidades articulares;  
* J⁺ representa a pseudo-inversa amortecida do Jacobiano;  
* x\_dot representa a velocidade cartesiana desejada;  
* k(kappa) representa um ganho adaptativo em função do número de condição.

Quando o Jacobiano apresenta bom condicionamento, o ganho permanece elevado. Quando o sistema se aproxima de regiões de singularidade, o ganho é reduzido, tornando o movimento mais seguro e estável.

## **4\. Estrutura dos Arquivos**

projeto\_ur10\_jacobiano/  
│  
├── main.py  
├── ur10\_kinematics.py  
├── jacobian\_tools.py  
├── singularity\_monitor.py  
├── adaptive\_controller.py  
├── data\_logger.py  
├── plot\_results.py  
├── config.py  
├── requirements.txt  
└── README.md

## **5\. Descrição dos Arquivos**

### **main.py**

Arquivo principal do projeto. Integra a leitura das juntas, o cálculo do Jacobiano, o monitoramento de singularidades, o controle adaptativo, o envio de comandos ao robô e o registro dos dados.

### **ur10\_kinematics.py**

Contém o modelo cinemático do UR10, incluindo os parâmetros DH, a cinemática direta e o cálculo do Jacobiano Geométrico 6x6.

### **jacobian\_tools.py**

Contém as ferramentas matemáticas usadas para análise do Jacobiano:

* cálculo dos valores singulares;  
* número de condição;  
* manipulabilidade;  
* pseudo-inversa amortecida;  
* classificação do estado operacional.

### **singularity\_monitor.py**

Implementa o sistema de proteção ativa contra singularidades. Define o nível de risco e o fator de velocidade permitido.

### **adaptive\_controller.py**

Implementa o controlador cartesiano adaptativo. Converte velocidades cartesianas desejadas em velocidades articulares usando a pseudo-inversa amortecida do Jacobiano.

### **data\_logger.py**

Registra os dados da simulação em arquivo CSV, permitindo a geração posterior dos gráficos.

### **plot\_results.py**

Gera automaticamente os gráficos utilizados na análise dos resultados.

### **config.py**

Arquivo de configuração com IP do URSim, frequência de controle, tempo de simulação, amortecimento, velocidade máxima e velocidade cartesiana desejada.

## **6\. Pré-requisitos**

É necessário ter instalado:

* Python 3.9 ou superior;  
* NumPy;  
* Pandas;  
* Matplotlib;  
* ur-rtde;  
* URSim configurado e em execução, caso se deseje testar a comunicação real.

## **7\. Instalação das Dependências**

Execute:

pip install \-r requirements.txt

O arquivo `requirements.txt` deve conter:

numpy  
pandas  
matplotlib  
ur-rtde

## **8\. Configuração do URSim**

No arquivo `config.py`, configure o IP do simulador:

URSIM\_IP \= "192.168.56.101"

Esse IP pode variar conforme a configuração da máquina virtual ou da rede local. Caso o URSim não esteja disponível, o programa executará automaticamente em modo de simulação local.

## **9\. Execução do Projeto**

Para rodar o sistema principal:

python main.py

Durante a execução, o terminal exibirá logs como:

t=03.42s | status=NORMAL   | kappa=  24.83 | manip=0.094521 | gain=1.00  
t=07.88s | status=ATENÇÃO  | kappa=  91.35 | manip=0.031840 | gain=0.60  
t=12.20s | status=RISCO    | kappa= 188.40 | manip=0.010265 | gain=0.25

Ao final, será gerado o arquivo:

dados\_simulacao.csv

## **10\. Geração dos Gráficos**

Após executar o `main.py`, rode:

python plot\_results.py

Os gráficos serão salvos automaticamente na pasta:

figuras/

Serão gerados os seguintes arquivos:

numero\_condicao.png  
manipulabilidade.png  
valores\_singulares.png  
ganho\_adaptativo.png  
velocidades\_articulares.png  
distribuicao\_status.png

## **11\. Interpretação dos Resultados**

O gráfico do número de condição mostra a evolução da estabilidade matemática do Jacobiano ao longo da trajetória.

O gráfico de manipulabilidade mostra a capacidade do manipulador de produzir velocidades cartesianas em diferentes direções.

O gráfico dos valores singulares permite identificar a aproximação de singularidades, principalmente pela redução do menor valor singular.

O gráfico do ganho adaptativo demonstra a atuação do controlador, reduzindo o ganho conforme o robô entra em regiões de pior condicionamento.

O gráfico das velocidades articulares comprova que o controlador converte a velocidade cartesiana desejada em comandos articulares.

A distribuição dos estados mostra quanto tempo o robô permaneceu em cada nível operacional: NORMAL, ATENÇÃO, RISCO ou CRÍTICO.

## **12\. Conclusão**

O projeto demonstra que o Jacobiano Geométrico pode ser utilizado não apenas como ferramenta teórica de cinemática diferencial, mas também como elemento central em sistemas reais de proteção e controle robótico.

A primeira aplicação utiliza o Jacobiano para monitorar singularidades e proteger o robô contra regiões de instabilidade.

A segunda aplicação utiliza a pseudo-inversa amortecida do Jacobiano para realizar controle cartesiano adaptativo, ajustando automaticamente o ganho de acordo com a condição matemática da matriz.

Dessa forma, o trabalho conecta diretamente conceitos matemáticos abstratos ao comportamento físico e operacional de um manipulador industrial UR10.

