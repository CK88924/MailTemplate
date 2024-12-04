# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 21:53:27 2024

@author: user
"""
import sqlite3
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def fetch_mailinfo(db_path, query="SELECT * FROM mailinfo;"):
    """
    從 SQLite 數據庫的 mailinfo 表中查詢數據並以字典形式返回。
    """
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"SQLite 錯誤: {e}")
        return []
    finally:
        if connection:
            connection.close()


def check_image_validity(image_path):
    """
    檢查圖片是否存在以及是否可讀。
    """
    if not os.path.exists(image_path):
        print(f"圖片不存在: {image_path}")
        return False
    try:
        with open(image_path, 'rb') as img_file:
            img_file.read(1)
        print(f"圖片檢查通過: {image_path}")
        return True
    except Exception as e:
        print(f"圖片無法讀取: {e}")
        return False


def send_email_with_embedded_image(to_email, subject, html_body, image_path, from_email, from_password, smtp_server="smtp.gmail.com", smtp_port=587):
    """
    發送帶嵌入圖片的郵件，並返回是否成功。
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        # 嵌入圖片
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            image = MIMEImage(img_data)
            # 設置文件名（解決 noname 問題）
            image.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
            # 設置 Content-ID 以便嵌入郵件 HTML
            image.add_header('Content-ID', '<product_image>')
            msg.attach(image)

        # 發送郵件
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
            print(f"郵件已成功發送至 {to_email}")
            return True  # 發送成功
    except Exception as e:
        print(f"發送郵件至 {to_email} 時出錯: {e}")
        return False  # 發送失敗


def generate_pr_email_template(customername, address, company_email, company_name="您的公司名稱"):
    """
    根據客戶信息生成個性化的 HTML 公關品信件模板。
    """
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>公關品通知信</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                background-color: #f9f9f9;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                font-size: 24px;
                font-weight: bold;
                color: #0056b3;
                text-align: center;
                margin-bottom: 20px;
            }}
            .content p {{
                margin: 10px 0;
            }}
            .product-image {{
                max-width: 100%;
                height: auto;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">公關品通知</div>
            <div class="content">
                <p>尊敬的 <strong>{customername}</strong>，您好：</p>
                <p>
                    我們準備了一份特別的公關品，感謝您對我們的支持。
                    以下是商品的圖片預覽：
                </p>
                <img src="cid:product_image" alt="商品圖片" class="product-image">
                <p>我們將寄送到以下地址：</p>
                <p>{address}</p>
                <p>若有疑問，請聯系我們的郵箱：<a href="mailto:{company_email}">{company_email}</a></p>
                <p>感謝您！</p>
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    db_path = "mail.db"
    results = fetch_mailinfo(db_path)
    
    if not results:
        print("未查詢到有效的客戶數據，程序結束。")
    else:
        from_password = ""#應用程式密碼
        company_email = ""#公司用郵箱
        company_name = ""#公司名
        product_image_path = ""#產品圖路徑

        success_count = 0
        failure_count = 0
        failed_emails = []

        # 檢查圖片是否有效
        if not check_image_validity(product_image_path):
            print("圖片無效，程序結束。")
        else:
            for row in results:
                customername = row['customername']
                address = row['address']
                customer_email = row['email']#客戶郵箱
                print(f"Customer Name: {row['customername']}, Address: {row['address']}, Email: {row['email']}")
                
                email_template = generate_pr_email_template(customername, address, company_email, company_name)
                print(email_template)
                if send_email_with_embedded_image(customer_email, "公關品通知", email_template, product_image_path, company_email, from_password):
                    success_count += 1
                else:
                    failure_count += 1
                    failed_emails.append(customer_email)

        # 打印發送結果
        print(f"成功發送郵件數量: {success_count}")
        print(f"失敗發送郵件數量: {failure_count}")
        if failed_emails:
            print("以下郵件發送失敗：")
            for email in failed_emails:
                print(email)
