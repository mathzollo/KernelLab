# Roteiro sugerido — vídeo de até 4 minutos

**0:00–0:25 — Problema:** apresente a MedControl e os problemas de atraso de alarmes, disputa por CPU, faltas de página e concorrência.

**0:25–1:20 — CPU:** execute `python src/main.py`, mostre os quatro escalonadores, o Gantt e as métricas. Explique que o menor número indica maior prioridade e que o quantum do Round Robin é 3.

**1:20–2:10 — Memória:** mostre os quatro frames, a sequência de referências e a comparação de FIFO, LRU e Optimal em hits e faults.

**2:10–2:55 — Dispositivos:** demonstre permissões e a fila exclusiva do disco, explicando que só um processo é proprietário por vez.

**2:55–3:35 — Resultados:** compare os números gerados e relacione-os ao alarme crítico P4. Não invente resultados; use a execução real.

**3:35–4:00 — Conclusão:** apresente a recomendação e as limitações. Informe o link do GitHub e confirme que o README explica como executar.
