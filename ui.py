import streamlit as st
import pandas as pd

# CSSでカスタムスタイリング
st.markdown(
    """
    <style>
    .chat-box {
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        background-color: #f1f1f1;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
        font-family: Arial, sans-serif;
    }
    .user-message {
        background-color: #e0ffe6;
        color: #2d7a36;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        font-weight: bold;
    }
    .bot-message {
        background-color: #d6e4ff;
        color: #1a3e79;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        font-weight: bold;
    }
    .header-title {
        font-size: 24px;
        color: #333;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# データの読み込み
data_path = "UI用データ.xlsx"
data = pd.read_excel(data_path)

# タイトルとURL入力
st.markdown(
    "<div class='header-title'>商品説明提案チャット</div>",
    unsafe_allow_html=True,
)

# セッションステートの初期化
if "current_step" not in st.session_state:
    st.session_state["current_step"] = "confirmation"  # 初期ステップ
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""
if "product_info" not in st.session_state:
    st.session_state["product_info"] = None

# チャット形式の入力
user_input = st.chat_input("URLを入力してください")

if user_input:
    st.session_state["input_text"] = user_input

    if st.session_state["current_step"] == "confirmation" and "http" in user_input:
        # 入力されたURLから該当商品のデータを抽出
        product_row = data[data["URL"] == user_input.strip()]

        if not product_row.empty:
            # 商品情報をセッションステートに保存
            st.session_state["product_info"] = product_row.iloc[0]

            # 商品情報を表示
            product_info = st.session_state["product_info"]
            st.markdown(
                f"""
                <div class="chat-box bot-message">
                <p><strong>この商品情報でよろしいですか？</strong></p>
                <p><strong>提案を生成する場合は「はい」と入力してください。</strong></p>
                <p><strong>ASIN:</strong> {product_info['ASIN']}</p>
                <p><strong>商品タイトル:</strong> {product_info['タイトル']}</p>
                <p><strong>商品説明:</strong> {product_info['説明文']}</p>
                <p><strong>価格:</strong> {product_info['価格']} 円</p>
                <p><strong>販売個数:</strong> {product_info['販売個数']} 個</p>
                <p><strong>売上:</strong> {product_info['売上']} 円</p>
                <p><strong>カテゴリ:</strong> {product_info['カテゴリ']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.session_state["current_step"] = "competitor_1"
        else:
            st.markdown(
                f"""
                <div class="chat-box bot-message">
                <p>入力されたURLに該当する商品が見つかりません。URLを再確認してください。</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif (
        st.session_state["current_step"] == "competitor_1"
        and user_input.lower() == "はい"
    ):
        product_info = st.session_state["product_info"]
        st.markdown(
            f"""
            <div class="chat-box bot-message">
            <p><strong>提案 - 競合商品1を参考にした内容</strong></p>
            <p><strong>提案タイトル:</strong></p>
            <ul>
                <li>{product_info['タイトル提案1_1']}</li>
                <li>{product_info['タイトル提案1_2']}</li>
                <li>{product_info['タイトル提案1_3']}</li>
            </ul>
            <p><strong>箇条書き説明:</strong></p>
            <ul>
                <li>{product_info['箇条書き説明提案1_1']}</li>
                <li>{product_info['箇条書き説明提案1_2']}</li>
                <li>{product_info['箇条書き説明提案1_3']}</li>
            </ul>
            <p><strong>詳細説明文:</strong></p>
            <ul>
                <li>{product_info['説明文提案1_1']}</li>
                <li>{product_info['説明文提案1_2']}</li>
                <li>{product_info['説明文提案1_3']}</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.session_state["current_step"] = "competitor_2"

    elif (
        st.session_state["current_step"] == "competitor_2"
        and user_input.lower() == "別の提案を見る"
    ):
        product_info = st.session_state["product_info"]
        st.markdown(
            f"""
            <div class="chat-box bot-message">
            <p><strong>提案 - 競合商品2を参考にした内容</strong></p>
            <p><strong>提案タイトル:</strong></p>
            <ul>
                <li>{product_info['タイトル提案2_1']}</li>
                <li>{product_info['タイトル提案2_2']}</li>
                <li>{product_info['タイトル提案2_3']}</li>
            </ul>
            <p><strong>箇条書き説明:</strong></p>
            <ul>
                <li>{product_info['箇条書き説明提案2_1']}</li>
                <li>{product_info['箇条書き説明提案2_2']}</li>
                <li>{product_info['箇条書き説明提案2_3']}</li>
            </ul>
            <p><strong>詳細説明文:</strong></p>
            <ul>
                <li>{product_info['説明文提案2_1']}</li>
                <li>{product_info['説明文提案2_2']}</li>
                <li>{product_info['説明文提案2_3']}</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        # 想定されるメッセージが入力されなかった場合
        st.markdown(
            f"""
            <div class="chat-box bot-message">
            <p>無効なメッセージが入力されました。全て最初からやり直してください。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # セッションステートをリセットして最初からやり直し
        st.session_state["current_step"] = "confirmation"
        st.session_state["product_info"] = None
        st.session_state["input_text"] = ""
