# -*- coding: utf-8 -*-
# SV_Stage2_FactSlice_V0 | 零依赖 | 全确定性 | 八态状态机 + 10工单事实切片
STATES = ["CANDIDATE","VALIDATING","VALIDATED","FACT","REJECTED","QUARANTINE","SUPERSEDED","REVOKED"]
LEGAL = {("CANDIDATE","VALIDATING"),("VALIDATING","VALIDATED"),("VALIDATING","REJECTED"),
         ("VALIDATING","QUARANTINE"),("VALIDATED","FACT"),("FACT","SUPERSEDED"),
         ("FACT","REVOKED"),("REJECTED","CANDIDATE"),("QUARANTINE","VALIDATING")}
WHITELIST = {"SENSOR","LEDGER","OPERATOR_LOG","CROSS_TICKET"}
W = [2,1,2,1,2]
VAL_MAX = 48
CROSS_TOL = 10
HARD = {"SVID_INVALID","EVIDENCE_MISSING","VALUE_OUT_OF_RANGE"}

def k_of(core):
    d = [int(core[1]), int(core[3]), int(core[4]), int(core[7]), int(core[10])]
    return (10 - (sum(a*b for a,b in zip(d,W)) % 10)) % 10

def validate(t):
    codes = set()
    svid = t["svid"]
    if not (svid[-1].isdigit() and int(svid[-1]) == k_of(svid.rsplit("-K",1)[0])):
        codes.add("SVID_INVALID")
    if len(t["ev"]) == 0:
        codes.add("EVIDENCE_MISSING")
    if any(s not in WHITELIST for s,_,_ in t["ev"]):
        codes.add("SOURCE_UNTRUSTED")
    eids = [e for _,e,_ in t["ev"]]
    if len(eids) != len(set(eids)):
        codes.add("EVIDENCE_REUSED")
    if any(v < 0 or v > VAL_MAX for _,_,v in t["ev"]):
        codes.add("VALUE_OUT_OF_RANGE")
    vals = [v for _,_,v in t["ev"]]
    if len(vals) >= 2 and max(vals) - min(vals) > CROSS_TOL:
        codes.add("CROSS_INCONSISTENT")
    dv = len({e for s,e,_ in t["ev"] if s in WHITELIST})
    trust = "T0" if codes else ("T2" if dv >= 2 else "T1")
    nxt = "REJECTED" if (codes & HARD) else "QUARANTINE" if codes else None
    return codes, trust, nxt

class Machine:
    def __init__(self):
        self.state = "CANDIDATE"
        self.path = ["CANDIDATE"]
    def go(self, to, audit):
        if (self.state, to) in LEGAL:
            self.state = to
            self.path.append(to)
            return True
        audit.append("ILLEGAL:" + self.state + "->" + to)
        return False

TICKETS = [
 {"id":"N1","svid":"H1-01-Y3-T1-K1","ev":[("SENSOR","ev-001",12),("LEDGER","ev-002",14)],"sc":"normal"},
 {"id":"D1","svid":"H1-01-Y1-T2-K9","ev":[("SENSOR","ev-003",10)],"sc":"normal"},
 {"id":"D2","svid":"H1-01-Y2-T3-K8","ev":[],"sc":"normal"},
 {"id":"D3","svid":"H1-01-Y4-T4-K4","ev":[("WECHAT_SCREENSHOT","ev-004",10)],"sc":"normal"},
 {"id":"D4","svid":"H1-01-Y5-T1-K9","ev":[("SENSOR","ev-005",55)],"sc":"normal"},
 {"id":"D5","svid":"H1-01-Y1-T1-K3","ev":[("SENSOR","ev-006",12),("OPERATOR_LOG","ev-007",38)],"sc":"normal"},
 {"id":"D6","svid":"H1-01-Y2-T1-K2","ev":[("LEDGER","ev-008",20)],"sc":"illegal_skip"},
 {"id":"D7","svid":"H1-01-Y3-T3-K7","ev":[("SENSOR","ev-009",30)],"sc":"revoke"},
 {"id":"D8","svid":"H1-01-Y4-T1-K0","ev":[("LEDGER","ev-010",8)],"sc":"illegal_repromote"},
 {"id":"D9","svid":"H1-01-Y5-T3-K5","ev":[("SENSOR","ev-011",15),("SENSOR","ev-011",15)],"sc":"normal"},
]

def run():
    legal_cnt = sum(1 for a in STATES for b in STATES if (a,b) in LEGAL)
    print("[1] MACHINE_STATES =", len(STATES), " LEGAL_EDGES =", legal_cnt,
          " BLOCKED =", len(STATES)**2 - legal_cnt)
    blocked_attempts = 0
    tally = {}
    trust_tally = {"T0":0,"T1":0,"T2":0}
    for t in TICKETS:
        audit = []
        m = Machine()
        if t["sc"] == "illegal_skip" and not m.go("FACT", audit):
            blocked_attempts += 1
        m.go("VALIDATING", audit)
        codes, trust, bad = validate(t)
        if bad is None:
            m.go("VALIDATED", audit)
            m.go("FACT", audit)
            if t["sc"] == "illegal_repromote" and not m.go("FACT", audit):
                blocked_attempts += 1
            if t["sc"] == "revoke":
                audit.append("EVIDENCE_INVALIDATED")
                m.go("REVOKED", audit)
        else:
            m.go(bad, audit)
        code = sorted(codes)[0] if codes else "NONE"
        if t["sc"] == "revoke" and not codes:
            code = "EVIDENCE_INVALIDATED"
        print(f"  {t['id']} result={'FAIL' if codes else 'PASS'} trust={trust} "
              f"state={m.state} code={code} path={'>'.join(m.path)}")
        if audit:
            print("    audit=" + ";".join(audit))
        assert not (m.state == "FACT" and codes), "T0 reached FACT"
        tally[m.state] = tally.get(m.state, 0) + 1
        trust_tally[trust] += 1
    print("[2] TICKETS =", len(TICKETS), " ILLEGAL_BLOCKED =", blocked_attempts)
    for s in STATES:
        print("    STATE_" + s, "=", tally.get(s, 0))
    for k in ("T0","T1","T2"):
        print("    TRUST_" + k, "=", trust_tally[k])
    print("[3] 结构可计算性 PASS / 真实效果 NOT_TESTED")

if __name__ == "__main__":
    run()
