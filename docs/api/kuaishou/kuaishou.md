# API 文档

## 快手

### 添加账号

- **URL**

  `/kuaishou/add_account`

- **Method**

  `POST`

- **URL Params**

  None

- **Data Params**

  **Required:**

  `"id"=[string]` - 账号id, 可填写账号昵称、id等，主要用于区分管理cookie。

  `"cookie"=[string]` - 快手cookie

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : null, "msg" : "OK" }`

### 获取账号列表

- **URL**

  `/kuaishou/account_list`

- **Method**

  `GET`

- **URL Params**

  None

- **Data Params**

  None

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : {}, "msg" : "OK" }`

### 获取视频详情

- **URL**

  `/快手/detail`

- **Method**

  `GET`

- **URL Params**

  **Required:**

  `"id"=[string]` - 快手视频id

- **Data Params**

  None

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : {}, "msg" : "OK" }`

### 获取视频评论(包含子评论)

- **URL**

  `/kuaishou/comments`

- **Method**

  `GET`

- **URL Params**

  **Required:**

  `"id"=[string]` - 快手视频id

  **Optional:**

  `"pcursor"=[string]` - 评论翻页偏移量, 默认0, 从返回中取得下一次的`pcursor`值, 获取子评论时, 请将pcursor设置为返回中的`subCommentsPcursor`

- **Data Params**

  None

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : {}, "msg" : "OK" }`

### 关键词搜索视频

- **URL**

  `/kuaishou/search`

- **Method**

  `GET`

- **URL Params**

  **Required:**

  `"keyword"=[string]` - 搜索关键词

  **Optional:**

  `"pcursor"=[string]` - 搜索结果翻页偏移量, 默认0, 从返回中取得下一次的`pcursor`值

- **Data Params**

  None

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : {}, "msg" : "OK" }`
  