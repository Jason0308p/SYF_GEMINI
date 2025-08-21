import pandas as pd
import pinecone
import time
import os

# --- 從 query_pinecone.py 複製過來的金鑰和設定 ---
PINECONE_API_KEY = "pcsk_3omCzy_QLPAhGBfA6jQv37cinTqoaA7sNrVCQ6uDF4Cw5cTfBdmBW44rW4PTrPVZRTiCSA"
# --- 結束複製 ---

# 初始化 Pinecone 連線
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# 列出所有索引
index_names = pc.list_indexes().names()
print("發現索引：", index_names)

# 建立 Excel writer
with pd.ExcelWriter("pinecone_all_indexes.xlsx") as writer:
    for idx_name in index_names:
        print(f"正在抓取索引: {idx_name}")
        index = pc.Index(idx_name)

        # 取得索引統計資料
        stats = index.describe_index_stats()
        # Correct way to get total vector count from stats
        total_vectors = sum(ns.vector_count for ns in stats.namespaces.values())
        print(f"總向量數量: {total_vectors}")

        all_data = []
        # 將 batch_size 降低，以避免 Request-URI Too Large 錯誤
        batch_size = 50 

        # --- CRITICAL CORRECTION: Get all vector IDs using list() ---
        # describe_index_stats does not return actual vector IDs, only counts.
        # We need to iterate through namespaces and list IDs for each.
        all_namespace_ids = []
        for ns_name in stats.namespaces.keys(): # Iterate through namespace names
            print(f"正在從命名空間 '{ns_name}' 收集 ID...")
            namespace_ids = [] # 初始化列表
            # list() returns a generator, iterate through it to get all IDs
            for vector_id in index.list(namespace=ns_name):
                namespace_ids.append(vector_id)
            all_namespace_ids.extend(namespace_ids)
        
        vector_ids = all_namespace_ids # Now vector_ids contains all IDs
        print(f"已收集到 {len(vector_ids)} 個向量 ID。")

        # If total_vectors from stats doesn't match actual IDs, use actual IDs count
        if total_vectors != len(vector_ids):
            print(f"警告: 統計資料中的總向量數量 ({total_vectors}) 與實際收集到的 ID 數量 ({len(vector_ids)}) 不符。將使用實際 ID 數量。")
            total_vectors = len(vector_ids) # Update total_vectors for accurate progress

        # 分批抓向量
        for i in range(0, len(vector_ids), batch_size):
            batch_ids = vector_ids[i:i+batch_size]
            vectors = index.fetch(ids=batch_ids)
            for vid, vec_data in vectors.vectors.items():
                metadata = vec_data.metadata if vec_data.metadata else {}
                metadata['id'] = vid
                print(f"正在收集的 metadata: {metadata}") # Debug print
                all_data.append(metadata)
            print(f"已抓取 {min(i+batch_size, len(vector_ids))} / {len(vector_ids)} 個向量")

        # 存成 Excel 的 sheet (sheet 名稱最多 31 字元)
        df = pd.DataFrame(all_data)
        if df.empty:
            df = pd.DataFrame([{"id": "無資料"}])
        df.to_excel(writer, sheet_name=idx_name[:31], index=False)

print("已將所有索引資料存成 pinecone_all_indexes.xlsx")