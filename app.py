import streamlit as st
from langchain_community.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from azure.cosmos import CosmosClient, PartitionKey
import speech_recognition as sr
import pyttsx3
import uuid
import datetime
import requests

# --- 既存のimportの下あたり（できれば30行目付近）に移動 ---
def search_web(query):
    """SerpAPIでGoogle検索結果のスニペットを取得"""
    api_key = st.secrets.get("SERPAPI_KEY", "")
    if not api_key:
        return ""
    params = {
        "q": query,
        "hl": "ja",
        "gl": "jp",
        "api_key": api_key,
        "num": 3,
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json()
        snippets = []
        for res in results.get("organic_results", []):
            title = res.get("title", "")
            snippet = res.get("snippet", "")
            if title and snippet:
                snippets.append(f"{title}: {snippet}")
        return "\n".join(snippets)
    except Exception as e:
        return ""
    
# --- シークレット読み込み ---
OPENAI_API_KEY = st.secrets["openai_api_key"]
AZURE_OPENAI_ENDPOINT = st.secrets["azure_endpoint"]
AZURE_OPENAI_DEPLOYMENT = st.secrets["azure_deployment"]
COSMOS_CONNECTION_STRING = st.secrets["COSMOS_CONNECTION_STRING"]
COSMOS_DB_NAME = st.secrets["COSMOS_DB_NAME"]
COSMOS_CONTAINER_NAME = st.secrets["COSMOS_CONTAINER_NAME"]

# --- Cosmos DB 初期化 ---
cosmos_client = CosmosClient.from_connection_string(COSMOS_CONNECTION_STRING)
database = cosmos_client.create_database_if_not_exists(id=COSMOS_DB_NAME)
container = database.create_container_if_not_exists(
    id=COSMOS_CONTAINER_NAME,
    partition_key=PartitionKey(path="/user_id")
)

# --- エージェント定義 ---
AGENTS = {
    "👵しずかさん（癒してくれます）": "あなたは優しい癒し系アシスタントです。共感し、励ます言葉で返答してください。",
    "👴なつおじ（懐かしい話がすき）": "あなたは思い出話を引き出すアシスタントです。過去の楽しい出来事を聞き出してください。",
    "😊げんき丸（げんきがでます！）": "あなたは前向きな気持ちを与えるアシスタントです。やる気の出る言葉で返答してください。",
    "👨‍🦳みつじい（ダジャレがすき）": "あなたは一流お笑い芸人です。すべて回答にユーモアとおやじギャグで利用者を笑わせるアシスタントです。楽しい返答をしてください。"
}

# --- 方言スタイル ---
DIALECTS = {
    "標準語": "",
    "関西弁": "関西弁で話してください。",
    "東北弁": "東北弁で話してください。",
    "群馬弁": "群馬の方言で話してください。",
    "広島弁": "広島の方言で話してください。",
    "熊本弁": "熊本の方言で話してください。",
    "沖縄弁": "沖縄の方言で話してください。",
}

# --- 音声読み上げ（Ayumi の声で） ---
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSTTS_V110_jaJP_Ayumi')
    engine.say(text)
    engine.runAndWait()

# --- ページ設定 & CSS ---
st.set_page_config(page_title="こころの縁がわチャット", layout="centered")

st.markdown("""
    <style>
        body, .stApp {
            background-color: #FFF8E7;
        }

        /* 既存の不要な白枠すべて完全非表示 */

        /* ▼ glass-box内のselectboxやinputの外側の白い枠を消す */
        .glass-box > div {
            background: none !important;
            box-shadow: none !important;
            border: none !important;
            padding: 0 !important;
            margin-bottom: 12px !important;
        }

        /* ▼ selectboxやinputの背景も透明に */
        .glass-box input, 
        .glass-box textarea, 
        .glass-box div[data-baseweb="select"], 
        .glass-box div[data-baseweb="select"] div[role="combobox"] {
            background: none !important;
            box-shadow: none !important;
            border: none !important;
        }

        /* ▼ 選択肢の背景も透明に */
        .glass-box div[data-baseweb="option"] {
            background: none !important;
        }

        .egawa-title {
            text-align: center;
            font-size: 2.2rem;
            font-weight: bold;
            margin-bottom: 0.2em;
        }
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #666666;
            margin-bottom: 10px;
        }
        .divider {
            border-bottom: 2px solid #FFA500;
            width: 50%;
            margin: 0 auto 20px auto;
        }

        /* ▼ マイクで話すボタンの背景を薄い緑に＋大きくする */
        button[kind="secondary"], .stButton>button {
            background-color: #d6f5d6 !important;
            color: #333 !important;
            border: none !important;
            font-size: 1.3rem !important;
            padding: 0.7em 2.5em !important;
            border-radius: 10px !important;
        }
        button[kind="secondary"]:hover, .stButton>button:hover {
            background-color: #b2e6b2 !important;
        }

        /* ▼ ラベル文字を大きくする（subtitleと同じサイズ） */
        label, .stSelectbox label, .glass-box label, .glass-box .stSelectbox label {
            font-size: 1.1rem !important;
        }
        /* ▼ selectboxの選択中の文字も大きく */
        .glass-box div[data-baseweb="select"] div[role="combobox"] {
            font-size: 1.1rem !important;
        }
        /* ▼ inputやselectの中身も大きく */
        .glass-box input, .glass-box textarea {
            font-size: 1.1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- タイトル表示 ---
st.markdown("""
    <div class="egawa-title">🍵こころの縁側チャット🍃</div>
    <p class='subtitle'>ホッとできる会話をどうぞ。</p>
    <div class='divider'></div>
""", unsafe_allow_html=True)

# --- UIカード部分 ---
st.markdown("<div class='glass-box'>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

selected_agent = st.selectbox("話し相手をえらんでください：", list(AGENTS.keys()))
selected_dialect = st.selectbox("方言をえらんでください：", list(DIALECTS.keys()))

# ▼ ボタンを横並びにする
col1, col2 = st.columns([1, 1])
with col1:
    mic_btn = st.button("🎤 マイクで話す")
with col2:
    clear_btn = st.button("🗑️ 会話履歴を消す")

# CSSは省略

if clear_btn:
    st.session_state["messages"] = []

user_input = None

if mic_btn:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("マイクから入力を待っています…")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio, language="ja-JP")
            st.success(f"音声認識結果：{user_input}")
        except Exception as e:
            st.error(f"音声認識に失敗しました：{e}")

# ▼ ここで user_input があれば会話処理
if user_input:
    # 必要なプロンプトや履歴処理
    # 例:
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    # システムプロンプトは毎回先頭に
    system_prompt = (
        AGENTS[selected_agent] + " " + DIALECTS[selected_dialect] +
        "\nあなたはWeb検索結果を参考に、できるだけ具体的な最新情報を要約して答えてください。"
    )
    # --- ここから追加 ---
    # ユーザー入力が特定ワードを含む場合はWeb検索
    web_info = ""
    keywords = ["天気", "ニュース", "今日", "今", "最新", "調べて", "検索", "気温", "話題", "気になる"]
    if any(word in user_input for word in keywords):
        web_info = search_web(user_input)
        st.write(web_info)  # ← 追加してみてください
        if web_info:
            user_input += f"\n\n以下は検索結果の参考情報です。\n{web_info}"
    # --- ここまで追加 ---

    if not st.session_state["messages"]:
        st.session_state["messages"].append(SystemMessage(content=system_prompt))
    st.session_state["messages"].append(HumanMessage(content=user_input))

    chat = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_version="2023-05-15",
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
        openai_api_key=OPENAI_API_KEY,
        openai_api_type="azure"
    )
    response = chat(st.session_state["messages"])
    st.session_state["messages"].append(response)

    st.markdown(f"#### {selected_agent} のこたえ")
    st.success(response.content)
    speak_text(response.content)

# ▼ 履歴を画面に表示（オプション：最新5件などにしてもOK）
for m in st.session_state["messages"]:
    if isinstance(m, HumanMessage):
        st.markdown(f"**あなた:** {m.content}")
    elif isinstance(m, SystemMessage):
        pass  # システムプロンプトは表示しない
    else:
        st.markdown(f"**{selected_agent}:** {m.content}")

st.markdown("</div>", unsafe_allow_html=True)

