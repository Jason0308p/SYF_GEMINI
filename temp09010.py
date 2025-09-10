import pandas as pd
import re

# 讀取 Excel
df = pd.read_excel(r"C:\Users\syf\Downloads\G2原始總表_0910.xlsx")

# 1. 去除空值列（只要兩個欄位其中一個是空的，就刪掉）
df = df.dropna(subset="G2_客人詢問數量")

# 2. 處理「G2_客人詢問數量_關聯」欄位，把裡面的數字抽出來
def extract_numbers(val):
    if pd.isna(val):
        return ""
    # 使用正則表達式取出所有數字
    nums = re.findall(r"\d+", str(val))
    return ",".join(nums)

df["G2_客人詢問數量_關聯"] = df["G2_客人詢問數量_關聯"].apply(extract_numbers)

# 3. 匯出新的 Excel
df.to_excel(r"C:\Users\syf\Downloads\G2導入詢問數量_清理後.xlsx", index=False)
