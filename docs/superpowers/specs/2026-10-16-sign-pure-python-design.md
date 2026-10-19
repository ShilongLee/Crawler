# 把抖音、小红书的 JS 环境模拟签名替换为原生 Python 实现

日期：2026-10-16
状态：待确认

## 意图

项目里抖音和小红书两个平台，请求签名不是用算法算出来的，而是**启动一个 JS 运行时执行平台自己的 JS 文件**——即"环境模拟"（补环境）。目标是拆掉这层 JS 运行时，改成原生 Python 直接实现签名算法，同时对齐平台**当前实际**的接口与加密逻辑，而不是沿用仓库里可能已过期的 JS。

豆瓣、微博、快手、淘宝、B站五个平台不涉及 JS 运行时（要么是纯 Python 标准算法，要么就没有签名），**不在本次范围内**。

## 现状（已实测，非推测）

### 涉及 JS 运行时的调用点只有 3 处

| 位置 | 用途 |
|---|---|
| `service/douyin/logic/common.py:60` | `DOUYIN_SIGN = execjs.compile(open('lib/js/douyin.js').read())` |
| `service/xhs/logic/common.py:31` | `xhs_sign_obj = execjs.compile(open('lib/js/xhs.js').read())` |
| `service/xhs/logic/search.py:12` | 每次搜索**又编译一遍** 222KB 的 xhs.js（明显是性能 bug） |

依赖链：`requirements.txt` 里的 `PyExecJS==1.5.1` + 宿主机 Node（`readme.md:53` 明确要求装 nodejs）。`lib/js/douyin.js` 434 行 / 14.9KB，`lib/js/xhs.js` 3714 行 / 222.2KB。

### 抖音 `douyin.js`：可解，已验证

实测在 node 里能正常产出 164 字符的 `a_bogus`。结构清晰：

```
sign_datail(params, ua) = sign(params, ua, [0, 1, 14])
sign(params, ua, args)  = generate_random_str()          // 7 字符随机前缀
                        + generate_rc4_bb_str(params, ua, "1536|747|...", "cus", args)
                        → result_encrypt(result_str, "s4") + "="
```

用到的原语：**自实现 RC4**、**自实现 SM3**（含 `_compress` / `_fill` / 自定义 Tj 常量）、自定义字符编码、`s4` 字母表编码。

**关键实测结论：连跑三次，164 字符输出中只有前 12 位和后 3 位在变，中间约 150 字符完全一致。** 也就是说随机性只来自 `generate_random_str()` 的 7 字符前缀，算法主体是确定性的。这为"逐字节差分对拍"提供了基础——Python 实现与 JS 在相同入参下，主体区必须逐字节相等。

### 小红书 `xhs.js`：已失效，此路不通

实测 `sign()` 内部第 3670 行调用 `window._webmsxyw(uri, params)`，而**该函数在整份文件中没有定义**（全文件仅此一处出现）。因此这份 222KB 的 JS 在当前状态下无法签出任何东西。

文件自报环境为 `x4: "4.20.1"`。结合公开资料，小红书 web 端当前签名机制已迁到 **`mnsv2`**：XXTEA 加密 + 自定义 base64 字母表，约 250 行量级；`x-s-common` 是 `s0`–`x11` 字段的 JSON 再 base64；`x-t` 为毫秒时间戳；`x-b3-traceid` 为 16 位随机 hex。另有 `x-rap-param` 风控头。

**结论：仓库里的小红书 JS 不是"最新接口"，它已经废弃。**

### 另外五个平台的实况（确认无需改动）

- **淘宝**：`sign = md5(token & tme & appkey & data)`，标准 h5 签名，已是纯 Python（`service/taobao/logic/common.py:23`）。
- **微博**、**快手**：无请求签名。
- **B站**：wbi 签名是纯 Python 的 MD5（`service/bilibili/logic/common.py`），另有 `sign_localtion()` / `get_dm_img()` / `random_cacl_1/2()` 生成 `dm_img_list`、`dm_img_inter` 等伪设备指纹——全是 Python 手写常量，不走 JS。

## 目标

1. 抖音 `a_bogus` 用纯 Python 生成，与现有 JS 在相同入参下主体区逐字节一致。
2. 小红书按 `mnsv2` 真实结构用纯 Python 实现 `x-s` / `x-t` / `x-s-common` / `x-b3-traceid`。
3. 移除 `PyExecJS` 依赖与 Node 运行时要求，`execjs` 不再出现在代码中。
4. 顺带修掉 `search.py` 每次重复编译 222KB JS 的问题（替换后自然消失）。
5. 全平台跑一遍整体校验，确认接口是否真的生效。

## 非目标

- 不改动淘宝、微博、快手、B站、京东五个平台。
- 不引入 `xhshow` 等第三方签名库（明确要求自己实现）。
- 不做浏览器自动化/无头浏览器方案——那只是换一种"环境模拟"，与目标相反。
- 不改动请求层、路由、数据模型、数据库结构。

## 约束与风险

### 硬约束：验签样本不足

这是最大的风险，必须提前说清。

- **仓库里的抖音 cookie 已有 700+ 天**（`ct=1733191768`，即 2024-12-03），几乎确定失效。
- **仓库里没有任何小红书 cookie**（`data/xhs/xhs.db` 的 account 表 0 行）。
- `test/cookie.py` 里八个平台的 cookie 全是空串。

推论：**"接口是否生效"这一步无法在没有新凭据的情况下完成。** 需要你自己提供当前登录态的抖音和小红书 cookie。

### 两档做法

| | A 档：离线差分实现 | B 档：对齐当前线上算法 |
|---|---|---|
| 抖音 | 照仓库 434 行 JS 重写为 Python，用差分对拍保证逐字节一致 | 从当前线上 `bdms.js` 重建（JSVMP 虚拟化，需自建 VM 解释器或走差分重建） |
| 小红书 | 无法进行——仓库 JS 已失效 | 按 `mnsv2` 的 XXTEA 结构实现 |
| 验证 | 抖音可离线逐字节验证；小红书无法离线验证 | 需真实 cookie 打真实接口 |
| 风险 | 抖音算法若已轮换，可能被服务端拒 | 工作量大，但唯一可能真正生效的路径 |

公开资料对当前抖音算法的描述是：签名在 `bdms.js` 中，**JSVMP 字节码虚拟化**，用 **SM3**（非 MD5/SHA-256）+ 盐值 `dhzx`，配 RC4 与自定义 64 字符 base64 字母表（`Dkdpgh2ZmsQB80/...`），payload 由「时间戳 + fortnight 索引 + 环境校验和 + 熵 + pageId + aid + 屏尺寸」组装后逐字节 XOR 混合。**输出非确定性**——与服务端校验算法而非固定串的事实一致。版本号聚集在 `1.0.1.19-fix.01`。

注意：以上算法细节来自公开二手资料，**未经本地验证**，仅作方向参考，不作为实现依据。

### 验证策略（无论哪档）

1. **抖音离线对拍**：固定 `Math.random` 使 JS 输出确定化，与 Python 输出逐字节比对主体区（中间 ~150 字符）。这是最强证据。
2. **小红书自洽性测试**：XXTEA 加解密往返、自定义 base64 字母表往返、`x-s-common` 的 JSON 结构还原比对。
3. **真机联调**：提供有效 cookie 后，跑 `test/` 下脚本，看返回码与数据。

### 工具

`rea` MCP 可用于：读取现有 JS 结构、静态解析、以及在需要时驱动本地 node 做对拍。它不能凭空产出"当前线上算法"——那需要有当前线上 JS 的来源。

## 待你确认的决策

**核心问题：走 A 档还是 B 档？**

- 选 A：今天就能动手，抖音有逐字节验证（可靠），小红书得先解决"当前算法从哪来"的问题。
- 选 B：需要你提供一个当前登录态的浏览器（Chrome 开 `--remote-debugging-port`），我用 `rea` 从 `www.xiaohongshu.com` 和 `www.douyin.com` 抓取**当前实际加载的签名代码**，再据此重建。这是唯一能保证"最新"的来源。

## 已定的实现选择（我的判断，非你的要求）

- 把 JS 原语（RC4、SM3）封装进 `lib/crypto/`，两个平台共用，避免各写一份。
- 抖音签名器放 `service/douyin/sign.py`，小红书放 `service/xhs/sign.py`，与 `logic/common.py` 解耦，便于单测。
- 保留 `lib/js/*.js` 文件不删（作为对拍基准留档），但不参与运行时。
- 单测放 `test/`，与现有 `unittest` 风格一致。
