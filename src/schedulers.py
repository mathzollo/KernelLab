"""Algoritmos de escalonamento de CPU do KernelLab."""
from collections import deque
from copy import deepcopy

DEFAULT_PROCESSES = [
    {"id":"P1","name":"Monitoramento cardíaco","arrival":0,"burst":8,"priority":1,"memory_mb":120,"devices":["rede"]},
    {"id":"P2","name":"Transmissão de telemetria","arrival":1,"burst":4,"priority":2,"memory_mb":80,"devices":["rede"]},
    {"id":"P3","name":"Geração de relatórios","arrival":2,"burst":9,"priority":4,"memory_mb":200,"devices":["disco"]},
    {"id":"P4","name":"Emissão de alarme crítico","arrival":3,"burst":2,"priority":0,"memory_mb":60,"devices":["audio","rede"]},
    {"id":"P5","name":"Backup do sistema","arrival":5,"burst":12,"priority":5,"memory_mb":300,"devices":["disco"]},
    {"id":"P6","name":"Atualização de dados","arrival":6,"burst":6,"priority":3,"memory_mb":150,"devices":["disco","rede"]},
]

def _prepare(processes):
    ps = deepcopy(processes)
    for p in ps:
        if p["arrival"] < 0 or p["burst"] <= 0:
            raise ValueError("Chegada deve ser >= 0 e burst deve ser > 0.")
    return ps

def _metrics(processes, timeline):
    by_id = {p["id"]: p for p in processes}
    first, finish, executed = {}, {}, {p["id"]: 0 for p in processes}
    last = None
    switches = 0
    for start, end, pid in timeline:
        if pid is None:
            last = None
            continue
        first.setdefault(pid, start)
        finish[pid] = end
        executed[pid] += end - start
        if last is not None and last != pid:
            switches += 1
        last = pid
    rows = []
    for p in processes:
        pid = p["id"]
        completion = finish[pid]
        turnaround = completion - p["arrival"]
        waiting = turnaround - p["burst"]
        response = first[pid] - p["arrival"]
        rows.append({"process":pid,"arrival":p["arrival"],"burst":p["burst"],
                     "priority":p["priority"],"start":first[pid],"completion":completion,
                     "waiting":waiting,"turnaround":turnaround,"response":response})
    n = len(rows) or 1
    averages = {k: round(sum(r[k] for r in rows)/n, 2) for k in ("waiting","turnaround","response")}
    return {"timeline":timeline,"metrics":rows,"averages":averages,"context_switches":switches}

def fcfs(processes):
    ps = _prepare(processes)
    pending = sorted(ps, key=lambda p:(p["arrival"], p["id"]))
    t, timeline = 0, []
    for p in pending:
        if t < p["arrival"]:
            timeline.append((t,p["arrival"],None)); t=p["arrival"]
        timeline.append((t,t+p["burst"],p["id"])); t += p["burst"]
    return _metrics(ps,timeline)

def sjf(processes):
    ps = _prepare(processes)
    remaining = {p["id"]:p["burst"] for p in ps}
    byid = {p["id"]:p for p in ps}
    t, timeline, done = 0, [], set()
    while len(done) < len(ps):
        ready=[p for p in ps if p["id"] not in done and p["arrival"] <= t]
        if not ready:
            nxt=min(p["arrival"] for p in ps if p["id"] not in done)
            timeline.append((t,nxt,None)); t=nxt; continue
        p=min(ready,key=lambda p:(p["burst"],p["arrival"],p["id"]))
        timeline.append((t,t+p["burst"],p["id"])); t+=p["burst"]; done.add(p["id"])
    return _metrics(ps,timeline)

def priority_nonpreemptive(processes):
    ps = _prepare(processes)
    t, timeline, done = 0, [], set()
    while len(done)<len(ps):
        ready=[p for p in ps if p["id"] not in done and p["arrival"]<=t]
        if not ready:
            nxt=min(p["arrival"] for p in ps if p["id"] not in done)
            timeline.append((t,nxt,None)); t=nxt; continue
        p=min(ready,key=lambda p:(p["priority"],p["arrival"],p["id"]))
        timeline.append((t,t+p["burst"],p["id"])); t+=p["burst"]; done.add(p["id"])
    return _metrics(ps,timeline)

def round_robin(processes, quantum=3):
    ps = _prepare(processes)
    if quantum <= 0: raise ValueError("O quantum deve ser maior que zero.")
    arrivals=sorted(ps,key=lambda p:(p["arrival"],p["id"]))
    rem={p["id"]:p["burst"] for p in ps}
    t, i, q, timeline = 0, 0, deque(), []
    while i<len(arrivals) or q:
        if not q and i<len(arrivals) and t<arrivals[i]["arrival"]:
            timeline.append((t,arrivals[i]["arrival"],None)); t=arrivals[i]["arrival"]
        while i<len(arrivals) and arrivals[i]["arrival"]<=t:
            q.append(arrivals[i]); i+=1
        if not q: continue
        p=q.popleft(); run=min(quantum,rem[p["id"]])
        timeline.append((t,t+run,p["id"])); t+=run; rem[p["id"]]-=run
        while i<len(arrivals) and arrivals[i]["arrival"]<=t:
            q.append(arrivals[i]); i+=1
        if rem[p["id"]]>0: q.append(p)
    return _metrics(ps,timeline)

def run_all(processes, quantum=3):
    return {
        "FCFS":fcfs(processes),
        "SJF":sjf(processes),
        "Round Robin":round_robin(processes,quantum),
        "Prioridade (não preemptivo)":priority_nonpreemptive(processes),
    }
