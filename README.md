# KernelLab — Simulador de Gerenciamento de Recursos

Projeto acadêmico para a disciplina de Sistemas Operacionais. Simula decisões de escalonamento de CPU, substituição de páginas e controle de acesso a dispositivos no cenário fictício da MedControl Systems.

## Requisitos
- Python 3.10 ou superior
- Não exige bibliotecas externas

## Executar
```bash
python src/main.py
```

## Executar testes
```bash
python -m unittest discover -s tests -v
```

## Estrutura
- `src/schedulers.py`: FCFS, SJF, Round Robin e prioridade não preemptiva.
- `src/memory.py`: FIFO, LRU e Optimal.
- `src/devices.py`: matriz ilustrativa de permissões e fila exclusiva.
- `src/metrics.py`: métricas e Diagrama de Gantt em texto.
- `src/main.py`: execução e apresentação dos resultados.
- `data/processes.json`: dados de processos editáveis.
- `tests/`: testes automatizados.

## Dados de entrada
Edite `data/processes.json`. Cada processo possui:
- `id`: identificador;
- `name`: descrição;
- `arrival`: instante de chegada;
- `burst`: duração total de CPU;
- `priority`: menor valor significa maior prioridade;
- `memory_mb`: memória declarada;
- `devices`: dispositivos relacionados.

O quantum do Round Robin é definido na chamada `run_all(processes, quantum=3)` em `src/main.py`. A sequência de páginas e o número de frames são definidos na seção de memória do mesmo arquivo.

## Algoritmos
- **FCFS**: executa na ordem de chegada.
- **SJF**: escolhe o menor burst entre os processos disponíveis, sem preempção.
- **Round Robin**: divide a CPU em fatias de tempo (quantum), aqui 3 unidades.
- **Prioridade**: escolhe o menor número de prioridade entre os processos disponíveis, sem preempção.
- **FIFO**: remove a página que entrou primeiro.
- **LRU**: remove a página usada há mais tempo.
- **Optimal**: remove a página cujo próximo uso está mais distante (ou que nunca mais será usada).

## Métricas
- **Espera** = retorno − burst.
- **Retorno** = conclusão − chegada.
- **Resposta** = primeira execução − chegada.
- **Page hit**: página já presente nos frames.
- **Page fault**: página ausente dos frames.
- **Taxa de faltas** = page faults / total de referências.
- **Troca de contexto**: contagem de transições diretas entre processos diferentes no timeline; o simulador não contabiliza custos de tempo dessas trocas.

## Limitações
- Modelo de CPU com um único núcleo e bursts fixos; não simula I/O bloqueante nem preempção por prioridade.
- SJF e prioridade são não preemptivos.
- A contagem de trocas de contexto exclui custo de despacho e não conta passagem por períodos ociosos como troca entre processos.
- A matriz de permissões é ilustrativa e deve ser justificada/ajustada no relatório.
- A fila de dispositivos é uma abstração sequencial com exclusão mútua lógica, não threads concorrentes reais.
- O simulador é educacional, não deve controlar dispositivos médicos reais.

## Recomendação inicial
Para a MedControl, a prioridade é reduzir a latência do alarme crítico P4. O escalonamento por prioridade não preemptivo é demonstrado, mas, para um sistema real, seria necessário avaliar prioridade preemptiva, limites de latência, prevenção de starvation e testes de segurança. A decisão final deve ser sustentada pelos resultados medidos.

## Referências
- Material da disciplina de Sistemas Operacionais disponibilizado no AVA.
- Tanenbaum, Andrew S.; Bos, Herbert. *Sistemas Operacionais Modernos*.
- Artigos e páginas sugeridos no enunciado do trabalho.
