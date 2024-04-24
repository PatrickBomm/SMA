# Simulador de Filas Tandem

## Descrição
Este projeto implementa um simulador de filas tandem, que são filas em série onde a saída de uma é a entrada de outra. Este simulador é útil para análise de sistemas de filas interconectadas, como em linhas de montagem, sistemas de processamento e outros cenários operacionais. O simulador utiliza eventos programados para simular as chegadas e os serviços em duas filas interconectadas, permitindo análise de desempenho e comportamento de filas.

## Estrutura do Projeto

O projeto consiste em três arquivos principais:

- `tandemQueue.py`: Contém a classe `TandemQueue` que implementa a lógica do simulador de filas tandem.
- `main.py`: Script principal que configura e executa simulações usando a classe `TandemQueue`.
- `utils.py`: Inclui funções auxiliares para geração de sementes, cálculo de resultados e escrita de resultados em arquivos.

## Pré-Requisitos

Para executar este projeto, você precisará de:
- Python 3.6 ou superior
- NumPy
- Tabulate

## Você pode instalar as dependências necessárias através do seguinte comando:
pip install numpy tabulate

Configuração e Execução
1 - `Execução do Simulador`:
Execute o arquivo main.py para iniciar a simulação. O comando a seguir pode ser usado para executar o script:
- python main.py

2 - `Dados`:
Forneça os dados das 2 filas para poder continuar a simulação

- Exemplo:
```json
  {
      "Enter arrival limits for queue 1 [min, max]": "1, 4",
      "Enter service limits for queue 1 [min, max]": "3, 4",
      "Enter service limits for queue 2 [min, max]": "2, 3",
      "Enter number of servers in queue 1": 2,
      "Enter capacity of queue 1": 3,
      "Enter number of servers in queue 2": 1,
      "Enter capacity of queue 2": 5,
      "Enter simulation number": 100000
  }

## Resultados:
Os resultados da simulação são escritos em dois arquivos de texto:

- `state_results.txt`: Contém os estados das filas ao longo das simulações.
- `results.txt`: Sumariza os resultados das simulações, incluindo tempos acumulados e probabilidades para cada estado das filas.