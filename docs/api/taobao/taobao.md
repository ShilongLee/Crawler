# API 文档

## 淘宝

以下POST请求参数均使用raw json格式，例如添加账号接口参数为：`{"id": "test", "cookie": ""}`

### 添加账号

- **功能说明**

用于添加淘宝账号。

- **URL**

  `/taobao/add_account`

- **Method**

  `POST`

- **Data Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 账户名(用于管理用户cookie) |
| cookie | true | string | 淘宝cookie |

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

  `/taobao/expire_account`

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

  `/taobao/account_list`

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
| cookie | true | string | 淘宝cookie |
| ct | true | int | 创建时间戳 |
| ut | true | int | 更新时间戳 |
| expired | true | int | 0: 有效 1: 过期 (请求失败时自动设为过期) |

### 获取商品详情

- **URL**

  `/taobao/detail`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 商品id |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 获取商品评论

- **URL**

  `/taobao/comments`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | string | 商品id |
| offset | false | int | 评论翻页偏移量, 默认0 |
| limit | false | int | 评论数量, 默认20 |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 关键词搜索商品

- **URL**

  `/taobao/search`

- **Method**

  `GET`

- **URL Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| keyword | true | string | 搜索词 |
| offset | false | int | 搜索翻页偏移量, 默认0 |
| limit | false | int | 结果数量, 默认48 |

- **Success Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | struct | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |
