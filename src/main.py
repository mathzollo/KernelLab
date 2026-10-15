"""Ponto de entrada do KernelLab."""
import json, os, sys
from schedulers import DEFAULT_PROCESSES, run_all
from memory import run_all as run_memory
from devices import DeviceQueue, can_access, DEVICES
from metrics import format_schedule

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load_processes():
    path=os.path.join(ROOT,"data","processes.json")
    if os.path.exists(path):
        with open(path,encoding="utf-8") as f: return json.load(f)
    return DEFAULT_PROCESSES

def main():
    processes=load_processes()
    print("="*68+"\n KERNELLAB — SIMULADOR DE RECURSOS DE SISTEMAS OPERACIONAIS\n"+"="*68)
    print("\n[1] ESCALONAMENTO DE CPU")
    schedules=run_all(processes,quantum=3)
    for name,result in schedules.items(): print(format_schedule(name,result))
    print("\n[2] MEMÓRIA VIRTUAL")
    sequence=[1,2,3,4,1,2,5,1,2,3,4,5,2,1,5,3,2]
    for name,result in run_memory(sequence,4).items():
        print(f'{name}: hits={result["hits"]}, faults={result["faults"]}, taxa={result["fault_rate"]:.1%}')
        print("  Frames por referência: "+" | ".join(str(r["frames"]) for r in result["steps"]))
    print("\n[3] CONTROLE DE DISPOSITIVOS")
    print("Permissões de uso por processo:")
    for p in processes:
        allowed=[d for d in DEVICES if can_access(p["id"],d,"use")]
        print(f'  {p["id"]}: {", ".join(allowed) if allowed else "nenhum dispositivo"}')
    q=DeviceQueue("disco")
    print("\nDemonstração de fila exclusiva no disco:")
    for pid in ("P3","P5","P6"): print(f"  Solicitação {pid}: {q.request(pid)}")
    print(f"  Liberação por P3; próximo proprietário: {q.release('P3')}")
    print(f"  Liberação pelo próximo proprietário; próximo: {q.release('P5')}")
    print("\n[4] RECOMENDAÇÃO INICIAL")
    print("Para o alarme crítico (P4), prioridade é uma escolha coerente, pois menor número significa maior prioridade.")
    print("Em produção, considere prioridade preemptiva, prevenção de starvation e validação rigorosa de permissões.")
    print("\nSimulação acadêmica: os tempos e permissões são modelos simplificados, não um SO real.")

if __name__=="__main__": main()
