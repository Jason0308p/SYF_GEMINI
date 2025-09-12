
import pandas as pd
import sys

# Set encoding to UTF-8 to handle various characters
sys.stdout.reconfigure(encoding='utf-8')

try:
    file_path = r"C:\Users\syf\Desktop\my_Gemini_project\舊站敘述整理\新增資料夾\0901_導入J2_1.xlsx"
    df = pd.read_excel(file_path)
    # Print the dataframe as a string to see all content
    print(df.to_string())
except Exception as e:
    print(f"An error occurred: {e}")
