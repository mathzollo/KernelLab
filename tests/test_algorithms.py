import os, sys, unittest
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
from schedulers import DEFAULT_PROCESSES, fcfs, sjf, round_robin, priority_nonpreemptive
from memory import simulate
from devices import DeviceQueue, can_access

class TestKernelLab(unittest.TestCase):
    def test_fcfs_completes_all(self):
        r=fcfs(DEFAULT_PROCESSES)
        self.assertEqual(len(r["metrics"]),6)
        self.assertTrue(all(m["waiting"]>=0 for m in r["metrics"]))
    def test_rr_quantum(self):
        r=round_robin(DEFAULT_PROCESSES,3)
        self.assertEqual(len(r["metrics"]),6)
    def test_memory_counts(self):
        seq=[1,2,3,4,1,2,5,1,2,3,4,5,2,1,5,3,2]
        r=simulate(seq,4,"FIFO")
        self.assertEqual(r["hits"]+r["faults"],len(seq))
    def test_device_exclusion(self):
        q=DeviceQueue("disco")
        self.assertEqual(q.request("P3"),"granted")
        self.assertEqual(q.request("P5"),"queued")
        self.assertEqual(q.release("P3"),"P5")
    def test_access(self):
        self.assertTrue(can_access("P4","audio","use"))
        self.assertFalse(can_access("P1","audio","use"))

if __name__=="__main__": unittest.main()
