from mistune import html
import pandas as pd
import numpy as np
import re
import random

col = '新站商品詳述'
J2_path = r"C:\Users\syf\Desktop\my_Gemini_project\舊站敘述整理\J2第二次修改規格0901.xlsx"
output_path = r'C:\Users\syf\Desktop\my_Gemini_project\舊站敘述整理\J2第二次修改規格0901_修改後三版.xlsx'
J2_df = pd.read_excel(J2_path)

# 進行特定欄位處理
# 去除 col 裡面的值 ul li裡的 '&nbsp'
J2_df[col] = J2_df[col].replace({r'&nbsp;': ' '}, regex=True) 

# 用正則刪除所有包含「最低」的 <li> ... </li>
# J2_df[col] = J2_df[col].str.replace(r'<li>[^<]*?最低[^<]*?</li>', '', regex=True)
# 刪掉 <li> 或 <br> 中含「最低」的行
J2_df[col] = J2_df[col].str.replace(
    r'(<li>[^<]*?最低[^<]*?</li>)|(<br>[^<]*?最低[^<]*?(<br>|$))',
    '',
    regex=True
)

J2_df = J2_df[['產品編號',col,'实例ID']]
# subset 代表只要col 有空值則刪除該 row
J2_df = J2_df.dropna(subset=[col])

J2_df.to_excel(output_path, index=False)
