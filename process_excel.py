import pandas as pd
import re

def extract_specs_for_new_column(description):
    if not isinstance(description, str):
        return ""
    cleaned_description = re.sub(r'<br>_x000D_\n|<br>|\n', '\n', description)
    lines = cleaned_description.splitlines()
    spec_lines = []
    keywords = ['規格', '尺寸', '材質', '工藝','重量','包裝'] 

    for line in lines:
        stripped_line = line.strip()
        for keyword in keywords:
            if stripped_line.startswith(keyword):
                spec_lines.append(stripped_line)
                break
    return '<br>'.join(spec_lines)

def clean_main_description(description):
    if not isinstance(description, str):
        return ""
    
    # 1. Remove work order numbers
    desc_no_work_orders = re.sub(r'\b\d{8,}(?:\.\d{8,})*\b', '', description)
    
    # 2. Normalize newlines
    cleaned_description = re.sub(r'<br>_x000D_\n|<br>|\n', '\n', desc_no_work_orders)
    
    lines = cleaned_description.splitlines()
    
    # 3. Exclude lines that describe product specs, craftsmanship, dimensions, material
    # These are the same keywords used for extraction, but here we *remove* them from the main description
    keywords_to_remove_from_main_desc = ['規格', '尺寸', '材質', '工藝','包裝','重量'] 
    
    final_lines = []
    for line in lines:
        stripped_line = line.strip()
        # Check if the line starts with any of the keywords to be removed
        should_remove = False
        for keyword in keywords_to_remove_from_main_desc:
            if stripped_line.startswith(keyword):
                should_remove = True
                break
        
        if not should_remove:
            final_lines.append(line)
            
    return '\n'.join(final_lines).strip()

# Read the original Excel file
df = pd.read_excel(r'C:\Users\syf\Desktop\my_Gemini_project\J2產品上架表單_20250807143709.xlsx')

# Ensure '商品描述' and '新規格' columns exist
if '商品描述' not in df.columns:
    df['商品描述'] = ''
if '新規格' not in df.columns:
    df['新規格'] = ''

# Fill NaN values with empty strings to avoid errors during string operations
df['商品描述'] = df['商品描述'].fillna('')
df['新規格'] = df['新規格'].fillna('')

# Function to process text and replace newlines with <br>
def format_text_for_html(text):
    return str(text).replace('\n', '<br>')

# Apply formatting to relevant columns
df['商品描述_formatted'] = df['商品描述'].apply(format_text_for_html)
df['新規格_formatted'] = df['新規格'].apply(format_text_for_html)

# # 合併成「最新導入格式」 = 【新規格】 + 新站商品詳述（清理後）
# df['最新導入格式'] = df.apply(
#     lambda row: (row['【新規格】'] + '<br>' + row['新站商品詳述']) 
#     if row['【新規格】'] and row['新站商品詳述'] 
#     else (row['【新規格】'] or row['新站商品詳述']),
#     axis=1
# )

print("--- DEBUG START ---")
print("Raw '商品描述' and '新規格':\n" + df[['商品描述', '新規格']].head().to_string())
print("\nFormatted '商品描述_formatted' and '新規格_formatted':\n" + df[['商品描述_formatted', '新規格_formatted']].head().to_string())
# print("\nFinal '最新導入格式':\n" + df[['最新導入格式']].head().to_string())
print("--- DEBUG END ---")

# Drop the temporary formatted columns if not needed later
df = df.drop(columns=['商品描述_formatted', '新規格_formatted'])



# Apply the function to create the '【新規格】' column (restoring original behavior)
df['【新規格】'] = df['新站商品詳述'].apply(extract_specs_for_new_column)

# Apply the cleaning function to the '新站商品詳述' column
df['新站商品詳述'] = df['新站商品詳述'].apply(clean_main_description)

# GPT 
# 🔑 在這裡合併成「最新導入格式」
df['最新導入格式'] = df.apply(
    lambda row: (row['【新規格】'] + '<br>' + row['新站商品詳述']) 
    if row['【新規格】'] and row['新站商品詳述'] 
    else (row['【新規格】'] or row['新站商品詳述']),
    axis=1
)
# GPT

# Filter out rows where '【新規格】' is empty
df = df[df['【新規格】'] != '']

# Define the columns to keep, including '【新規格】'
columns_to_keep = [
    '新站商品詳述',
    '產品規格_測試中',
    '【新規格】', # This column is now included again
    '最新導入格式', # Added the new column here
    '实例ID',
    '產品編號'
]

# Filter for columns that actually exist in the DataFrame
final_columns = [col for col in columns_to_keep if col in df.columns]

# Create the final dataframe with only the specified columns
output_df = df[final_columns]

# Save the final dataframe to the output file
output_df.to_excel(r'C:\Users\syf\Desktop\my_Gemini_project\output4.xlsx', index=False)

print("檔案處理完成，已更新 '新站商品詳述' 欄位並儲存至 output4.xlsx")