import pandas as pd
import re

# 將新規格文字轉成 HTML <ul><li> 列點
def convert_to_html_list(spec_text):
    if not spec_text:
        return ''
    items = spec_text.split('<br>')
    list_items = ''.join([f'<li>{item.strip()}</li>' for item in items if item.strip()])
    return f'<ul>{list_items}</ul>'

# 從商品描述中提取規格相關欄位
# def extract_specs_for_new_column(description):
#     if not isinstance(description, str):
#         return ""
#     cleaned_description = re.sub(r'<br>_x000D_\n|<br>|\n', '\n', description)
#     lines = cleaned_description.splitlines()
#     spec_lines = []
#     keywords = ['規格', '尺寸', '材質', '工藝', '包裝', '重量','電流','總長','線徑','接口','電壓','功率','mm','ml','mAh','cm','厚度','高度','公分','英吋','檔位','直徑','尺寸為','材質為','尺寸長','尺寸:',] 

#     for line in lines:
#         stripped_line = line.strip()
#         for keyword in keywords:
#             if stripped_line.startswith(keyword):
#                 spec_lines.append(stripped_line)
#                 break
#     return '<br>'.join(spec_lines)


# 清理商品描述，去除規格相關文字
import re

def remove_number_prefix(text):
    if not isinstance(text, str):
        return text
    # 去掉每行開頭的「數字.」或「數字、」
    return re.sub(r'^\s*\d+[\.、]\s*', '', text, flags=re.MULTILINE)

def extract_precise_specs(description):
    if not isinstance(description, str):
        return ""
    
    # 換行統一
    description = re.sub(r'<br>_x000D_\n|<br>|\n', '\n', description)
    lines = description.splitlines()
    specs = []

    # 規格開頭常見字詞
    keywords_start = ['尺寸', '規格', '材質', '重量', '容量', '厚度', '直徑', '長度', '高度', '張數']

    # 數字+單位正則
    units_pattern = re.compile(r'\d+(\.\d+)?\s*(cm|mm|g|kg|KG|ml|mAh|張|\*|x|X)', re.IGNORECASE)

    # 過濾描述性文字
    discard_words = r'(方便|適合|實用|使用|呈現|展現|提升|增加|專業|美觀|好用|耐用|客製|耐用|質感|優點|特色|色彩|鮮明|便攜|輕巧|多功能|設計|風格|外觀|品質|精緻|細節|工藝|創新|獨特|時尚|經典|品質|優良|耐磨|耐熱|防水|防塵|抗菌|環保|安全|健康|舒適|易清潔|易操作|易安裝|易攜帶|易存儲|精美|精選|精心|精緻|精巧|精美|精細|精確|精湛|精益求精|高品質|高性能|高效率|高科技|高端|高雅|高貴|高尚|高級|豪華|豪華感|豪華版|豪華型號|堅固|堅韌|堅固耐用|堅固型號|堅固版|耐用型號|耐用版|耐磨損|耐磨耗|耐磨損性|耐磨耗性|耐磨損型號|耐磨損版|耐磨耗型號|耐磨耗版|專為|專用|專業版|專業型號|專業設計|專業品質|專業性能|專業技術|專業工藝|專業材料|專業製造|專業品牌|專業認證|專業標準|專業測試|專業評價|專業推薦|創意|創新設計|創新技術|創新材料|創新工藝|創新品牌|創新產品|創新型號|創新版|創新性能|創新品質|創新標準|創新測試|創新評價|創新推薦|小巧|輕便|輕盈|輕巧型號|輕巧版|輕便型號|輕便版|便捷|便捷型號|便捷版|易用|易用型號|易用版|易操作型號|易操作版|易安裝型號|易安裝版|易攜帶型號|易攜帶版|易存儲型號|易存儲版|輕鬆|讓你|讓您|柔軟|觸感|有效|個性|效果|保溫|保冷|保暖|保護|防護|防滑|防震|防摔|防爆|防火|防盜|防盜型號|防盜版|耐磨損性|耐磨耗性|耐磨損型號|耐磨損版|耐磨耗型號|耐磨耗版|廣告|簡易|持久|替換|簡約|大方|可供選擇|可填寫|一次|滿足|可調整|可調節|可調整型號|可調整版|可調節型號|可調節版|可擴展|可擴充|可擴展型號|可擴展版|可擴充型號|可擴充版|多功能型號|多功能版|多用途|多用途型號|多用途版|採用|效益|廣告|增加|附加價值|價值|可分解|取代|塑膠|環保|環保材料|環保型號|環保版|環保設計|環保工藝|環保性能|環保品質|環保標準|環保測試|環保評價|環保推薦|符合|趨勢|適合|效果佳|適合)'

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 如果開頭為關鍵字或有數字+單位
        if any(line.startswith(k) for k in keywords_start) or units_pattern.search(line):
            # 移除描述性文字後的部分
            cleaned_line = re.split(discard_words, line)[0].strip()
            specs.append(cleaned_line)

    return '<br>'.join(specs)


# 讀取 Excel
df = pd.read_excel(r'C:\Users\syf\Desktop\my_Gemini_project\J2產品上架表單_20250807143709.xlsx')

# 確保必要欄位存在
if '商品描述' not in df.columns:
    df['商品描述'] = ''
if '新規格' not in df.columns:
    df['新規格'] = ''

# 填入空字串，避免空值錯誤
df['商品描述'] = df['商品描述'].fillna('')
df['新規格'] = df['新規格'].fillna('')

# 將新站商品詳述拆成規格欄位
df['商品描述'] = df['商品描述'].apply(remove_number_prefix)
df['【新規格】'] = df['新站商品詳述'].apply(extract_precise_specs)

# 清理的描述
# df['新站商品詳述_清理版'] = df['新站商品詳述'].apply(extract_specs_for_new_column)

# 生成 HTML 格式的新規格
df['【新規格】_html'] = df['【新規格】'].apply(convert_to_html_list)

# 合併成最新導入格式
df['最新導入格式'] = df.apply(
    lambda row: '<br>'.join(filter(None, [str([row['【新規格】_html']]), str(row['新站商品詳述'])])),
    axis=1
)

# 過濾掉空的【新規格】
df = df[df['【新規格】'] != '']

# 指定保留欄位
columns_to_keep = [
    '新站商品詳述',
    '新站商品詳述_清理版',
    '【新規格】',
    '最新導入格式',
    '实例ID',
    '產品編號'
]

# 只保留存在的欄位~
final_columns = [col for col in columns_to_keep if col in df.columns]
output_df = df[final_columns]

# 儲存至 Excel~
output_df.to_excel(r'C:\Users\syf\Desktop\my_Gemini_project\更細規格01.xlsx', index=False)

print("檔案處理完成，已更新 '新站商品詳述' 欄位並儲存至 更細規格01.xlsx")
