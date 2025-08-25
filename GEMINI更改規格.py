import re
import pandas as pd
import numpy as np

# ---------- 換行正規化 ----------
def normalize_breaks(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # 統一各類換行成 '\n'
    return re.sub(r'(?:<br\s*/?>|_x000D_|\r\n|\r|\n)+', '\n', text, flags=re.IGNORECASE)

# ---------- 移除每行開頭編號（含全形數字/標點） ----------
# 支援: "1. ", "2、", "３．", "４。" 等
NUM_PREFIX_RE = re.compile(r'^\s*[0-9０-９]+[\.、．。]\s*', re.MULTILINE)

def remove_number_prefix(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = normalize_breaks(text)                 # 先正規化換行
    text = NUM_PREFIX_RE.sub('', text)            # 每行行首去編號
    return text.replace('\n', '<br>')             # 若欄位要保留HTML，轉回 <br>

# ---------- 新規格：輸出 <ul><li>，並逐項去編號 ----------
def convert_to_html_list(spec_text: str) -> str:
    if not spec_text:
        return ''
    # 以 <br>（或已被替換的）切段
    parts = [p.strip() for p in spec_text.split('<br>') if p.strip()]
    # 去除每項目前綴編號
    parts = [re.sub(r'^\s*[0-9０-９]+[\.、．。]\s*', '', p) for p in parts]
    if not parts:
        return ''
    return '<ul>' + ''.join(f'<li>{p}</li>' for p in parts) + '</ul>'

# ---------- 從描述中精準抽規格 ----------
def extract_precise_specs(description: str) -> str:
    if not isinstance(description, str):
        return ""

    # 先正規化換行並去掉每行前綴編號（含全形）
    txt = normalize_breaks(description)
    txt = NUM_PREFIX_RE.sub('', txt)

    # 數字+單位（x/* 視為尺寸連接符）
    # Adjusted order: ml before m
    unit_re = re.compile(
        r'\d+(?:\.\d+)?\s*(?:cm|mm|ml|m|g|kg|l|mAh|W|V|A|張|入|組|盒|套|°|公分|英吋|寸|mmHg|kPa|pcs|pc)'
        r'(?:\s*[xX*]\s*\d+(?:\.\d+)?)?',  # 例如 10x20、10*20
        re.IGNORECASE
    )

    # 規格關鍵字
    head_keywords = ('尺寸','規格','材質','重量','容量','厚度','直徑','長度','高度',
                     '張數','電壓','電流','功率','總長','線徑','接口')
    head_keywords_str = '|'.join(head_keywords)

    # Define patterns for specific types of values
    numeric_value_pattern = r'\d+(?:\.\d+)?(?:\s*[xX*]\s*\d+(?:\.\d+)?)?\s*(?:cm|mm|ml|m|g|kg|l|mAh|W|V|A|張|入|組|盒|套|°|公分|英吋|寸|mmHg|kPa|pcs|pc)?'

    # Material values (e.g., "壓克力", "銅版紙", "模造紙", "不銹鋼")
    material_value_pattern = r'(?:壓克力|銅版紙|模造紙|不銹鋼|PU橡膠|PVC|白紙|黃模造紙|304不銹鋼)'

    # Combined spec extraction pattern
    spec_extraction_pattern = re.compile(
        rf'((?:{head_keywords_str})[為:]?\s*(?:{numeric_value_pattern}|{material_value_pattern}))' # Group 1: Keyword + value
        rf'|({numeric_value_pattern})' # Group 2: Standalone numeric value
        rf'|(\d+\s*個卡位)' # Group 3: Specific feature counts
        rf'|(\d+\s*張內頁)' # Group 4: Specific "張內頁"
        rf'|(\d+G\s*(?:銅版紙|白紙|模造紙))' # Group 5: Specific "G" patterns
        , re.IGNORECASE
    )

    extracted_specs = []

    for match in spec_extraction_pattern.finditer(txt):
        spec = None
        # Iterate through capturing groups to find the matched spec
        # Prioritize groups that include keywords
        if match.group(1): # Keyword + value
            spec = match.group(1)
        elif match.group(2): # Standalone numeric value
            spec = match.group(2)
            # If it's a standalone numeric value, try to infer a keyword
            # This is a heuristic and might not always be accurate.
            # Look for a keyword before this spec in the original text (within a small window)
            start_index = match.start()
            search_window = txt[max(0, start_index - 15):start_index] # Look back 15 chars

            found_keyword = None
            # Check for "尺寸", "長度", "厚度", "容量", "重量" specifically
            if unit_re.search(spec): # Only try to infer if it's a unit-containing number
                if "尺寸" in search_window:
                    found_keyword = "尺寸"
                elif "長度" in search_window:
                    found_keyword = "長度"
                elif "厚度" in search_window:
                    found_keyword = "厚度"
                elif "容量" in search_window:
                    found_keyword = "容量"
                elif "重量" in search_window:
                    found_keyword = "重量"
            
            if found_keyword:
                spec = f"{found_keyword}：{spec}" # Add keyword hint

        elif match.group(3): # 個卡位
            spec = match.group(3)
        elif match.group(4): # 張內頁
            spec = match.group(4)
        elif match.group(5): # G + material
            spec = match.group(5)

        if spec:
            spec = spec.strip(' ，,。;；、.\t ')
            spec = re.sub(r'^\s*[0-9０-９]+[\.、．。]\s*', '', spec)
            if spec:
                extracted_specs.append(spec)

    # 移除重複項並保持順序
    unique_specs = list(dict.fromkeys(extracted_specs))

    return '<br>'.join(unique_specs)

# ---------- 讀取資料 ----------
df = pd.read_excel(r'C:\Users\syf\Desktop\my_Gemini_project\J2產品上架表單_20250807143709.xlsx')

# 確保必備欄位存在
for col in ['商品描述', '新規格', '新站商品詳述']:
    if col not in df.columns:
        df[col] = ''

# 統一型別 & 空值
df['商品描述'] = df['商品描述'].fillna('').astype(str)
df['新規格']   = df['新規格'].fillna('').astype(str)
df['新站商品詳述'] = df['新站商品詳述'].fillna('').astype(str)

# ---------- 先處理去編號（商品描述、新站商品詳述） ----------
df['商品描述'] = df['商品描述'].apply(remove_number_prefix)
df['新站商品詳述'] = df['新站商品詳述'].apply(remove_number_prefix)

# ---------- 從「新站商品詳述」萃取【新規格】 ----------
df['【新規格】'] = df['新站商品詳述'].apply(extract_precise_specs)

# ---------- 產生 HTML 版的【新規格】 ----------
df['【新規格】_html'] = df['【新規格】'].apply(convert_to_html_list)

# ---------- 合併「最新導入格式」：有規格(HTML) + 原新站描述 ----------
# 注意：不要用 str([ ... ])，會輸出方括號字元
df['最新導入格式'] = df.apply(lambda r: r.get('【新規格】_html',''), axis=1)

# ---------- 過濾空規格（如需） ----------
df['產品編號'] = df['產品編號'].apply(
    lambda x: "" if str(x).startswith("73AA") or str(x).startswith("74BA") or str(x).startswith('60IA') or str(x).startswith('73ZA') else str(x)
)
df = df[df['產品編號']!='']
df['【新規格】'] = df['【新規格】'].fillna('').astype(str).str.strip()
df = df[df['【新規格】'].str.len() > 0]


# ---------- 指定輸出欄位 ----------
columns_to_keep = [
    '新站商品詳述',          # 已去編號（保留 <br>）
    '【新規格】',            # 純文字（以 <br> 分段）
    '【新規格】_html',       # <ul><li> 版
    '最新導入格式',
    '实例ID',
    '產品編號'
]
final_columns = [c for c in columns_to_keep if c in df.columns]
output_df = df[final_columns]

# ---------- DEBUG（可關閉） ----------
print("--- DEBUG START ---")
print(output_df.head(3).to_string(index=False))
print("--- DEBUG END ---")

# ---------- 存檔 ----------
out_path = r'C:\Users\syf\Desktop\my_Gemini_project\gemini更新規格.xlsx'
output_df.to_excel(out_path, index=False)
print(f"檔案處理完成，已輸出：{out_path}")
