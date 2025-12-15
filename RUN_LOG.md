# 執行過程記錄（AI 內容偵測器）

日期：2025-12-15（Windows / Conda 環境 HW5）

---

## 1. 環境建立與套件安裝

```powershell
# 建立並啟用 Conda 環境
conda create -n HW5 python=3.11 -y
conda activate HW5

# 安裝專案需求
pip install -r C:\HW5\requirements.txt
```

安裝重點：
- streamlit、transformers、torch、matplotlib、langdetect
- 首次載入 Hugging Face 模型時，Windows 可能顯示 symlink 緩存警示，屬正常（可忽略或啟用開發人員模式）。

---

## 2. 啟動應用

```powershell
streamlit run C:\HW5\app\ai_content_detector.py
```

執行成功後，Streamlit 會輸出：
- Local URL：`http://localhost:8501`
- Network URL：依據本機網路環境而定

注意事項：
- 若輸入文本超過模型最大長度（512 tokens），系統會顯示「已自動截斷」提示。
- 若為非英文文本，介面會提示目前模型主要訓練於英文，結果可能失準。

---

## 3. Demo 與分析

步驟：
- 展開「快速套用範例文本」
  - 「套用 AI 生成示例（英文）」：技術敘述段落
  - 「套用人類撰寫示例（英文）」：生活敘事段落
- 按「開始分析」後，介面顯示：
  - 判定（AI / 人類）與信心百分比
  - 人類/AI 機率（metrics）與進度條（AI 機率）
  - 可選圓餅圖比例
  - 「診斷：原始標籤與機率」表格（如 fake / real）

側邊欄設定：
- 模型：roberta-base-openai-detector
- Softmax 溫度：預設 1.0（可調 0.5–2.0）
- AI 判定閾值（Fake）：預設 0.6（fake ≥ 閾值 判定 AI）

---

## 4. 常見訊息與處理

- 模型權重載入：
  - Some weights ... were not used ... → 常見於不同任務初始化，屬正常。
- 字型缺字警告（Matplotlib）：
  - 於中文圓餅圖標籤可能出現缺字警告，不影響功能。
- 長文本警告：
  - Token indices sequence length is longer than the specified maximum sequence length ... → 已改為 512 並自動截斷。

---

## 5. 推送到 GitHub

```powershell
cd C:\HW5

# 初始化與提交
git init
git branch -M main
git add .
git commit -m "feat/docs: AI detector app + README + .gitignore"

# 設定遠端並推送
git remote add origin https://github.com/Jimmy920403/AI_detector.git
git push -u origin main
```

若已存在遠端：
```powershell
git remote set-url origin https://github.com/Jimmy920403/AI_detector.git
git push -u origin main
```

---

## 6. 版本與檔案重點

- 應用：app/ai_content_detector.py
  - 使用 @st.cache_resource 快取模型載入
  - 以 id2label 對應 real/fake 計算機率
  - 512 tokens 最大長度、自動截斷提示
  - 側邊欄：模型、溫度、閾值
- 文件：README.md
- 需求：requirements.txt
- 忽略：.gitignore
- OpenSpec：openspec/（專案規範與變更提案）

---

## 7. 後續建議

- 若需中文更準確的偵測，改用中文/多語模型或加入 ensemble（困惑度/啟發式）。
- 可加入 GitHub Actions：自動安裝與 openspec validate --strict 檢查。
