
import openpyxl

# Data fetched from the website
data = [
    ["主題", "內容"],
    ["摘要", "這篇文章是為企業採購提供的客製化工商日誌挑選指南，強調日誌作為禮贈品能長期傳遞品牌形象的價值。"],
    ["客製化四大關鍵", "尺寸、內頁格式、外觀與材質、LOGO 印刷"],
    ["常見尺寸", "16K (19x26 cm): 尺寸較大，適合會議記錄與規劃。 25K (20x15 cm): 最受歡迎的尺寸，方便攜帶。 48K (9.5x17 cm): 尺寸小巧，適合隨身記事。"],
    ["內頁格式", "基本包含年曆、年計畫、月計畫。常見的週計畫格式有三種：「左三右四」、「左七右筆記」、「全筆記」。"],
    ["外觀與材質", "外觀款式：活頁本、精裝本、三折式、軟皮本等。 封面材質：PU皮革、真皮、布面、再生紙等。 封口方式：磁扣、金屬扣、綁繩、鬆緊帶、拉鍊包等多種設計。"],
    ["LOGO 印刷", "提供 LOGO 燙印服務，並有圖示說明燙印的效果與範圍。"]
]

# Create a new workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "工商日誌客製化"

# Write data to the worksheet
for row in data:
    ws.append(row)

# Save the workbook
try:
    wb.save("C:\\Users\\syf\\Desktop\\my_Gemini_project\\1688\\syf.xlsx")
    print("Successfully created syf.xlsx")
except Exception as e:
    print(f"Error saving file: {e}")
