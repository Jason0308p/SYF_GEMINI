import pandas as pd
import numpy as np
import re
import random

def parse_specs(description):
    """解析原始描述，將其轉換為結構化的鍵值對列表。"""
    if not isinstance(description, str):
        return []

    # 先將 <br> 轉換為換行符，以便後續處理
    temp_description = re.sub('<br>', '\n', description)
    # 移除所有剩餘的HTML標籤
    clean_description = re.sub('<[^>]*>', '', temp_description)

    specs = []
    lines = clean_description.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = re.split(r'[：】]', line, 1)
        if len(parts) == 2:
            key = re.sub(r'[【 ]', '', parts[0])
            value = parts[1].strip()
            specs.append({'key': key, 'value': value})
    return specs

def process_value(key, value, style_num):
    """根據key和風格編號，對value進行精細處理"""
    # --- 通用清理 ---
    value = value.replace('約', '').replace('*', 'x')

    if key == '常用尺寸':
        # 將 (275x210mm) 格式標準化
        value = re.sub(r'\((\d+.*\d+mm)\)', r' (\1)', value)
        return ' / '.join([v.strip() for v in value.split('/')])

    if key == '封面規格':
        if style_num == 1:
            return value.replace('/', ' (') + ')' if '/' in value else value
        else:
            return value.replace('/', ', ')

    if key == '公版內頁':
        return '、'.join([v.strip() for v in value.split('/')])

    if key == '可選配件':
        return '、'.join([v.strip() for v in value.split('/')])

    if key == '內頁':
        parts = [p.strip() for p in value.split('/')]
        if len(parts) == 2:
            return f"{parts[1]}，{parts[0]}" # 交換順序
        return value

    return value # 默認返回原值

def format_style_1(specs):
    """樣式一：精細處理"""
    output = []
    key_map = {
        '常用尺寸': '尺寸選項', '封面規格': '封面類型', '公版內頁': '內頁格式',
        '客製內容': '客製項目', '皮面加工': 'LOGO加工', '可選配件': '可選附件',
        '內頁尺寸': '內頁大小', '內頁': '內頁規格', '桌檯': '桌曆底座',
        '裝訂': '裝訂方式', '燙印': '加工方式'
    }
    for spec in specs:
        key = spec['key']
        processed_value = process_value(key, spec['value'], 1)
        new_key = key_map.get(key, key)
        output.append(f"<li>{new_key}：{processed_value}</li>")
    return '<ul>\n' + '\n'.join(output) + '\n</ul>'

def format_style_2(specs):
    """樣式二：精細處理"""
    output = []
    key_map = {
        '常用尺寸': '提供尺寸', '封面規格': '材質規格', '公版內頁': '公版選擇',
        '客製內容': '客製範圍', '皮面加工': '表面處理', '可選配件': '選購品項',
        '內頁尺寸': '內頁大小', '內頁': '紙張規格', '桌檯': '底座尺寸',
        '裝訂': '裝訂樣式', '燙印': '印刷工藝'
    }
    for spec in specs:
        key = spec['key']
        processed_value = process_value(key, spec['value'], 2)
        new_key = key_map.get(key, key)
        output.append(f"<li>{new_key}：{processed_value}</li>")
    return '<ul>\n' + '\n'.join(output) + '\n</ul>'

def transform_description(description):
    specs = parse_specs(description)
    if not specs:
        return ""
    style_functions = [format_style_1, format_style_2]
    chosen_style = random.choice(style_functions)
    return chosen_style(specs)

# --- 主程式 ---
input_filename = "C:\\Users\\syf\\Desktop\\my_Gemini_project\\舊站敘述整理\\0825舊站產品資料0804.xlsx"
output_filename = '舊站描述整理成新規格_0828_3.xlsx'

print(f"正在讀取檔案: {input_filename}")
try:
    df = pd.read_excel(input_filename, dtype=str).fillna('')
    print("正在使用強化版腳本處理所有資料...")
    
    # 處理 goods_brief
    df['新規格_brief'] = df['goods_brief'].apply(transform_description)
    # 處理 goods_desc
    df['新規格_desc'] = df['goods_desc'].apply(transform_description)

    # 新增判斷欄位
    df['判斷欄位1'] = np.where(df['新規格_brief'] != '', 1, 0)
    df['判斷欄位2'] = np.where(df['新規格_desc'] != '', 1, 0)
    df['同時有兩規格'] = np.where((df['判斷欄位1'] != 0) & (df['判斷欄位2'] != 0), 1, 0)

    # 刪除 brief 和 desc 皆為空的數據
    df = df[(df['判斷欄位1'] != 0) | (df['判斷欄位2'] != 0)]

    # 輸出結果，包含 brief 和 desc 的原始及處理後欄位，並加入新欄位
    output_df = df[['goods_sn', 'goods_brief', '新規格_brief', '判斷欄位1', 'goods_desc', '新規格_desc', '判斷欄位2']]
    output_df.to_excel(output_filename, index=False)
    
    print(f"處理完成！已將結果儲存至新檔案: {output_filename}")
except FileNotFoundError:
    print(f"錯誤：找不到檔案 '{input_filename}'。")
except Exception as e:
    print(f"處理過程中發生錯誤: {e}")
