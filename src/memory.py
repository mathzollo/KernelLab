"""Simuladores de substituição de páginas."""
def simulate(sequence, frame_count, algorithm):
    if frame_count <= 0: raise ValueError("A quantidade de frames deve ser positiva.")
    if algorithm not in {"FIFO","LRU","Optimal"}: raise ValueError("Algoritmo inválido.")
    frames=[]; rows=[]; faults=0; queue=[]
    for i,page in enumerate(sequence):
        hit=page in frames
        replaced=None
        if not hit:
            faults+=1
            if len(frames)<frame_count:
                frames.append(page)
                queue.append(page)
            else:
                if algorithm=="FIFO":
                    victim=queue.pop(0); idx=frames.index(victim); replaced=victim
                    frames[idx]=page; queue.append(page)
                elif algorithm=="LRU":
                    # Último uso mais antigo entre as páginas atualmente residentes.
                    last_used={f:max(j for j in range(i) if sequence[j]==f) for f in frames}
                    victim=min(frames,key=lambda f:last_used[f]); idx=frames.index(victim); replaced=victim
                    frames[idx]=page
                else:
                    future=sequence[i+1:]
                    next_use={f:(future.index(f) if f in future else float("inf")) for f in frames}
                    victim=max(frames,key=lambda f:next_use[f]); idx=frames.index(victim); replaced=victim
                    frames[idx]=page
        rows.append({"step":i+1,"page":page,"frames":frames.copy(),"hit":hit,"fault":not hit,"replaced":replaced})
    return {"algorithm":algorithm,"steps":rows,"hits":len(sequence)-faults,"faults":faults,
            "fault_rate":round(faults/len(sequence),4) if sequence else 0}

def run_all(sequence, frame_count=4):
    return {a:simulate(sequence,frame_count,a) for a in ("FIFO","LRU","Optimal")}
