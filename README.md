# AI 內容偵測器

以 Streamlit 建立的「AI vs 人類文章偵測器」。使用 Hugging Face Transformers 與 `roberta-base-openai-detector` 模型進行文本分類，提供即時的機率與信心視覺化。

---

## 功能概述
- 標題與大型輸入框，支援長文分析（自動截斷至 512 tokens）。
- 一鍵套用英文示例（AI／人類）以便 Demo。
- 顯示人類/AI 機率、信心分數、進度條及可選圓餅圖。
- 側邊欄提供模型選擇、Softmax 溫度校正與 AI 判定閾值設定。
- 顯示原始標籤與機率的診斷表格，便於理解模型輸出。

---

## 環境安裝

### 選項 A：Conda（推薦）
```powershell
conda create -n HW5 python=3.11 -y
conda activate HW5
pip install -r C:\HW5\requirements.txt
```

### 選項 B：venv
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 專案執行
```powershell
streamlit run C:\HW5\app\ai_content_detector.py
```

執行成功後，請於瀏覽器開啟頁面（如 `http://localhost:8501`）。

---

## 使用指南
- 在主視窗輸入文本並按「開始分析」。
- 若欲 Demo，可展開「快速套用範例文本」，選擇：
	- 「套用 AI 生成示例（英文）」
	- 「套用人類撰寫示例（英文）」
- 側邊欄：
	- 模型選擇（目前預設 `roberta-base-openai-detector`）
	- Softmax 溫度（1.0 為原始；>1 降低極端信心，<1 提高尖銳度）
	- AI 判定閾值（預設 0.6；`fake >= 閾值` 判定為 AI 生成）
- 診斷表格會顯示模型原始標籤與機率，便於檢視輸出分佈。

---

## 已知限制與建議
- 語言適用性：`roberta-base-openai-detector` 主要訓練於英文，對中文文本的準確度有限。
	- 若偵測到非英文文本，介面會提示結果可能失準。
	- 建議改用中文／多語專用的 AI 偵測模型，或提高 AI 判定閾值。
- 長度限制：模型最大序列長度為 512 tokens，超過會自動截斷，結果可能受影響。
- 視覺化：若環境缺字型，Matplotlib 圓餅圖可能出現字元警告，不影響功能。

---

## 檔案結構
- `app/ai_content_detector.py`：主應用程式（Streamlit）。
- `requirements.txt`：套件需求（含 transformers、torch、streamlit、matplotlib、langdetect）。
- `openspec/`：OpenSpec 專案規格與變更提案資料夾。
- `README.md`：本說明文件。

---

## 推送至 GitHub
如需推送本專案至你的 GitHub 倉庫：
```powershell
cd C:\HW5
git init
git branch -M main
git add .
git commit -m "feat: AI content detector app + OpenSpec scaffolding"
git remote add origin https://github.com/Jimmy920403/AI_detector.git
git push -u origin main
```

如已設定過遠端：
```powershell
git remote set-url origin https://github.com/Jimmy920403/AI_detector.git
git push -u origin main
```

---

## 後續強化（可選）
- 加入模型 ID 自訂輸入，測試其他偵測器。
- 提供中文專用或多語模型選項，並建立 ensemble 判定（加入困惑度或啟發式特徵）。
- 加入 CI（GitHub Actions）自動執行 `openspec validate --strict` 或基本健檢。