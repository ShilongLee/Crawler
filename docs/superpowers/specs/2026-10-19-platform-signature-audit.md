# 各平台签名算法现状核实报告

日期：2026-10-19
方式：用本地 Chrome（真实登录态）通过 CDP 探测线上页面运行时状态，并用真实 cookie 实测接口返回。
本文只记录实测结果，不含推测。

## 结论汇总

| 平台 | 签名机制 | 纯 Python 可行性 | 实测状态 |
|---|---|---|---|
| 哔哩哔哩 | wbi：`md5(query + mixin_key)` | ✅ 已是纯 Python | ✅ 实测 `code=0`，20 条结果 |
| 淘宝 | mtop：`md5(token&t&appkey&data)` | ✅ 已是纯 Python | ✅ 签名被接受，但撞登录/设备风控 |
| 微博 | 无请求签名，靠 cookie | ✅ 已是纯 Python | ✅ `ajax/side/hotSearch` 免登录返回 `ok:1` |
| 快手 | GraphQL + `__NS_hxfalcon` | ⚠️ 需 JSVMP 生成的 falcon | ❌ 无 falcon 直接 `"签名验证失败"` |
| 京东 | 搜索页 HTML 解析 | ✅ 无签名 | ❌ 搜索页已被 `京东验证` 拦截 |
| 抖音 | JSVMP 虚拟机（`webmssdk` 1.0.0.20） | ❌ 需移植 37KB VM 解释器 | 未做纯 Python 化 |
| 小红书 | JSVMP 虚拟机（动态下发） | ❌ 字节码每页动态下发 | 未做纯 Python 化 |

## 逐平台实测记录

### 哔哩哔哩：签名算法未变，已验证可用

线上 `nav` 接口返回的 wbi 密钥与仓库内硬编码的完全一致：

```
img_key: 7cd084941338484aae1ad9425b84077c
sub_key: 4932caff0ff746eab6f01bf08b70ac45
mixin_key: ea1db124af3c7062474693fa704f4ff8
```

用该 `mixin_key` 计算 `w_rid` 请求 `x/web-interface/wbi/search/type`：

```
HTTP 200  code=0  message=OK  搜索结果条数=20
```

**sign 函数与 `getMixinKey` 的 salt 顺序表无需改动。** 仅把 UA / `sec-ch-ua` 版本对齐到当前 Chrome。

`dm_img_list` / `dm_img_inter` 等伪设备指纹参数仍然可选，实测不传也能正常返回。

### 淘宝：签名算法未变，但接口已加登录风控

`md5(token & t & appkey & data)` 结构确认有效。用真实 `_m_h5_tk`（形如 `<32位hex>_<13位时间戳>`）签名后请求：

- `mtop.taobao.wsearch.appsearch` → `RGV587_ERROR::SM`
- `mtop.relationrecommend.wirelessrecommend.recommend` → `RGV587_ERROR::SM`

`RGV587` 是登录态/设备风控，**不是签名错误**（签名错误会返回 `FAIL_SYS_ILLEGAL_ACCESS` 或 `TOKEN_EMPTY`）。要真正跑通需要已登录且通过设备校验的 cookie。

`sign()` / `get_token()` 无需改动。

### 微博：无签名，依赖访客 cookie

`https://weibo.com/ajax/side/hotSearch` 不带任何 cookie 即返回 `{"ok":1,...}`。

`m.weibo.cn` 的搜索接口在无访客 cookie 时返回 `Sina Visitor System` 拦截页，需先取访客身份。这是 cookie 层面的事，与签名无关。

`client-version` / `server-version` 两个请求头是 2024 年抓的版本号，实测不影响上述接口；保留但不再作为关键依赖。

### 快手：GraphQL 仍在，但需要 falcon 风控参数

线上页面实际调用的是 REST 接口并带 `__NS_hxfalcon`：

```
/rest/v/profile/get?__NS_hxfalcon=HUDR_...
/rest/v/feed/hot?__NS_hxfalcon=HUDR_...
/rest/v/photo/comment/list
```

不带 falcon 时：

```
/rest/v/feed/hot     -> {"result":2}
/rest/v/profile/get  -> {"result":50,"ab8d":true,"error_msg":"签名验证失败"}
/graphql (POST)      -> {"data":{"result":400002, ... captcha ...}}
```

页面上的生成入口是 `window.kwpsec.getData()`，其源码是 `_ace_` 前缀的 JSVMP 调度器：

```js
function () {_ace_e28e = {_ace_d789d: this || _ace_796b2,_ace_c6403: _ace_e28e,
  _ace_6e75c: arguments,_ace_184c6: _ace_cbec}; _ace_37b52(_ace_71ea5); ... }
```

返回的是 174~218 字符的 base64 串，格式与真实请求里的 `HUDR_...` 不同，**不能直接顶替 falcon**。因此快手无法用纯 Python 生成该参数。

### 京东：搜索页已被验证页替换

```
https://search.jd.com/Search?keyword=test&page=1
  -> HTTP 200, 2696 字节, <title>京东验证</title>, gl-item 出现 0 次
```

`parse_search_html()` 依赖的 `gl-item`、`result_count` 均已不存在。这是页面结构层面的变化，与签名无关。

### 抖音：JSVMP 虚拟机

线上组件与实际版本：

```
webmssdk.es5.js      1.0.0.20
sdk-glue.js          1.0.0.64-fix.01
bdms_1.0.1.19_fix.js 1.0.1.19
```

签名调用链：

```
byted_acrawler.frontierSign(...)
  -> window['_$webrt_1668687510']('484e4f4a403f5243...')
  -> webmssdk.es5.js 内的 VM 解释器(37549 字符)
```

- `frontierSign` 输出 `X-Bogus`（16 字符），三次同输入结果不同（非确定性）。
- `frontierSign` 自身字节码 3057 字节，可完整提取。
- 字节码是**版本化静态资源**，不是每次动态下发。

纯 Python 化需要把 37549 字符的 VM 解释器翻译为 Python 并实现字节码加载器，工作量以天到周计。

### 小红书：JSVMP 虚拟机，字节码动态下发

签名入口 `window._webmsxyw` 与 `window.mnsv2` 均为 100~300 字符的 VM 调度器，真正逻辑在闭包内的解释器与字节码中。

`X-s` 头部结构：

```
XYW_ + base64({"signSvn":"56","signType":"x2","appId":"xhs-pc-web",
               "signVersion":"1","payload":"<464 位 hex>"})
```

外层结构可复现，但 `payload` 由 VM 生成。

VM 宿主由 `https://as.xiaohongshu.com/api/sec/v1/ds?appId=xhs-pc-web` 返回，约 60KB，**每次页面加载动态下发**，开头带下发版本戳（本次为 `1792134232353`）。因此即使移植成功，平台更新后即失效。

## 本次改动范围

- 各平台 `logic/common.py` 的 UA 与 `sec-ch-ua` 版本统一升级到 Chrome 155（线上实际版本）。
- 未改动任何签名算法——经实测，B站、淘宝、微博的签名算法与实现均与线上一致。
- 抖音、小红书继续使用原有 JS 运行时路径，未做纯 Python 化。
