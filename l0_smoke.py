# -*- coding: utf-8 -*-
# L0_SMOKE_V0 | 零依赖 | 只证管道通，不证任何主张（agent-track 标签）
import os, json, time, hashlib, urllib.request

PROMPTS = [
    ("A", "只输出一个词：TRUE 或 FALSE。断言：1+1=2", "TRUE"),
    ("B", "只输出一个词：TRUE 或 FALSE。断言：3<2",  "FALSE"),
]
PROVIDERS = [
    ("openrouter", "https://openrouter.ai/api/v1/chat/completions",
     "OPENROUTER_API_KEY", os.environ.get("OPENROUTER_MODEL", "deepseek/deepseek-chat")),
    ("deepseek", "https://api.deepseek.com/chat/completions",
     "DEEPSEEK_API_KEY", os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")),
]

def call(url, key, model, content):
    body = json.dumps({"model": model, "temperature": 0, "max_tokens": 8,
        "messages": [{"role": "user", "content": content}]}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.loads(r.read())
    return out["choices"][0]["message"]["content"].strip(), round(time.time()-t0, 2)

total = match = 0
for name, url, envkey, model in PROVIDERS:
    key = os.environ.get(envkey)
    if not key:
        print(f"[{name}] SKIP: {envkey} 未设置"); continue
    for pid, text, expect in PROMPTS:
        try:
            resp, dt = call(url, key, model, text)
            v = ("TRUE" if resp.upper().startswith("TRUE")
                 else "FALSE" if resp.upper().startswith("FALSE") else "UNPARSABLE")
            ok = (v == expect); total += 1; match += ok
            print(f"[{name}] {pid} model={model} {dt}s verdict={v} "
                  f"expect={expect} MATCH={ok} sha={hashlib.sha256(resp.encode()).hexdigest()[:16]}")
        except Exception as e:
            print(f"[{name}] {pid} FAILED: {type(e).__name__}: {e}")
print(f"[SUMMARY] calls={total} verdict_match={match}/{total}")
