import streamlit as st
import google.generativeai as genai
import os

# ページの設定
st.set_page_config(page_title="熊本不動産検索AI", layout="centered")

st.title("🏠 熊本不動産検索AIツール")
st.caption("Gemini AIがあなたにぴったりの物件を提案します")

# サイドバーの設定（APIキーなど）
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Gemini API Keyを入力", type="password")
    st.info("APIキーはGoogle AI Studioで取得したものを入力してください。")

# 入力フォーム
with st.form("search_form"):
    area = st.text_input("希望の地域は？", placeholder="例：熊本市中央区、合志市")
    budget = st.text_input("予算（上限）や間取りは？", placeholder="例：8万円、2LDK")
    options = st.text_area("その他の条件", placeholder="例：駐車場込み、築浅、12畳以上のLDK")
    
    submit_button = st.form_submit_button("AIに物件を検索してもらう")

# 実行ボタンが押された時の処理
if submit_button:
    if not api_key:
        st.warning("左側のサイドバーにAPIキーを入力してください。")
    elif not area or not budget:
        st.error("地域と予算は必須入力です。")
    else:
        try:
            genai.configure(api_key=api_key)
            # モデルの指定（最新の2.0-flashなどを使用）
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            with st.spinner("AIが最適な物件を考えています..."):
                prompt = f"""
                あなたは熊本の不動産エキスパートです。
                以下の条件に合う物件情報を提案し、最後にSUUMOやホームズへのリンクを提示してください。
                
                地域: {area}
                予算・間取り: {budget}
                条件: {options}
                """
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown("### 🤖 AIからの提案結果")
                st.write(response.text)
                st.success("検索が完了しました！")
                
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            
