import pandas as pd
df = pd.read_excel(r'C:\Users\syf\Desktop\my_Gemini_project\J2產品上架表單_20250807143709.xlsx')
with open('debug_info.txt', 'w', encoding='utf-8') as f:
    f.write(str(df.columns.to_list()) + '\n')
    f.write(df.head().to_string())