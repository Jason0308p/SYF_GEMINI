import pandas as pd
import re

def extract_specs(description):
    """
    嘗試從商品簡介中提取規格。
    這個函數是一個範例，您可能需要根據您資料的具體格式來調整裡面的邏輯。
    目前的邏輯是：
    1. 如果描述為空，則返回空字串。
    2. 按換行符號分割文字。
    3. 保留包含冒號、數字、或特殊符號 (■, ●, *) 的行，這些通常是規格。
    4. 移除HTML標籤。
    """
    if not isinstance(description, str):
        return ""

    specs = []
    # 移除HTML標籤
    clean_description = re.sub('<[^<]+?>', '', description)
    
    lines = clean_description.split('\n')
    
    for line in lines:
        line = line.strip()
        # 判斷是否為規格的條件 (包含數字、冒號或特定符號)
        if re.search(r'\d', line) or ':' in line or '：' in line or any(symbol in line for symbol in ['■', '●', '*']):
            if line: # 確保不是空行
                specs.append(line)
    
    return '\n'.join(specs)

# --- 主程式 ---
input_filename = '0825舊站產品資料0804.xlsx'
output_filename = 'output_specifications.xlsx'

print(f"正在讀取檔案: {input_filename}")

try:
    # 讀取 Excel 檔案
    df = pd.read_excel(input_filename)

    # 確保必要的欄位存在
    if 'goods_sn' not in df.columns or 'goods_brief' not in df.columns:
        print("錯誤：Excel 檔案中缺少 'goods_sn' 或 'goods_brief' 欄位。")
    else:
        print("正在處理資料並產生新規格...")
        # 套用函數，建立新欄位
        df['新規格'] = df['goods_brief'].apply(extract_specs)

        # 篩選出最終需要的欄位
        output_df = df[['goods_sn', 'goods_brief', '新規格']]

        # 儲存到新的 Excel 檔案
        output_df.to_excel(output_filename, index=False)

        print(f"處理完成！結果已儲存至 {output_filename}")

except FileNotFoundError:
    print(f"錯誤：找不到檔案 '{input_filename}'。請確認檔案名稱是否正確，且與腳本在同一個資料夾中。")
except Exception as e:
    print(f"處理過程中發生錯誤: {e}")
