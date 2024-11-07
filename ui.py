import streamlit as st
import pandas as pd

# データの読み込み
data_path = "UI用データ.xlsx"
data = pd.read_excel(data_path)

# タイトルとURL入力
st.title("商品提案デモ - 自社商品と競合商品の情報表示")
url_input = st.text_input("URLを入力してください")

# セッションステートの初期化
if "current_step" not in st.session_state:
    st.session_state["current_step"] = "confirmation"  # 初期ステップ

# URLに基づく商品の確認
if url_input:
    # 入力されたURLから該当商品のデータを抽出
    product_row = data[data["URL"] == url_input]

    if not product_row.empty:
        product_info = product_row.iloc[0]

        if st.session_state["current_step"] == "confirmation":
            # 商品情報を表示
            st.subheader("この商品情報でよろしいですか？")
            st.write(f"**ASIN**: {product_info['ASIN']}")
            st.write(f"**商品タイトル**: {product_info['タイトル']}")
            st.write(f"**商品説明**: {product_info['説明文']}")
            st.write(f"**価格**: {product_info['価格']} 円")
            st.write(f"**販売個数**: {product_info['販売個数']} 個")
            st.write(f"**売上**: {product_info['売上']} 円")
            st.write(f"**カテゴリ**: {product_info['カテゴリ']}")

            # ボタンを表示
            col1, col2 = st.columns(2)
            with col1:
                generate_btn = st.button("タイトル、箇条書き説明、説明文を生成")
            with col2:
                no_btn = st.button("いいえ")

            # "いいえ"が押された場合は最初に戻る
            if no_btn:
                st.session_state["current_step"] = "confirmation"
                st.experimental_rerun()

            # "生成"が押された場合は競合1の提案を表示
            if generate_btn:
                st.session_state["current_step"] = "competitor_1"
                st.experimental_rerun()

        elif st.session_state["current_step"] == "competitor_1":
            st.subheader("提案 - 競合商品1を参考にした内容")

            # タイトル、箇条書き、説明文の提案（競合1）
            st.write("**提案タイトル**")
            st.write(f"- {product_info['タイトル提案1_1']}")
            st.write(f"- {product_info['タイトル提案1_2']}")
            st.write(f"- {product_info['タイトル提案1_3']}")

            st.write("**箇条書き説明**")
            st.write(f"- {product_info['箇条書き説明提案1_1']}")
            st.write(f"- {product_info['箇条書き説明提案1_2']}")
            st.write(f"- {product_info['箇条書き説明提案1_3']}")

            st.write("**詳細説明文**")
            st.write(f"- {product_info['説明文提案1_1']}")
            st.write(f"- {product_info['説明文提案1_2']}")
            st.write(f"- {product_info['説明文提案1_3']}")

            # 別の競合商品を参考にした提案を表示するボタン
            if st.button("別の競合商品を参考にした提案を見る"):
                st.session_state["current_step"] = "competitor_2"
                st.experimental_rerun()

        elif st.session_state["current_step"] == "competitor_2":
            st.subheader("提案 - 競合商品2を参考にした内容")

            # タイトル、箇条書き、説明文の提案（競合2）
            st.write("**提案タイトル**")
            st.write(f"- {product_info['タイトル提案2_1']}")
            st.write(f"- {product_info['タイトル提案2_2']}")
            st.write(f"- {product_info['タイトル提案2_3']}")

            st.write("**箇条書き説明**")
            st.write(f"- {product_info['箇条書き説明提案2_1']}")
            st.write(f"- {product_info['箇条書き説明提案2_2']}")
            st.write(f"- {product_info['箇条書き説明提案2_3']}")

            st.write("**詳細説明文**")
            st.write(f"- {product_info['説明文提案2_1']}")
            st.write(f"- {product_info['説明文提案2_2']}")
            st.write(f"- {product_info['説明文提案2_3']}")

    else:
        st.warning(
            "入力されたURLに該当する商品が見つかりません。URLを再確認してください。"
        )
