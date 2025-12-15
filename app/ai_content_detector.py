import streamlit as st
from typing import Dict, Tuple

@st.cache_resource(show_spinner=True)
def load_model(model_name: str):
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

def predict(text: str, model_name: str, temperature: float = 1.0) -> Tuple[float, float, Dict[str, float]]:
    import torch
    from torch.nn.functional import softmax
    tokenizer, model = load_model(model_name)
    # roberta 類模型最大序列長度通常為 512
    encoded = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.inference_mode():
        logits = model(**encoded).logits
        if temperature and temperature > 0 and temperature != 1.0:
            logits = logits / temperature
        probs = softmax(logits, dim=-1)[0].cpu().numpy().tolist()

    # 使用模型的 id2label 提供的標籤名稱，避免誤判
    # roberta-base-openai-detector 通常為 {0: 'Real', 1: 'Fake'}
    id2label = getattr(model.config, 'id2label', {0: 'Real', 1: 'Fake'})
    labels = [id2label.get(i, f"LABEL_{i}").lower() for i in range(len(probs))]

    # 嘗試以名稱對應，若名稱缺失則以索引回退
    real_idx = labels.index('real') if 'real' in labels else 0
    fake_idx = labels.index('fake') if 'fake' in labels else (1 if len(probs) > 1 else 0)

    real = float(probs[real_idx])
    fake = float(probs[fake_idx])
    raw = {labels[i]: float(probs[i]) for i in range(len(probs))}
    return real, fake, raw

def render_metrics(real: float, fake: float):
    col1, col2 = st.columns(2)
    col1.metric("人類文本機率", f"{real*100:.2f}%")
    col2.metric("AI 文本機率", f"{fake*100:.2f}%")
    st.progress(int(fake * 100))
    st.caption("進度條以 AI 機率表示")

def render_pie(real: float, fake: float):
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.pie([real, fake], labels=["人類", "AI"], autopct='%1.1f%%', colors=['#4CAF50', '#FF7043'])
        ax.axis('equal')
        st.pyplot(fig)
    except Exception:
        st.info("圖表模組不可用，略過圓餅圖。")

def main():
    st.set_page_config(page_title="AI 內容偵測器", page_icon="🤖", layout="centered")
    st.title("AI 內容偵測器")
    st.write("輸入一段文字，系統將判斷其為人類撰寫或 AI 生成的可能性。")

    # 模型選擇與診斷參數
    with st.sidebar:
        st.header("模型與設定")
        model_name = st.selectbox(
            "選擇偵測模型",
            options=[
                "roberta-base-openai-detector",
                # 可再加入其他檢測模型 ID
            ],
            index=0,
        )
        temperature = st.slider("Softmax 溫度 (校正)", min_value=0.5, max_value=2.0, value=1.0, step=0.1,
                                help=">1 降低極端信心，<1 提高尖銳度。")
        threshold = st.slider("AI 判定閾值 (Fake)", min_value=0.5, max_value=0.9, value=0.6, step=0.05,
                               help="當 AI 機率 ≥ 閾值 時判定為 AI 生成。")

    # 範例文本（英文示例）
    demo_ai = (
        "In modern machine learning systems, generalization performance often depends on data distribution,\n"
        "regularization strategies, and trade-offs in multi-objective optimization to achieve robust metrics."
    )
    demo_human = (
        "This morning my commute took about half an hour, so I finished yesterday's article on the train.\n"
        "When I got to the office, I cleaned up my to-do list and fixed a small bug that had been blocking me."
    )

    with st.expander("快速套用範例文本"):
        c1, c2 = st.columns(2)
        if c1.button("套用 AI 生成示例（英文）"):
            st.session_state["input_text"] = demo_ai
        if c2.button("套用人類撰寫示例（英文）"):
            st.session_state["input_text"] = demo_human

    default_text = st.session_state.get("input_text", "")
    text = st.text_area("請貼上待分析文本", value=default_text, height=240, help="支援長文輸入，請按下方按鈕開始分析。")
    analyze = st.button("開始分析")

    if analyze:
        if not text or not text.strip():
            st.error("輸入不可為空，請提供文本後重試。")
            return
        # 語言偵測（提示模型適用性）
        try:
            from langdetect import detect
            lang = detect(text.strip())
            if lang != 'en':
                st.info("偵測到非英文文本。當前模型主要針對英文訓練，結果可能失準，建議更換為支援中文的偵測模型或調整判定閾值。")
        except Exception:
            pass
        with st.spinner("載入模型並分析中…"):
            try:
                real, fake, raw = predict(text.strip(), model_name=model_name, temperature=temperature)
            except Exception as e:
                st.error(f"分析時發生錯誤：{e}")
                return
        # 若文本過長，提示已截斷
        try:
            from transformers import AutoTokenizer
            tk = AutoTokenizer.from_pretrained(model_name)
            if len(tk(text).get('input_ids', [])) > 512:
                st.warning("文本超過模型最大長度，已自動截斷至前 512 token，結果可能受影響。")
        except Exception:
            pass

        # 結果顯示
        verdict = "AI 生成" if fake >= threshold else "人類撰寫"
        confidence = max(real, fake)
        st.subheader("分析結果")
        st.success(f"判定：{verdict}（信心 {confidence*100:.2f}%）")

        render_metrics(real, fake)
        st.divider()
        st.caption("比例視覺化（可選）")
        render_pie(real, fake)

        # 顯示原始標籤與機率以便診斷
        st.divider()
        st.subheader("診斷：原始標籤與機率")
        st.table({"label": list(raw.keys()), "prob": [f"{p*100:.2f}%" for p in raw.values()]})

if __name__ == "__main__":
    main()