# MailTemplate
信件模板自動寄信

## 靈感來源
[觀看影片 (1:25:05)](https://www.youtube.com/watch?v=-bBYmMembAw&t=5105s)

## 問題描述
主要是因為該影片中提到的公關品統計寄發貨等問題發想能不能採用以下方法結合方便日後流程，例如：
- 廠商、客戶基本資料修改
- 公關品或其他公式信件模板修改與自動寄發功能

## 作法簡述
- **建立資料庫：** 設計廠商和客戶的基本資料表（如 SQLite 或 MySQL），並進行資料欄位限制檢查。
- **生成信件樣板：** 使用 `generate_pr_email_template` 函數以 HTML 或其他格式構建信件模板。
- **自動寄信功能：** 使用 `send_email_with_embedded_image` 函數，實現信件自動寄出。
- **其他輔助功能：**
  - `fetch_mailinfo`: 查詢信件相關資料。
  - `check_image_validity`: 檢查圖像路徑是否有效。

## 成果範例
<img src="res/res.jpg" alt="成果圖像" width="800" height="800">
