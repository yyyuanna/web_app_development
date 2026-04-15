# 讀書筆記本（小說專用） 流程圖設計

本文件透過視覺化的方式，說明使用者如何操作本應用程式，以及系統內部資料如何互動。

## 1. 使用者流程圖（User Flow）

此流程圖描述使用者從進入應用程式首頁開始，能夠執行哪些操作、以及頁面之間的跳轉邏輯。

```mermaid
flowchart LR
    A([使用者造訪網頁]) --> B[首頁 - 小說筆記列表]
    
    B --> C{選擇操作}
    
    C -->|關鍵字搜尋| D[使用搜尋列過濾列表]
    D --> B
    
    C -->|點擊「新增筆記」| E[進入新增表單頁面]
    E --> F[輸入書名、作者、心得與評分]
    F -->|送出表單| G{資料驗證成功？}
    G -->|成功| B
    G -->|失敗| E
    
    C -->|點擊特定筆記「編輯」| H[進入編輯表單頁面]
    H --> I[修改筆記資訊]
    I -->|送出更新| G
    
    C -->|點擊特定筆記「刪除」| J{再次確認是否刪除？}
    J -->|確認刪除| B
    J -->|取消刪除| B
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖以「**使用者新增一筆小說紀錄**」為例，說明從前端瀏覽器傳送資料，一路經過後端 Flask 到儲存進 SQLite 資料庫的完整過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (模板 View)
    participant Flask as Flask Route (Controller)
    participant Model as Note Model (資料操作)
    participant DB as SQLite (資料庫)

    User->>Browser: 填寫書名、心得等資料並點擊送出
    Browser->>Flask: POST /add (攜帶表單資料)
    Flask->>Flask: 驗證資料是否完整、評分格式是否為1-5
    
    alt 資料驗證失敗
        Flask-->>Browser: 返回錯誤訊息並保留原輸入內容
    else 資料驗證成功
        Flask->>Model: 呼叫 add_note(書名, 作者, 心得, 評等)
        Model->>DB: INSERT INTO notes ...
        DB-->>Model: 回傳寫入成功
        Model-->>Flask: 操作完成
        Flask-->>Browser: HTTP 302 重新導向至首頁 (/)
        
        Note right of Flask: 接下來是重新渲染首頁的流程
        
        Browser->>Flask: GET /
        Flask->>Model: 撈取最新筆記清單
        Model->>DB: SELECT * FROM notes ORDER BY id DESC
        DB-->>Model: 回傳資料
        Model-->>Flask: 回傳 Python List 物件
        Flask-->>Browser: 回傳最新渲染好的首頁 HTML
        Browser-->>User: 看到新增完成的筆記卡片
    end
```

## 3. 功能清單與路由對照表

此表列出每項系統功能的對應 URL 設計與使用的 HTTP 方法，為接下來的 API 設計及實作打好基礎：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁與清單展示** | `/` | `GET` | 撈取並渲染全數的小說筆記清單。 |
| **搜尋筆記** | `/?search=關鍵字` | `GET` | 透過參數進行「書名」或「作者」的模糊搜尋，並返回過濾清單。 |
| **新增筆記（進入頁面）** | `/add` | `GET` | 顯示新增用的空白表單頁面。 |
| **新增筆記（送出表單）** | `/add` | `POST` | 接收表單送出的資料寫入資料庫，成功後導向 `/`。 |
| **編輯筆記（進入頁面）** | `/edit/<id>` | `GET` | 取得指定 `<id>` 的筆記資料並顯示在表單中。 |
| **編輯筆記（送出表單）** | `/edit/<id>` | `POST` | 接收修改後的表單資料並更新回資料庫，成功後導向 `/`。 |
| **刪除筆記** | `/delete/<id>` | `POST` | 根據指定的 `<id>` 將筆記進行刪除，成功後導向 `/`。（註：避免使用 GET 來設計刪除路由，以防安全問題） |
