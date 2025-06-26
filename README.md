## 🌸 こころの縁側チャット (Kokoro no Engawa Chat)

**高齢者向け・心に寄り添う音声対話チャットアプリ**  
「誰かと話したい」「ホッとしたい」そんな気持ちに寄り添うキャラクターたちが、やさしく会話します。

🎥 **デモ動画**：  
[https://youtu.be/ETD4_0hYz2I](https://youtu.be/ETD4_0hYz2I)

---

## 🌟 主な機能

- 🎤 **音声入力でチャット**（ローカル起動限定）
- 🧓 **エージェント切替**（癒し／思い出話／元気づけ／ダジャレ）
- 🗣️ **方言対応**：関西弁、東北弁、群馬弁、広島弁、熊本弁、沖縄弁
- 🧠 **Azure OpenAI GPT-4o 連携**
- 🔊 **pyttsx3 による音声読み上げ**（キャラごとに声を変更）
- 🌐 **SerpAPI による検索補助**（天気・ニュースなど）
- 🗃 **会話履歴は Azure Cosmos DB に保存**

---

## 🛠 技術スタック

| 技術 | 内容 |
|------|------|
| Streamlit | UI/アプリケーション構築 |
| Azure OpenAI | 会話AI (GPT-4o) |
| Azure Cosmos DB | 会話履歴保存（NoSQL） |
| LangChain | 会話履歴管理・チャット構築 |
| SerpAPI | Web検索スニペット取得（任意） |
| SpeechRecognition / pyttsx3 | 音声認識／読み上げ（ローカル限定） |

---

## 🚀 起動方法

### ▶ クラウド（Streamlit Cloud など）
```bash
streamlit run app.py
```

### ▶ ローカル（音声入力機能あり）
```bash
pip install -r requirements_local.txt
streamlit run app_with_voice.py
```
※ローカル実行には `PyAudio` のセットアップが必要です（Windowsは `pipwin install pyaudio` を推奨）

---

## 📁 ファイル構成

```
elderly-chatbot/
├── app.py                # Cloud用：テキスト入力版
├── app_with_voice.py     # ローカル用：音声入力対応版
├── requirements.txt       # Cloud用依存パッケージ
├── requirements_local.txt # ローカル用パッケージ（音声対応含む）
├── README.md
└── .streamlit/           # secrets.tomlを格納
```

---

## 💌 制作者より

本アプリは、高齢者や独居者の方との会話のきっかけをつくる実験的な取り組みです。  
今後は声質や感情表現の向上、多言語・方言対応、モバイル展開などを目指しています。
