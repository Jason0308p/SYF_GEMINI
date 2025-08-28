import pandas as pd
import re
import random

def parse_specs(description):
    """解析原始描述，將其轉換為結構化的鍵值對列表。"""
    if not isinstance(description, str):
        return []

    specs = []
    # 移除可能的HTML標籤，以簡化解析
    clean_description = re.sub('<br>', '\n', description)
    lines = clean_description.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 處理 【標題】內容 格式
        if '】' in line:
            parts = line.split('】', 1)
            key = parts[0].replace('【', '').strip()
            value = parts[1].strip()
            specs.append({'key': key, 'value': value})
        # 處理 標題：內容 格式
        elif '：' in line:
            parts = line.split('：', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            specs.append({'key': key, 'value': value})
        # 如果沒有特定格式，但看起來是規格，也加進去
        elif re.search(r'\d', line):
             specs.append({'key': '規格', 'value': line})

    return specs

def format_style_1(specs):
    """樣式一：使用 ▪ 和不同的標題"""
    output = []
    key_map = {
        '常用尺寸': '▪ 尺寸選項', '封面規格': '▪ 封面類型', '公版內頁': '▪ 內頁格式',
        '客製內容': '▪ 客製項目', '皮面加工': '▪ LOGO加工', '可選配件': '▪ 可選附件',
        '內頁尺寸': '▪ 內頁大小', '內頁': '▪ 內頁規格', '桌檯': '▪ 桌曆底座',
        '裝訂': '▪ 裝訂方式', '燙印': '▪ 加工方式', '規格': '▪ 規格'
    }
    for spec in specs:
        key = spec['key']
        new_key = key_map.get(key, f"▪ {key}")
        output.append(f"{new_key}：{spec['value']}")
    return '<br>\n'.join(output)

def format_style_2(specs):
    """樣式二：使用 • 和不同的標題"""
    output = []
    key_map = {
        '常用尺寸': '• 規格尺寸', '封面規格': '• 封面材質', '公版內頁': '• 公版內頁',
        '客製內容': '• 客製服務', '皮面加工': '• 表面加工', '可選配件': '• 選購配件',
        '內頁尺寸': '• 內頁尺寸', '內頁': '• 紙張規格', '桌檯': '• 底座規格',
        '裝訂': '• 裝訂', '燙印': '• 燙印處理', '規格': '• 規格'
    }
    for spec in specs:
        key = spec['key']
        new_key = key_map.get(key, f"• {key}")
        output.append(f"{new_key}：{spec['value']}")
    return '<br>\n'.join(output)

def transform_description(description):
    """主轉換函數，解析後隨機選擇一種樣式"""
    specs = parse_specs(description)
    if not specs:
        return ""
    
    # 隨機選擇一種樣式函數
    style_functions = [format_style_1, format_style_2]
    chosen_style = random.choice(style_functions)
    
    return chosen_style(specs)

# --- 主程式 ---
input_filename = '0825舊站產品資料0804.xlsx'
output_filename = 'processed_products_final.xlsx'

print(f"正在讀取檔案: {input_filename}")

try:
    df = pd.read_excel(input_filename, dtype=str).fillna('')

    if 'goods_sn' not in df.columns or 'goods_brief' not in df.columns:
        print("錯誤：Excel 檔案中缺少 'goods_sn' 或 'goods_brief' 欄位。")
    else:
        print("正在處理所有資料，請稍候...")
        
        # 對 'goods_brief' 應用轉換函數
        df['新規格'] = df['goods_brief'].apply(transform_description)
        
        output_df = df[['goods_sn', 'goods_brief', '新規格']]
        
        output_df.to_excel(output_filename, index=False)
        
        print(f"太棒了！全部處理完成，結果已儲存至 {output_filename}")

except FileNotFoundError:
    print(f"錯誤：找不到檔案 '{input_filename}'。")
except Exception as e:
    print(f"處理過程中發生錯誤: {e}")
