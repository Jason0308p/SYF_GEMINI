
import sys
import pinecone
import google.generativeai as genai # 假設您安裝的是 google-generativeai

print(f"正在使用的 Python 解譯器: {sys.executable}")
# 或者如果您安裝的是 google-genai，則使用 from google.genai import Client

# --- 步驟 1: 設定您的金鑰和模型 ---

# 建議從環境變數讀取您的 API Key，這樣比較安全
GOOGLE_API_KEY = "AIzaSyCNkzjLT6ES39vRAcxsE92ZmQk_8ztIKBA"
PINECONE_API_KEY = "pcsk_3omCzy_QLPAhGBfA6jQv37cinTqoaA7sNrVCQ6uDF4Cw5cTfBdmBW44rW4PTrPVZRTiCSA"

# Pinecone 環境，根據您提供的資訊是 "us-east-1"
PINECONE_ENVIRONMENT = "us-east-1"

# 您的索引名稱
INDEX_NAME = "syf-products-gemini-01"

# Google Embedding 模型名稱
EMBEDDING_MODEL = "models/text-embedding-004"

# --- 步驟 2: 定義查詢功能 ---

def search_products(query_text: str, top_k: int = 5):
    """
    在 Pinecone 中搜尋與查詢文字最相似的產品。

    Args:
        query_text: 使用者輸入的搜尋文字。
        top_k: 希望返回的最相似結果數量。

    Returns:
        Pinecone 的查詢結果。
    """
    # if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY":
    #     print("錯誤：請設定您的 GOOGLE_API_KEY。")
    #     return None

    # if not PINECONE_API_KEY or PINECONE_API_KEY == "YOUR_PINECONE_API_KEY":
    #     print("錯誤：請設定您的 PINECONE_API_KEY。")
    #     return None

    # 初始化 Google Generative AI 客戶端
    genai.configure(api_key=GOOGLE_API_KEY)

    print(f"正在將查詢 '{query_text}' 轉換為向量 (使用 {EMBEDDING_MODEL})...")
    try:
        # 使用 Google Embedding API 產生向量
        response = genai.embed_content(model=EMBEDDING_MODEL, content=query_text)
        query_vector = response['embedding']
    except Exception as e:
        print(f"生成 Embedding 時發生錯誤: {e}")
        return None

    print("正在初始化 Pinecone 連線...")
    pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

    if INDEX_NAME not in pc.list_indexes().names():
        print(f"錯誤：找不到索引 '{INDEX_NAME}'。")
        return None
        
    index = pc.Index(INDEX_NAME)

    print(f"正在 Pinecone 中搜尋 top {top_k} 個結果...")
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True  # 確保我們能取回產品資訊
    )
    
    return results

# --- 步驟 3: 執行並顯示結果 ---

if __name__ == "__main__":
    # 您想搜尋的產品描述
    # 如果您想要測試，可以取消註解以下行並修改查詢文字
    # search_query = "有背帶的大容量水壺"


    search_query = input("請輸入您想查詢的產品描述：")
    # search_query = "有背帶的大容量水壺"

    search_results = search_products(search_query)
    
    if search_results and search_results['matches']:
        print("\n" + "="*50)
        print(f"查詢 '{search_query}' 的搜尋結果：")
        print("="*50)
        
        for i, match in enumerate(search_results['matches']):
            # 假設您的 metadata 包含 'product_name' 和 'id'
            # .get() 方法可以在鍵不存在時安全地返回 None 或預設值
            product_name = match['metadata'].get('name', '未提供品名')
            product_id = match['id'] # 直接從 match['id'] 獲取產品ID
            score = match['score']
            
            print(f"  結果 {i+1}:")
            print(f"    - 相似度分數: {score:.4f}")
            print(f"    - 產品ID: {product_id}")
            print(f"    - 產品名稱: {product_name}")
            # print(f"    - 原始 Metadata: {match['metadata']}") # 用於除錯
        print("="*50)
    else:
        print("\n查詢沒有返回任何結果。")
