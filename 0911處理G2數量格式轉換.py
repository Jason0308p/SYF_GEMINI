import re
import pandas as pd

# 讀取 Excel
df = pd.read_excel(r"C:\Users\syf\Downloads\G2-新建LINE客戶_20250911140455.xlsx")

# 先去除空值列
df = df.dropna(subset=["詢問產品種類子表.1"])

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)

    # 允許的內容：數字、中文字、破折號 - 、波浪號 ~
    # 其他符號一律替換成逗號
    text = re.sub(r"[^0-9\u4e00-\u9fff\-~]", ",", text)

    # 將多個逗號合併成一個
    text = re.sub(r",+", ",", text)

    # 去掉頭尾的逗號
    text = text.strip(",")

    return text

# 建立 B 欄位
df["詢問產品種類子表.2"] = df["詢問產品種類子表.1"].apply(clean_text)

# 輸出 Excel
df.to_excel(r"C:\Users\syf\Downloads\G2_整理後數量.xlsx", index=False)

print("處理完成，結果已存成 G2_整理後數量.xlsx")
