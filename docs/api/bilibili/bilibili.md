# API 文档

## 哔哩哔哩

以下POST请求参数均使用raw json格式，例如添加账号接口参数为：`{"id": "test", "cookie": ""}`

### 添加账号

- **功能说明**

用于添加哔哩哔哩账号，cookie最好复制视频详情页中`https://api.bilibili.com/x/v2/reply/wbi/main`接口请求时带的cookie，成功率较高。

- **URL**

  `/bilibili/add_account`

- **Method**

  `POST`

- **Data Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 账户名(用于管理用户cookie) |
| cookie | true | string | 哔哩哔哩cookie |

- **Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 过期账号

- **功能说明**

用于标记账号过期，之后不再使用该账号发送请求。

- **URL**

  `/bilibili/expire_account`

- **Method**

  `POST`

- **Data Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 账户名(用于管理用户cookie) |

- **Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 获取账号列表

- **URL**

  `/bilibili/account_list`

- **Method**

  `GET`

- **URL Params**

  None

- **Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | list | [ [账户信息](#账户信息) ] |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

#### 账户信息

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 账户名(用于管理用户cookie) |
| cookie | true | string | 哔哩哔哩cookie |
| ct | true | int | 创建时间戳 |
| ut | true | int | 更新时间戳 |
| expired | true | int | 0: 有效 1: 过期 (请求失败时自动设为过期) |

### 获取视频详情

- **功能说明**

接口只能获取到视频下载链接。由于哔哩哔哩音视频分离，且需要构造下载请求，如需下载视频，请使用[下载视频](#bilibili视频下载)脚本。

- **URL**

  `/bilibili/detail`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 哔哩哔哩视频id，从网页链接中获取，例如: BV18f421o7zr |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 获取视频评论

- **URL**

  `/bilibili/comments`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 哔哩哔哩视频id |
| offset | false | int | 评论翻页偏移量, 默认0 |
| limit | false | int | 评论数量, 默认10 |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 获取评论回复

- **URL**

  `/bilibili/replys`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 哔哩哔哩视频id，从网页链接中获取，例如: BV18f421o7zr |
| comment_id | true | string | 视频评论id，从评论中获得到的rpid，例如: 215241055632 |
| offset | false | int | 评论翻页偏移量, 默认0 |
| limit | false | int | 评论数量, 默认10 |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 关键词搜索视频

- **URL**

  `/bilibili/search`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| keyword | true | string | 搜索词 |
| offset | false | int | 搜索翻页偏移量, 默认0 |
| limit | false | int | 结果数量, 默认10 |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### bilibili视频下载

- **功能说明**

脚本会自动获取视频下载链接，然后下载视频。[查看示例](https://github.com/ShilongLee/Crawler/wiki/%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9#%E4%B8%8B%E8%BD%BD%E8%A7%86%E9%A2%91)。

- **脚本路径**

script/bilibili/download.py

- **使用方法**

```bash
python3 script/bilibili/download.py --id=<video_id> --dir=<dir> --retain=<retain> --hostport=<hostport>

# id : 视频id，从网页链接中获取，例如: BV18f421o7zr
# dir : 下载目录, 默认为 .cache/bilibili/
# retain : 是否保留下载链接文件, 0: 不保存, 1: 保存, 默认为0
# hostport : crawler服务所在主机端口, 默认为 http://localhost:8080
```

### 用户信息及作品获取

- **URL**

  `/bilibili/user`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 用户id，用户详情页url中获取，例如: 6574487 |
| offset | false | int | 作品翻页偏移量, 默认0 |
| limit | false | int | 作品返回数量, 默认30 |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |
