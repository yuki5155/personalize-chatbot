# Chatbot API

Personalized Chatbot のバックエンドAPIです。FastAPIとDynamoDBを使用して構築されています。

## 技術スタック

- Python 3.13
- FastAPI
- DynamoDB
- AWS Cognito（認証）
- Docker（開発環境）

## セットアップ

### 環境変数

`.env.example` ファイルを `.env` にコピーして、必要な設定を行います：

```bash
cp .env.example .env
```

### Dockerを使った開発環境の起動

```bash
docker-compose up -d
```

これにより、FastAPIサーバーとDynamoDB Localが起動します。APIは http://localhost:8000 でアクセスできます。

## API ドキュメント

FastAPIの自動生成されたドキュメントは以下のURLでアクセスできます：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 開発

### コンテナに入る

```bash
docker exec -it chatbot-api bash
```

### 手動でアプリケーションを起動

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## DynamoDBテーブル構造

アプリケーションは以下のテーブルを使用します：

- `Users`: ユーザー情報
- `Threads`: チャットスレッド
- `Messages`: チャットメッセージ
- `Settings`: ユーザー設定
- `Presets`: チャットプリセット

これらのテーブルは、アプリケーション起動時に自動的に作成されます。 