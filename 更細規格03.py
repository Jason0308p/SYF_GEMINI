import re
import pandas as pd
import numpy as np

# ---------- 移除 <br> 後多餘的逗號 ----------
def clean_br_comma(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # 移除 <br> 後面緊跟的全形/半形逗號
    return re.sub(r'(<br>)[，,]\s*', r'\1', text)

# ---------- 移除工單號 / 產品編號（開頭純數字 + <br>） ----------
def remove_order_id(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # 匹配一行開頭純數字（至少 6 碼）+ <br> 或空格
    return re.sub(r'^\s*\d{6,}\s*(<br>|$)', '', text)

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

# ---------- 新增欄位：新站商品詳述（去掉新規格） ----------
def remove_specs_from_desc(row):
    desc = row.get('新站商品詳述', '')
    specs = row.get('【新規格】', '')
    if not desc or not specs:
        return desc
    desc_cleaned = desc
    for spec in specs.split('<br>'):   # 規格是以 <br> 分段的
        spec = spec.strip()
        if spec:
            desc_cleaned = desc_cleaned.replace(spec, '')
    # 移除多餘 <br>
    desc_cleaned = re.sub(r'(<br>\s*)+', '<br>', desc_cleaned).strip('<br>')
    return desc_cleaned

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
import re

def extract_precise_specs(description: str) -> str:
    if not isinstance(description, str):
        return ""

    # 先正規化換行並去掉每行前綴編號（含全形）
    txt = normalize_breaks(description)
    txt = NUM_PREFIX_RE.sub('', txt)

    lines = [ln.strip() for ln in txt.split('\n') if ln.strip()]
    specs = []

    # 開頭常見規格關鍵字
    head_keywords = ('尺寸','規格','材質','重量','容量','厚度','直徑','長度','高度',
                     '張數','電壓','電流','功率','總長','線徑','接口')

    # 數字+單位（x/* 視為尺寸連接符）
    unit_re = re.compile(
        r'\d+(?:\.\d+)?\s*(?:cm|mm|m|g|kg|ml|l|mAh|W|V|A|張|入|組|盒|套|°|公分|英吋|寸|mmHg|kPa|pcs|pc)'
        r'(?:\s*[xX*]\s*\d+(?:\.\d+)?)?',  # 例如 10x20、10*20
        re.IGNORECASE
    )

    # 過濾描述性文字（遇到第一個關鍵詞就截斷）
    discard_words_re = re.compile(
        r'(方便|適合|實用|使用|呈現|展現|提升|增加|專業|美觀|好用|耐用|客製|質感|優點|特色|'
        r'色彩|鮮明|便攜|輕巧|多功能|設計|風格|外觀|品質|精緻|細節|工藝|創新|獨特|時尚|經典|'
        r'優良|耐磨|耐熱|防水|防塵|抗菌|環保|安全|健康|舒適|易清潔|易操作|易安裝|易攜帶|易存儲|'
        r'精美|精選|精心|精細|精確|精湛|高品質|高性能|高效率|高科技|高端|高雅|高貴|高尚|高級|'
        r'豪華|堅固|耐磨損|耐磨耗|專為|專用|專業版|專業設計|專業品質|專業技術|專業工藝|專業製造|'
        r'創意|小巧|輕便|便捷|易用|輕鬆|讓你|讓您|柔軟|觸感|有效|個性|效果|保溫|保冷|保護|防護|'
        r'防滑|防震|防摔|防爆|防火|防盜|廣告|簡易|持久|替換|簡約|大方|可供選擇|一次|滿足|'
        r'可調整|可調節|可擴展|可擴充|採用|效益|附加價值|價值|符合|趨勢|容納|容量|可容納|各式物品|可放置|放置|適中|便於|即時|及時)'
    )

    for line in lines:
        # 判斷是否屬於「規格型」的句子
        if line.startswith(head_keywords) or unit_re.search(line):
            m = discard_words_re.search(line)
            cleaned = (line[:m.start()] if m else line).strip(' ，,。;；、.\t ')
            # 再次防呆去除可能殘留的行首編號
            cleaned = re.sub(r'^\s*[0-9０-９]+[\.、．。]\s*', '', cleaned)
            if cleaned:
                specs.append(cleaned)

    return '<br>'.join(specs)
    if not isinstance(description, str):
        return ""

    # 先處理換行 & 去掉每行編號（避免 "…<br>2. 尺寸…" 抓不到）
    txt = normalize_breaks(description)
    txt = NUM_PREFIX_RE.sub('', txt)

    lines = [ln.strip() for ln in txt.split('\n') if ln.strip()]
    specs = []

    # 開頭常見規格關鍵字
    head_keywords = ('尺寸','規格','材質','重量','容量','厚度','直徑','長度','高度','張數','電壓','電流','功率','總長','線徑','接口')
    # 數字+單位（常見單位盡量cover；x、* 視為尺寸連接符）
    unit_re = re.compile(r'\d+(?:\.\d+)?\s*(cm|mm|m|g|kg|ml|l|mAh|W|V|A|張|入|組|盒|套|°|公分|英吋|寸|mmHg|kPa|pcs|pc|x|X|\*)', re.IGNORECASE)
   # 過濾描述性文字
    discard_words = r'(方便|適合|實用|使用|呈現|展現|提升|增加|專業|美觀|好用|耐用|客製|耐用|質感|優點|特色|色彩|鮮明|便攜|輕巧|多功能|設計|風格|外觀|品質|精緻|細節|工藝|創新|獨特|時尚|經典|品質|優良|耐磨|耐熱|防水|防塵|抗菌|環保|安全|健康|舒適|易清潔|易操作|易安裝|易攜帶|易存儲|精美|精選|精心|精緻|精巧|精美|精細|精確|精湛|精益求精|高品質|高性能|高效率|高科技|高端|高雅|高貴|高尚|高級|豪華|豪華感|豪華版|豪華型號|堅固|堅韌|堅固耐用|堅固型號|堅固版|耐用型號|耐用版|耐磨損|耐磨耗|耐磨損性|耐磨耗性|耐磨損型號|耐磨損版|耐磨耗型號|耐磨耗版|專為|專用|專業版|專業型號|專業設計|專業品質|專業性能|專業技術|專業工藝|專業材料|專業製造|專業品牌|專業認證|專業標準|專業測試|專業評價|專業推薦|創意|創新設計|創新技術|創新材料|創新工藝|創新品牌|創新產品|創新型號|創新版|創新性能|創新品質|創新標準|創新測試|創新評價|創新推薦|小巧|輕便|輕盈|輕巧型號|輕巧版|輕便型號|輕便版|便捷|便捷型號|便捷版|易用|易用型號|易用版|易操作型號|易操作版|易安裝型號|易安裝版|易攜帶型號|易攜帶版|易存儲型號|易存儲版|輕鬆|讓你|讓您|柔軟|觸感|有效|個性|效果|保溫|保冷|保暖|保護|防護|防滑|防震|防摔|防爆|防火|防盜|防盜型號|防盜版|耐磨損性|耐磨耗性|耐磨損型號|耐磨損版|耐磨耗型號|耐磨耗版|廣告|簡易|持久|替換|簡約|大方|可供選擇|可填寫|一次|滿足|可調整|可調節|可調整型號|可調整版|可調節型號|可調節版|可擴展|可擴充|可擴展型號|可擴展版|可擴充型號|可擴充版|多功能型號|多功能版|多用途|多用途型號|多用途版|採用|效益|廣告|增加|附加價值|價值|可分解|取代|塑膠|環保|環保材料|環保型號|環保版|環保設計|環保工藝|環保性能|環保品質|環保標準|環保測試|環保評價|環保推薦|符合|趨勢|適合|效果佳|適合)'

    for line in lines:
        if line.startswith(head_keywords) or unit_re.search(line):
            cleaned = discard_words.split(line)[0].strip()
            if cleaned:
                specs.append(cleaned)
        return '<br>'.join(specs)

# ---------- 讀取資料 ----------
df = pd.read_excel(r'C:\Users\syf\Desktop\my_Gemini_project\J2產品上架表單_20250807143709.xlsx')


# 套用到 新站商品詳述_去規格
df['新站商品詳述'] = df['新站商品詳述'].apply(remove_order_id)

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
df['最新導入格式'] = df.apply(
    lambda r: '<br>'.join([x for x in [r.get('【新規格】_html',''), r.get('新站商品詳述','')] if x]),
    axis=1
)

df['新站商品_描述去規格'] = df.apply(remove_specs_from_desc, axis=1)

df['最新導入格式_描述去除規格版'] = df.apply(
    lambda r: '<br>'.join([x for x in [r.get('【新規格】_html',''), r.get('新站商品_描述去規格','')] if x]),
    axis=1
)

# ---------- 過濾空規格（如需） ----------
df['產品編號'] = df['產品編號'].apply(
    lambda x: "" if str(x).startswith("73AA") or str(x).startswith("74BA") or str(x).startswith('60IA') or str(x).startswith('73ZA') else str(x)
)
df = df[df['產品編號']!='']
df['【新規格】'] = df['【新規格】'].fillna('').astype(str).str.strip()
df = df[df['【新規格】'].str.len() > 0]
df['新站商品_描述去規格'] = df['新站商品_描述去規格'].apply(clean_br_comma)
df['最新導入格式_描述去除規格版'] = df['最新導入格式_描述去除規格版'].apply(clean_br_comma)

# 定義要刪掉的關鍵詞
keywords = ["尺寸", "規格", "重量", "材質", "貨運", "容量", "厚度", "直徑", "長度", "高度", "張數", "電壓", "電流", "功率", "總長", "線徑", "接口", "大","全彩","材質為","日系","內頁","厚度","直徑","長度","高度","張數","電壓","電流","功率","總長","線徑","接口","高","可","原木","背面","企業","精巧","尺寸可","風扇","紳士","韓系","高","兒童","手機","外型","大圓形","運動","可愛","時尚","簡約","經典","多功能","便攜","輕巧","實用","創新","環保","耐用","高品質","高性能","高效率","高科技","高端","高雅","高貴","高尚","豪華","精巧套裝"]

# 直接過濾掉「完全等於」這些詞的列
df = df[~df['【新規格】'].isin(keywords)].copy()



# ---------- 指定輸出欄位 ----------
columns_to_keep = [
    '新站商品詳述',          # 已去編號（保留 <br>）
    '【新規格】',            # 純文字（以 <br> 分段）
    '新站商品_描述去規格',
    '最新導入格式_描述去除規格版',
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
out_path = r'C:\Users\syf\Desktop\my_Gemini_project\更細規格01_完成版.xlsx'
output_df.to_excel(out_path, index=False)
print(f"檔案處理完成，已輸出：{out_path}")
