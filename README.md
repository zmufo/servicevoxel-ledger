> [!WARNING]
> **本仓为 v1.0 历史账本，已退役，HISTORICAL_LEDGER_ONLY。**
> v1.0 的“正向业务事实校验 / 真相基准”使命已于 2026-11 被证伪：
> 其锚点（哈希、时间戳、内部事实切片）均由被校验方自有系统生成，构成闭环自证，
> 无法满足「事实来源独立于被校验方」这一硬标准。
>
> 当前有效框架：**体元（ServiceVoxel）v2.0 —— 多源独立锚点负向风险筛查器**
> （只提示“值得人工核查的异常线索”，不证明“服务已发生”，也不证明“服务未发生”，不做事实认定，默认不阻断；详见 DEPRECATION.md
>
> 本仓保留全部 Commit / 锚链 / FAILED 留痕，仅作证伪轨迹与工程史档案，
> **请勿将本仓任何“真相基准 / canonical / 已验证”表述用于对外主张。**

# servicevoxel-ledger (ServiceVoxel Canonical Ledger)

Core ledger reference implementation for ServiceVoxel governance protocol. (retracted with v1.0 — see warning above) Mirrors only hold role stamps, never fact copies.

# servicevoxel-ledger（服务体元真账）

**角色：canonical** — 真相以本仓为准；其余仓库只挂角色章，不存副本。

## 锚链

| commit | 事件 | 判定 |
|---|---|---|
| 3c9e1af | E1 首跑（119 字节假输出） | FAILED · 留痕 |
| 54ea5c | E1-fix（360/360 · K_PASS=True） | PASSED |
| 68cc215 | Stage2 事实切片（10 工单 10/10） | PASSED |

## 内容

sv_full_test.py（E1 结构层）· sv_stage2.py（八态状态机＋事实切片）

stage2_run*.txt（双跑证据，按阶段命名，永不覆盖）· key_check.py / l0_smoke.py

## 纪律

双跑一致 → 正控 → 哈希 → commit。FAILED 也是账本的一部分。

---

## 协议声明

本仓库为「体元（ServiceVoxel）」治理协议之核心账本参考实现，遵循以下原则：

1. **事实准入，不存副本**：本仓只挂角色章、不存业务事实副本；真实工单数据不进入本仓。
2. **FAILED 亦为账本一部分**：校验失败记录与成功记录同等留痕，不可擦除。
3. **只验形状，不碰值**：校验脚本（如 `key_check.py`）仅输出长度、指纹、结构问题，永不输出密钥原文。
4. **署名防伪**：本仓所有核心文件均含结构化署名标记，洗稿可追溯。

本仓采用 MIT License 开源，欢迎引用、复用、对抗性审阅。

> 体元协议提出者：曾鑫（Zeng Xin）  
> 研究方向：社区服务与可计算治理  
> 联系：zmufo@126.com  
> 首次冻结版本：V1.0（2026-11-25）