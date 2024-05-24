# API 文档

## 抖音

### 添加账号

- **URL**

  `/douyin/add_account`

- **Method**

  `POST`

- **URL Params**

  None

- **Data Params**

  **Required:**

  `"id"=[string]` - 账号id, 可填写账号昵称、id等，主要用于区分管理cookie。

  `"cookie"=[string]` - 抖音cookie

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : null, "msg" : "OK" }`

### 获取账号列表

- **URL**

  `/douyin/account_list`

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

  `/douyin/detail`

- **Method**

  `GET`

- **URL Params**

  **Required:**

  `"id"=[string]` - 抖音视频id

- **Data Params**

  None

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : {}, "msg" : "OK" }`

### 获取视频评论

- **URL**

  `/douyin/comments`

- **Method**

  `GET`

- **URL Params**

  **Required:**

  `"id"=[string]` - 抖音视频id

  **Optional:**

  `"offset"=[string]` - 评论翻页偏移量, 默认0

  `"limit"=[string]` - 评论数量, 默认20

- **Data Params**

  None

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : {}, "msg" : "OK" }`

### 获取评论回复

- **URL**

  `/douyin/replys`

- **Method**

  `GET`

- **URL Params**

  **Required:**

  `"video_id"=[string]` - 抖音视频id

  `"comment_id"=[string]` - 抖音评论id

  **Optional:**

  `"offset"=[string]` - 评论翻页偏移量, 默认0

  `"limit"=[string]` - 评论数量, 默认20

- **Data Params**

  None

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : {}, "msg" : "OK" }`

### 关键词搜索视频

- **URL**

  `/douyin/search`

- **Method**

  `GET`

- **URL Params**

  **Required:**

  `"keyword"=[string]` - 搜索关键词

  **Optional:**

  `"offset"=[string]` - 搜索结果翻页偏移量, 默认0

  `"limit"=[string]` - 搜索结果数量, 默认10

- **Data Params**

  None

- **Success Response**

  - **Code:** 200
  - **Content:** `{ "code" : 0, "data" : {}, "msg" : "OK" }`
  