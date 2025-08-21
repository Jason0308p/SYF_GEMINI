import pinecone
import pandas as pd

# 初始化
pc = pinecone.Pinecone(api_key="pcsk_3omCzy_QLPAhGBfA6jQv37cinTqoaA7sNrVCQ6uDF4Cw5cTfBdmBW44rW4PTrPVZRTiCSA", environment="us-west1-gcp")

index_names = pc.list_indexes().names()

print("發現索引：", index_names)

# 建立一個 Excel writer
with pd.ExcelWriter("pinecone_all_indexes.xlsx") as writer:
    for idx_name in index_names:
        print(f"正在抓取索引: {idx_name}")
        index = pc.Index(idx_name)
        
        # 取得向量總數
        stats = index.describe_index_stats()
        total_vectors = stats.total_vector_count
        print(f"總向量數量: {total_vectors}")
        
        all_data = []
        batch_size = 500
        start_id = 0

        while start_id < total_vectors:
            # 假設你的 ID 是整數從 0 開始，分批抓
            ids = [str(i) for i in range(start_id, min(start_id + batch_size, total_vectors))]
            vectors = index.fetch(ids=ids)
            
            for vid, vec_data in vectors.vectors.items():
                item = vec_data['metadata']
                item['id'] = vid
                all_data.append(item)
            
            start_id += batch_size
            print(f"已抓取 {start_id} / {total_vectors} 個向量")
        
        # 存成 Excel 的 sheet
        df = pd.DataFrame(all_data)
        df.to_excel(writer, sheet_name=idx_name[:31], index=False)  # sheet 名稱最多31字元

print("已將所有索引資料存成 pinecone_all_indexes.xlsx")