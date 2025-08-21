from google.genai import Client
import os

# 使用您在 pinecone_J2_test.py 中的 API 金鑰
api_key = "AIzaSyCNkzjLT6ES39vRAcxsE92ZmQk_8ztIKBA"

print("正在尋找支援 'embedContent' 的模型...")

try:
    client = Client(api_key=api_key)
    
    found_embedding_model = False
    # 迭代所有模型
    for model in client.models.list():
        # 檢查 'supported_actions' 屬性是否存在，並且是否包含 'embedContent'
        if hasattr(model, 'supported_actions') and 'embedContent' in model.supported_actions:
            print(f"  - 找到支援的 embedding 模型: {model.name}")
            found_embedding_model = True
            
    if not found_embedding_model:
        print("\n找不到支援 'embedContent' 的模型。")
        print("請到 Google AI 的官方文件查詢適用於您 API 版本的 embedding 模型名稱。")
        print("常見的名稱有 'text-embedding-004', 'embedding-001' 等。")

except Exception as e:
    print(f"查詢模型時發生錯誤: {e}")
