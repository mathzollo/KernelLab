# KernelLab — Relatório Técnico
**Disciplina:** Sistemas Operacionais  
**Projeto:** Simulador de Gerenciamento de CPU, Memória e Dispositivos  
**Integrantes:** [preencher]  
**Instituição:** [preencher]  
**Data:** [preencher]

## 1. Introdução
A MedControl Systems mantém processos de monitoramento, alarmes, transmissão de dados, relatórios, backup e atualização. O cenário descreve atrasos em alarmes, disputa por CPU, faltas de página, espera excessiva e concorrência no acesso a dispositivos. O KernelLab foi proposto para simular políticas de gerenciamento e comparar seus resultados.

## 2. Objetivo
Implementar uma aplicação educacional que simule quatro políticas de escalonamento, três algoritmos de substituição de páginas e um mecanismo simples de controle de acesso e exclusão mútua para dispositivos.

## 3. Processos e premissas
O projeto utiliza os seis processos fornecidos no enunciado. A CPU é única; o menor número representa maior prioridade; Round Robin usa quantum 3. SJF e prioridade foram implementados sem preempção. Essas premissas devem ser explicitadas ao interpretar os resultados.

## 4. Escalonamento de CPU
- **FCFS:** atende os processos pela ordem de chegada. É simples, mas processos curtos podem esperar atrás de um processo longo.
- **SJF:** escolhe o menor burst entre os processos já disponíveis. Pode reduzir a espera média, mas pode prejudicar tarefas longas.
- **Round Robin:** entrega fatias de CPU de até três unidades, favorecendo alternância e resposta interativa; há mais trocas de contexto.
- **Prioridade:** escolhe o menor número de prioridade entre os processos disponíveis. Favorece o alarme P4 (prioridade 0), mas uma versão não preemptiva não interrompe um processo que já começou.

As métricas apresentadas pelo programa são espera (retorno menos burst), retorno (conclusão menos chegada) e resposta (primeira execução menos chegada). O Diagrama de Gantt e as médias devem ser copiados da execução final para as tabelas do relatório.

## 5. Gerenciamento de memória
O simulador utiliza quatro frames e a sequência de referências fornecida. FIFO substitui a página mais antiga em memória; LRU substitui a página cujo uso anterior é mais distante; Optimal substitui a página cujo próximo uso está mais distante. Optimal é uma referência teórica porque depende de conhecer a sequência futura. Registre a tabela completa de frames, hits, faults e taxa de faltas gerada pelo programa.

## 6. Controle de dispositivos e segurança
O programa inclui uma matriz ilustrativa de permissões para disco, rede, áudio e logs. A fila de dispositivo representa pedidos concorrentes e mantém um único proprietário por vez. O mutex/semaforização é modelado por regras de estado sequenciais; não equivale a sincronização de threads reais. Em um sistema real, as permissões deveriam seguir menor privilégio, autenticação, auditoria e validação por recurso.

## 7. Resultados e análise
Preencher após executar `python src/main.py`:
- Menor tempo médio de espera: [algoritmo e valor]
- Melhor tempo médio de resposta: [algoritmo e valor]
- Melhor resultado de memória: [algoritmo e page faults]
- Trocas de contexto: [comparação]
- Consequências para o alarme P4: [análise]
- Riscos de starvation e justiça: [análise baseada nos resultados]

## 8. Recomendação técnica
A recomendação deve ponderar a criticidade do alarme, espera média, resposta, justiça e risco de starvation. A prioridade é relevante para P4, mas o modelo não preemptivo pode não ser suficiente para garantir resposta rápida quando a CPU já está ocupada. Uma versão futura poderia implementar prioridade preemptiva com envelhecimento (aging), bloqueio real de I/O e gráficos.

## 9. Limitações
O KernelLab é um simulador acadêmico. Não representa todos os comportamentos de um sistema operacional, não simula o custo real das trocas de contexto e não deve ser utilizado em sistemas médicos reais. A matriz de permissões é uma política didática, não uma política validada pela MedControl.

## 10. Conclusão
O projeto demonstra como políticas diferentes afetam o uso da CPU, o comportamento da memória e o acesso a dispositivos. A conclusão final deve citar os resultados medidos e justificar a política escolhida para o cenário.

## Referências
- Materiais da disciplina Sistemas Operacionais disponíveis no AVA.
- TANENBAUM, Andrew S.; BOS, Herbert. *Sistemas Operacionais Modernos*.
- Demais referências indicadas no enunciado da atividade.
