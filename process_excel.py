import pandas as pd
import re

def extract_and_clean_specs(description):
    if not isinstance(description, str):
        return ""
    # Normalize newlines by replacing various forms of line breaks with a standard newline character
    cleaned_description = re.sub(r'<br>_x000D_\\n|<br>|\\n', '\n', description)
    
    lines = cleaned_description.splitlines()
    spec_lines = []
    keywords = ['規格', '尺寸', '材質', '工藝']
    
    for line in lines:
        stripped_line = line.strip()
        for keyword in keywords:
            if stripped_line.startswith(keyword):
                spec_lines.append(stripped_line)
                break
                
    return '\n'.join(spec_lines)

# Read the original Excel file
df = pd.read_excel(r'C:\Users\syf\Desktop\my_Gemini_project\J2產品上架表單_20250807143709.xlsx')

# Apply the function to create the new column
df['【新規格】'] = df['新站商品詳述'].apply(extract_and_clean_specs)

# Define the columns to keep, using the exact names from the file
columns_to_keep = [
    '新站商品詳述',
    '產品規格_測試中', # Assuming this is what user meant by '產品規格'
    '【新規格】',
    '实例ID',       # Using the actual column name '实例ID'
    '產品編號'
]

# Create the final dataframe with only the specified columns
output_df = df[columns_to_keep]

# Save the final dataframe to the output file
output_df.to_excel(r'C:\Users\syf\Desktop\my_Gemini_project\output.xlsx', index=False)

print("檔案處理完成，已將指定欄位儲存至 output.xlsx")
