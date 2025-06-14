# こころの編尾チャット (高齢者向けAI役割切替形音声入力チャット)

## 概要

「**こころの編尾チャット**」は、**高齢者向けの心に寄り添う音声对話AIチャットボット**です．
以下の機能を備えており、こころの休息所のような仕組みを目指しました。

## 主要機能

- 【🍴話し相手切り替機能】
  - しずかさん（病みを聞いてくれる優しい人）
  - なつおじ（憩しを感じさせる思い出話風）
  - げんき丸（元気づけする役々）
  - みつじい（ダジャレやユーモアを入れて笑わせる）

- 【🌎方言スタイル切り替機能】
  - 標準語 / 関西語 / 東北語 / 群馬語 / 広島語 / 熊本語 / 沖縄語

- 【🎧音声入力 & 読み上げ】
  - Google Speech Recognition での声認識
  - pyttsx3 での読み上げ (しずかさんは女性声 など)

- 【📊最新ニュース/天気 サーチ】
  - SerpAPI を使ってGoogle検索結果を見せながら応答

- 【📃Azure Cosmos DBに展開する会話履歴】
  - 各使用者ID単位でも保存が可能

---

## 技術構成

| 技術 | 内容 |
|--------|--------|
| 開発言語 | Python / Streamlit |
| 音声認識 | `speech_recognition` |
| 読み上げ | `pyttsx3` (声変更対応) |
| LLM | Azure OpenAI GPT-4o |
| 矩空検索 | SerpAPI (日本語Web検索) |
| データ保存 | Azure Cosmos DB (NoSQL) |

---

## 実行方法

1. secrets.toml を作成
```toml
openai_api_key = "sk-..."
azure_endpoint = "https://xxxx.openai.azure.com"
azure_deployment = "gpt4o"
COSMOS_CONNECTION_STRING = "AccountEndpoint=..."
COSMOS_DB_NAME = "xxxxx"
COSMOS_CONTAINER_NAME = "messages"
SERPAPI_KEY = "your-serpapi-key"
```

2. Streamlit 実行
```bash
streamlit run app.py
```

---

## ライセンス
MIT

---

## 目的
孤独感の解消、こころの軟らぐ場所を目指します。
