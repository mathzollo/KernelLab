"""Funções de apresentação de resultados."""
def gantt_ascii(timeline):
    if not timeline: return "(sem execução)"
    parts=[]
    for start,end,pid in timeline:
        label=pid or "IDLE"
        parts.append(f"| {label} [{start}-{end}] ")
    return "".join(parts)+"|"

def format_schedule(name,result):
    lines=[f"\n=== {name} ===",gantt_ascii(result["timeline"]),"Processo | Espera | Retorno | Resposta"]
    for m in result["metrics"]:
        lines.append(f'{m["process"]:7} | {m["waiting"]:6} | {m["turnaround"]:7} | {m["response"]:8}')
    a=result["averages"]
    lines.append(f'Médias: espera={a["waiting"]}, retorno={a["turnaround"]}, resposta={a["response"]}')
    lines.append(f'Trocas de contexto: {result["context_switches"]}')
    return "\n".join(lines)
