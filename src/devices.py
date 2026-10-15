"""Controle de acesso e fila de solicitações a dispositivos."""
from collections import deque
DEVICES = ("disco","rede","audio","logs")
# Permissões ilustrativas para a simulação acadêmica; não representam uma política real.
ACCESS = {
    "P1":{"rede":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False},"audio":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"disco":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"logs":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False}},
    "P2":{"rede":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False},"audio":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"disco":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"logs":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False}},
    "P3":{"disco":{"read":True,"write":True,"execute":False,"use":True,"exclusive":True},"rede":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"audio":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"logs":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False}},
    "P4":{"audio":{"read":False,"write":True,"execute":False,"use":True,"exclusive":True},"rede":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False},"disco":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"logs":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False}},
    "P5":{"disco":{"read":True,"write":True,"execute":False,"use":True,"exclusive":True},"rede":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"audio":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"logs":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False}},
    "P6":{"disco":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False},"rede":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False},"audio":{"read":False,"write":False,"execute":False,"use":False,"exclusive":False},"logs":{"read":True,"write":True,"execute":False,"use":True,"exclusive":False}},
}
def can_access(process_id, device, permission="use"):
    return bool(ACCESS.get(process_id,{}).get(device,{}).get(permission,False))

class DeviceQueue:
    """Fila FIFO com exclusão mútua lógica: apenas um processo detém o dispositivo."""
    def __init__(self, device):
        self.device=device; self.waiting=deque(); self.owner=None; self.events=[]
    def request(self, process_id):
        if self.owner is None:
            self.owner=process_id; self.events.append(f"{process_id} obteve {self.device}")
            return "granted"
        if process_id==self.owner: return "already_owner"
        self.waiting.append(process_id); self.events.append(f"{process_id} entrou na fila de {self.device}")
        return "queued"
    def release(self, process_id):
        if self.owner != process_id: raise PermissionError("Somente o processo proprietário pode liberar o dispositivo.")
        self.events.append(f"{process_id} liberou {self.device}")
        self.owner=self.waiting.popleft() if self.waiting else None
        if self.owner: self.events.append(f"{self.owner} obteve {self.device}")
        return self.owner
