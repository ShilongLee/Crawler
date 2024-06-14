# API 文档

## 小红书

以下POST请求参数均使用raw json格式，例如添加账号接口参数为：`{"id": "test", "cookie": ""}`

### 添加账号

- **功能说明**

用于添加小红书账号，cookie最好复制笔记详情页中`https://edith.xiaohongshu.com/api/sns/web/v1/homefeed`接口请求时带的cookie，成功率较高。

- **URL**

  `/xhs/add_account`

- **Method**

  `POST`

- **Data Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 账户名(用于管理用户cookie) |
| cookie | true | string | 小红书cookie |

- **Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 获取账号列表

- **URL**

  `/xhs/account_list`

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
| cookie | true | string | 小红书cookie |
| ct | true | int | 创建时间戳 |
| ut | true | int | 更新时间戳 |
| expired | true | int | 0: 有效 1: 过期 (请求失败时自动设为过期) |

### 获取笔记详情

- **URL**

  `/xhs/detail`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 小红书笔记id，从网页链接中获取，例如: 6653f0820000000005005f9b |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 获取笔记评论

- **URL**

  `/xhs/comments`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 小红书笔记id |
| offset | false | int | 评论翻页偏移量, 默认0 |
| limit | false | int | 评论数量, 默认20 |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 获取评论回复

- **URL**

  `/xhs/replys`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 小红书笔记id，从网页链接中获取，例如: 6653f0820000000005005f9b |
| comment_id | true | string | 笔记评论id，从评论中获得到的id，例如: 6654b9ac000000001c015031 |
| cursor | true | string | 笔记评论游标id，从评论中获得到的sub_comment_cursor，例如: 66551bdb000000001c0248d1 |
| offset | false | int | 评论翻页偏移量, 默认0 |
| limit | false | int | 评论数量, 默认20 |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 关键词搜索笔记

- **URL**

  `/xhs/search`

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
