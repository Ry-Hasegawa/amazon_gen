import streamlit as st
import pandas as pd

# CSSでカスタムスタイリング
st.markdown(
    """
    <style>
    .highlight-box {
        padding: 10px;
        margin: 10px 0;
        border-radius: 8px;
        background-color: #e6f7ff;
        font-family: Arial, sans-serif;
    }
    .title-highlight {
        background-color: #dff0d8;
        padding: 10px;
        border-radius: 8px;
    }
    .important-message {
        background-color: #fcf8e3;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# データの読み込み
data_path = "./UI用データ.xlsx"
data = pd.read_excel(data_path)

# タイトルとURL入力
st.markdown(
    "<div class='header-title'>商品説明提案チャット</div>",
    unsafe_allow_html=True,
)

# セッションステートの初期化
if "current_step" not in st.session_state:
    st.session_state["current_step"] = "url_input"
if "product_info" not in st.session_state:
    st.session_state["product_info"] = None
if "messages" not in st.session_state:
    # 最初の案内メッセージを設定
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "商品説明を生成したい商品のURLを入力してください。",
        }
    ]


# チャット履歴の表示
def show_chat_messages():
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).markdown(msg["content"])


# チャット履歴の表示関数呼び出し
show_chat_messages()

# 入力プロンプトのメッセージは常に「メッセージを入力してください」
user_input = st.chat_input("メッセージを入力してください")

# ユーザーからの入力があった場合
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # ステップ 1: URL入力ステップ
    if st.session_state["current_step"] == "url_input" and "http" in user_input:
        product_row = data[data["URL"] == user_input.strip()]

        if not product_row.empty:
            # 商品情報をセッションステートに保存
            st.session_state["product_info"] = product_row.iloc[0]
            product_info = st.session_state["product_info"]

            # 商品情報表示と案内メッセージ
            assistant_msg = (
                "**この商品情報でよろしいですか？「はい」と入力してください。**\n\n"
                f"- **ASIN:** {product_info['ASIN']}\n"
                f"- **商品タイトル:** {product_info['タイトル']}\n"
                f"- **商品説明:** {product_info['説明文']}\n"
                f"- **価格:** {product_info['価格']} 円\n"
                f"- **販売個数:** {product_info['販売個数']} 個\n"
                f"- **売上:** {product_info['売上']} 円\n"
                f"- **カテゴリ:** {product_info['カテゴリ']}\n"
            )
            st.session_state["messages"].append(
                {"role": "assistant", "content": assistant_msg}
            )
            st.session_state["current_step"] = "title_proposal"
        else:
            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": "入力されたURLに該当する商品が見つかりません。URLを再確認してください。",
                }
            )

    # ステップ 2: タイトル提案ステップ
    elif (
        st.session_state["current_step"] == "title_proposal"
        and user_input.lower() == "はい"
    ):
        product_info = st.session_state["product_info"]
        assistant_msg = (
            "**タイトル提案:**\n\n"
            f"- **提案1:** {product_info['タイトル提案1']}\n"
            f"- **提案2:** {product_info['タイトル提案2']}\n"
            f"- **提案3:** {product_info['タイトル提案3']}\n\n"
            "**「次へ」と入力して訴求軸を確認してください。**"
        )
        st.session_state["messages"].append(
            {"role": "assistant", "content": assistant_msg}
        )
        st.session_state["current_step"] = "appeal_points"

    # ステップ 3: 訴求軸の提示ステップ
    elif (
        st.session_state["current_step"] == "appeal_points"
        and user_input.lower() == "次へ"
    ):
        product_info = st.session_state["product_info"]

        # 訴求軸を「:」で分割して改行しながら表示
        def format_appeal_points(text):
            # Split by ":" and filter out empty strings
            points = [p.strip() for p in text.split(":") if p.strip()]
            return "\n".join(f"  - {p}" for p in points)

        formatted_appeal_points = (
            "### 訴求軸:\n\n"
            f"**自社製品訴求軸:**\n{format_appeal_points(product_info['自社製品訴求軸'])}\n\n"
            f"**競合訴求軸:**\n{format_appeal_points(product_info['競合訴求軸'])}\n\n"
            "**「次へ」と入力して箇条書き説明を確認してください。**"
        )
        st.session_state["messages"].append(
            {"role": "assistant", "content": formatted_appeal_points}
        )
        st.session_state["current_step"] = "bullet_points"

    # ステップ 4: 箇条書き説明提案ステップ
    elif (
        st.session_state["current_step"] == "bullet_points"
        and user_input.lower() == "次へ"
    ):
        product_info = st.session_state["product_info"]

        # 各箇条書き説明を「【」で分割し、見やすい形式で表示（【を保持）
        def format_bullet_points(bullet_text):
            points = [
                f"【{point.strip()}" for point in bullet_text.split("【") if point
            ]
            return "\n".join(f"- {p}" for p in points)

        formatted_bullet_points = (
            f"**提案1**:\n{format_bullet_points(product_info['箇条書き説明提案1'])}\n\n"
            f"**提案2**:\n{format_bullet_points(product_info['箇条書き説明提案2'])}\n\n"
            f"**提案3**:\n{format_bullet_points(product_info['箇条書き説明提案3'])}\n\n"
            f"**提案4**:\n{format_bullet_points(product_info['箇条書き説明提案4'])}\n\n"
            "**「次へ」と入力して詳細な説明文を確認してください。**"
        )

        st.session_state["messages"].append(
            {"role": "assistant", "content": formatted_bullet_points}
        )
        st.session_state["current_step"] = "long_description"

    # ステップ 5: 詳細説明文提案ステップ
    elif (
        st.session_state["current_step"] == "long_description"
        and user_input.lower() == "次へ"
    ):
        product_info = st.session_state["product_info"]
        assistant_msg = (
            "### 詳細説明文提案:\n\n"
            f"- **説明1:** {product_info['説明文提案1']}\n"
            f"- **説明2:** {product_info['説明文提案2']}\n"
            f"- **説明3:** {product_info['説明文提案3']}\n\n"
            "次の商品を提案したい場合、再度URLを入力してください。\n\n"
            f"**参考にした競合商品:**\n- {product_info['競合タイトル']}\n- {product_info['競合2タイトル']}"
        )
        st.session_state["messages"].append(
            {"role": "assistant", "content": assistant_msg}
        )
        # 最初に戻す
        st.session_state["current_step"] = "url_input"
        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": "商品説明を生成したい商品のURLを入力してください。",
            }
        )

    # 想定されるメッセージが入力されなかった場合
    else:
        st.session.state["messages"].append(
            {
                "role": "assistant",
                "content": "無効なメッセージです。全て最初からやり直してください。",
            }
        )
        # セッションステートをリセットして最初からやり直し
        st.session_state["current_step"] = "url_input"
        st.session_state["product_info"] = None
        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": "商品説明を生成したい商品のURLを入力してください。",
            }
        )

    # チャット履歴を更新して表示
    show_chat_messages()
