# API 文档

## 代理

以下POST请求参数均使用raw json格式，例如添加代理接口参数为：`{"urls": ["http://example.com:1234", "http://example2.com:2345"] }`

### 添加代理

- **功能说明**

添加完成后，默认为启用状态(`enable = 1`)。

- **URL**

  `/proxies/add`

- **Method**

  `POST`

- **Data Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| urls | true | [string] | url列表 |

- **Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | false | null | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 移除代理

- **URL**

  `/proxies/remove`

- **Method**

  `POST`

- **Data Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| ids | true | [int] | 需要移除的代理id列表，id可以从代理的list接口获取 |

- **Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | false | null | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 代理列表

- **URL**

  `/proxies/list`

- **Method**

  `GET`

- **URL Params**

  None

- **Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | true | list | [ [代理信息](#代理信息) ] |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

#### 代理信息

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| id | true | int | id(用于管理) |
| url | true | string | 代理地址 |
| ct | true | int | 创建时间戳 |
| ut | true | int | 更新时间戳 |
| enable | true | int | 0: 不启用 1: 启用 |

### 启用代理

- **功能说明**

请求会轮换使用处于启用状态下的代理。

- **URL**

  `/proxies/enable`

- **Method**

  `POST`

- **Data Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| ids | true | [int] | 需要启用的代理id列表，id可以从代理的list接口获取 |

- **Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | false | null | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |

### 禁用代理

- **功能说明**

禁用状态下的代理不会被使用。

- **URL**

  `/proxies/disable`

- **Method**

  `POST`

- **Data Params**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| ids | true | [int] | 需要禁用的代理id列表，id可以从代理的list接口获取 |

- **Response**

| 参数 | 必选 | 类型 | 说明 |
|:---:|:---:|:---:|:---:|
| code | true | int | 0: 成功 1: 参数错误 2: 服务器错误 |
| data | false | null | 数据 |
| msg | true | string | 请求说明(成功、参数错误、服务器错误) |
