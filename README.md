# 🍵 こころの縁側チャット（Kokoro no Engawa Chat）

高齢者の方に向けた、心に寄り添う音声対話AIチャットボットです。  
音声入力・方言切替・キャラクター切替などを備え、まるで縁側でおしゃべりしているような温かさを届けます。

👉 デモ動画：https://youtu.be/8irsx42btNo

---

## 🧩 主な機能

- 🎙 **音声入力でチャット**（マイクで話すだけ）
- 🧑‍🤝‍🧑 **エージェント切替**（癒し／思い出話／元気づけ／ダジャレ）
- 🗣 **方言対応**：関西弁、東北弁、群馬弁、広島弁、熊本弁、沖縄弁
- 🧠 **Azure OpenAI GPT-4o連携**
- 🔊 **pyttsx3による音声読み上げ**（キャラごとに声変更）
- 🌤 **最新ニュースや天気を検索（SerpAPI連携）**
- 📦 **会話履歴を Azure Cosmos DB に保存**

---

## ⚙️ 技術スタック

| 技術 | 内容 |
|------|------|
| UI | Streamlit |
| 言語 | Python |
| LLM | Azure OpenAI GPT-4o |
| 音声認識 | `speech_recognition` (Google) |
| 読み上げ | `pyttsx3` |
| 検索API | SerpAPI |
| データ保存 | Azure Cosmos DB |
| その他 | 方言プロンプト／キャラクター指示切替など

---

## 🚀 実行方法

1. `secrets.toml` を用意（以下をローカルに設置）:

```toml
openai_api_key = "sk-..."
azure_endpoint = "https://xxx.openai.azure.com"
azure_deployment = "gpt4o"
COSMOS_CONNECTION_STRING = "AccountEndpoint=..."
COSMOS_DB_NAME = "your-db"
COSMOS_CONTAINER_NAME = "messages"
SERPAPI_KEY = "your-serpapi-key"
