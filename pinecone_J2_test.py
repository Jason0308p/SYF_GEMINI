from google.genai import Client
from pinecone import Pinecone, ServerlessSpec
import pandas as pd
import time

# --- 安全性建議 ---
# 建議您使用環境變數等更安全的方式來管理您的 API 金鑰，而不是直接寫在程式碼中。
# from dotenv import load_dotenv
# import os
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# ​​​ 初始化 Gemini client
# client = Client(api_key=GOOGLE_API_KEY)
client = Client(api_key="AIzaSyCNkzjLT6ES39vRAcxsE92ZmQk_8ztIKBA")

# ​​​ 載入資料
df = pd.read_excel(r"C:\Users\syf\Desktop\my_Gemini_project\J2產品上架表單_20250807143709.xlsx", engine='openpyxl')

# --- 關鍵修正：將所有 NaN 值轉換為 None ---
df = df.where(pd.notna(df), None)

# ​​​ 初始化 Pinecone
# pc = Pinecone(api_key=PINECONE_API_KEY)
pc = Pinecone(api_key="pcsk_3omCzy_QLPAhGBfA6jQv37cinTqoaA7sNrVCQ6uDF4Cw5cTfBdmBW44rW4PTrPVZRTiCSA")
index_name = "syf-products-gemini-01"

# --- 刪除舊索引以重建 ---
# 檢查索引是否存在，如果存在，則刪除它以確保維度正確
if index_name in pc.list_indexes().names():
    print(f"偵測到舊索引 '{index_name}'，正在刪除以修正維度不符問題...")
    pc.delete_index(index_name)
    # 等待幾秒鐘，確保索引完全刪除
    time.sleep(5)
    print("舊索引刪除完畢。")

# --- Pinecone 索引操作 ---
# 檢查索引是否存在，如果不存在，則建立一個新的
if index_name not in pc.list_indexes().names():
    print(f"正在建立新索引 '{index_name}'...")
    # 注意：dimension 需要與您的 embedding 模型輸出維度一致
    # text-embedding-004 的維度是 768
    pc.create_index(
        name=index_name,
        dimension=768, 
        metric='cosine',
        # 修正：將區域改為免費方案支援的 us-east-1
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
    print("新索引建立完成。")

# 連接到您的索引
index = pc.Index(index_name)

# --- 批次處理與上傳 ---
batch_size = 32  # 根據您的資料量和 API 限制調整批次大小

print("開始處理與上傳資料...")
for i in range(0, len(df), batch_size):
    batch_df = df.iloc[i:i+batch_size].copy() # 使用 .copy() 避免 SettingWithCopyWarning
    
    # 為批次中的每一行建立要 embedding 的文本
    texts_to_embed = [f"{row['新站商品名稱']},{row['新站商品簡述']}" for _, row in batch_df.iterrows()]
    
    try:
        # --- 使用正確的模型名稱 ---
        resp = client.models.embed_content(
            model="models/text-embedding-004",
            contents=texts_to_embed
        )
        
        # --- 修正：從每個 embedding 物件中提取 .values ---
        embeddings = [e.values for e in resp.embeddings]
        
        # 將 embedding 加回到 batch_df 中，方便後續處理
        batch_df['values'] = embeddings

        # --- 準備上傳到 Pinecone 的資料格式 ---
        vectors_to_upsert = []
        for _, row in batch_df.iterrows():
            product_id = str(row['產品編號'])

            # --- 檢查 ID 是否為 ASCII，如果不是，則跳過 (通常是標題行)
            if not product_id.isascii():
                print(f"偵測到非 ASCII 的 ID，已跳過: {product_id}")
                continue

            # --- 建立 metadata ---
            metadata = {
                "name": row.get('新站商品名稱'),
                "category": row.get('核心原始核心編碼名稱'),
                "price": row.get('新單價'),
                "url": row.get('新站產品 URL'),
                "image": row.get('商品圖片路徑')
            }

            # --- 終極修正：過濾掉值為 None 的 metadata 欄位 ---
            filtered_metadata = {k: v for k, v in metadata.items() if v is not None}

            vectors_to_upsert.append({
                "id": product_id,
                "values": row['values'],
                "metadata": filtered_metadata
            })

        # --- 在迴圈內批次上傳到 Pinecone ---
        if vectors_to_upsert:
            index.upsert(vectors=vectors_to_upsert)
            print(f"成功處理並上傳批次 {i//batch_size + 1}，共 {len(vectors_to_upsert)} 筆資料。")

    except Exception as e:
        print(f"處理批次 {i//batch_size + 1} 時發生錯誤: {e}")
        # 您可以在這裡加入更詳細的錯誤日誌或重試機制
        time.sleep(5)

print("\n所有批次處理完成！")