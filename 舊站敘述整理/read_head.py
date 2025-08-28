
import pandas as pd
input_filename = '0825舊站產品資料0804.xlsx'
try:
    df = pd.read_excel(input_filename, dtype=str).fillna('')
    print(df[['goods_sn', 'goods_brief']].head().to_string())
except FileNotFoundError:
    print(f"Error: Cannot find the file '{input_filename}'")
except Exception as e:
    print(f"An error occurred: {e}")
