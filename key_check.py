# -*- coding: utf-8 -*-
# KEY_CHECK | 只输出长度/指纹/形状问题,永不输出值
import os, hashlib
EXP = {"OPENROUTER_API_KEY": 73, "DEEPSEEK_API_KEY": 35}
for name, exp in EXP.items():
    k = os.environ.get(name)
    if not k:
        print(f"[{name}] 未设置"); continue
    issues = []
    if k != k.strip(): issues.append("首尾含空白")
    if k[0] in "\"'" or k[-1] in "\"'": issues.append("含引号")
    if name == "OPENROUTER_API_KEY" and k.startswith("sk-") and not k.startswith("sk-or-"):
        issues.append("疑似装反(DeepSeek钥匙)")
    if name == "DEEPSEEK_API_KEY" and k.startswith("sk-or-"):
        issues.append("疑似装反(OpenRouter钥匙)")
    if len(k) != exp: issues.append(f"长度{len(k)}≠预期{exp}")
    fp = hashlib.sha256(k.encode()).hexdigest()[:16]
    print(f"[{name}] len={len(k)} 指纹={fp} 问题={issues or '无'}")
