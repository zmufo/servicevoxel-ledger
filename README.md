1   # servicevoxel-ledger（服务体素真账）
2   **角色：canonical** — 真相以本仓为准；其余仓库只挂角色章，不存副本。
3   ## 锚链
4   | commit | 事件 | 判定 |
5   |---|---|---|
6   | 3c9e1af | E1 首跑（119 字节假输出） | FAILED · 留痕 |
7   | 54ea5c | E1-fix（360/360 · K_PASS=True） | PASSED |
8   | 68cc215 | Stage2 事实切片（10 工单 10/10） | PASSED |
9   ## 内容
10  sv_full_test.py（E1 结构层）· sv_stage2.py（八态状态机＋事实切片）
11  stage2_run*.txt（双跑证据，按阶段命名，永不覆盖）· key_check.py / l0_smoke.py
12  ## 纪律
13  双跑一致 → 正控 → 哈希 → commit。FAILED 也是账本的一部分。
