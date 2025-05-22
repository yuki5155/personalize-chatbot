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

### PYTHONPATHの設定

開発時には、以下のコマンドでPYTHONPATHを設定することをお勧めします：

```bash
export PYTHONPATH=$PYTHONPATH:/workspaces/backend
```

これにより、モジュールのインポートが正しく動作します。 

```
project_root/
├── src/
│   ├── __init__.py
│   ├── domain/                     # ドメイン層
│   │   ├── __init__.py
│   │   ├── entities/               # エンティティ
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── order.py
│   │   │   └── product.py
│   │   ├── value_objects/          # 値オブジェクト
│   │   │   ├── __init__.py
│   │   │   ├── email.py
│   │   │   ├── money.py
│   │   │   └── user_id.py
│   │   ├── repositories/           # リポジトリインターフェース
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   └── order_repository.py
│   │   ├── services/               # ドメインサービス
│   │   │   ├── __init__.py
│   │   │   ├── user_domain_service.py
│   │   │   └── order_domain_service.py
│   │   ├── events/                 # ドメインイベント
│   │   │   ├── __init__.py
│   │   │   ├── user_created.py
│   │   │   └── order_placed.py
│   │   └── exceptions/             # ドメイン例外
│   │       ├── __init__.py
│   │       ├── domain_exception.py
│   │       └── validation_exception.py
│   │
│   ├── application/                # アプリケーション層
│   │   ├── __init__.py
│   │   ├── services/               # アプリケーションサービス
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py
│   │   │   └── order_service.py
│   │   ├── dto/                    # データ転送オブジェクト
│   │   │   ├── __init__.py
│   │   │   ├── user_dto.py
│   │   │   └── order_dto.py
│   │   ├── commands/               # コマンド
│   │   │   ├── __init__.py
│   │   │   ├── create_user_command.py
│   │   │   └── place_order_command.py
│   │   ├── queries/                # クエリ
│   │   │   ├── __init__.py
│   │   │   ├── user_query.py
│   │   │   └── order_query.py
│   │   └── handlers/               # コマンド/クエリハンドラー
│   │       ├── __init__.py
│   │       ├── command_handlers/
│   │       │   ├── __init__.py
│   │       │   ├── create_user_handler.py
│   │       │   └── place_order_handler.py
│   │       └── query_handlers/
│   │           ├── __init__.py
│   │           ├── user_query_handler.py
│   │           └── order_query_handler.py
│   │
│   ├── infrastructure/             # インフラストラクチャ層
│   │   ├── __init__.py
│   │   ├── persistence/            # データ永続化
│   │   │   ├── __init__.py
│   │   │   ├── database/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── connection.py
│   │   │   │   └── migrations/
│   │   │   ├── repositories/       # リポジトリ実装
│   │   │   │   ├── __init__.py
│   │   │   │   ├── sqlalchemy_user_repository.py
│   │   │   │   └── sqlalchemy_order_repository.py
│   │   │   └── models/             # ORMモデル
│   │   │       ├── __init__.py
│   │   │       ├── user_model.py
│   │   │       └── order_model.py
│   │   ├── external_services/      # 外部サービス連携
│   │   │   ├── __init__.py
│   │   │   ├── email_service.py
│   │   │   └── payment_service.py
│   │   ├── messaging/              # メッセージング
│   │   │   ├── __init__.py
│   │   │   ├── event_bus.py
│   │   │   └── message_queue.py
│   │   └── config/                 # 設定
│   │       ├── __init__.py
│   │       ├── settings.py
│   │       └── dependency_injection.py
│   │
│   └── presentation/               # プレゼンテーション層
│       ├── __init__.py
│       ├── api/                    # REST API
│       │   ├── __init__.py
│       │   ├── controllers/
│       │   │   ├── __init__.py
│       │   │   ├── user_controller.py
│       │   │   └── order_controller.py
│       │   ├── middleware/
│       │   │   ├── __init__.py
│       │   │   ├── auth_middleware.py
│       │   │   └── error_handler.py
│       │   └── schemas/            # APIスキーマ（リクエスト/レスポンス）
│       │       ├── __init__.py
│       │       ├── user_schema.py
│       │       └── order_schema.py
│       ├── cli/                    # コマンドラインインターフェース
│       │   ├── __init__.py
│       │   └── commands.py
│       └── web/                    # Webインターフェース（必要に応じて）
│           ├── __init__.py
│           ├── templates/
│           └── static/
│
├── tests/                          # テスト
│   ├── __init__.py
│   ├── unit/                       # ユニットテスト
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/                # 統合テスト
│   │   ├── repositories/
│   │   └── services/
│   ├── acceptance/                 # 受け入れテスト
│   │   └── api/
│   └── fixtures/                   # テストフィクスチャ
│       ├── __init__.py
│       └── test_data.py
│
├── scripts/                        # スクリプト
│   ├── setup_db.py
│   └── seed_data.py
│
├── docs/                          # ドキュメント
│   ├── architecture.md
│   ├── api_specification.md
│   └── deployment.md
│
├── requirements/                   # 依存関係
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
│
├── docker/                        # Docker設定
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .env.example                   # 環境変数サンプル
├── .gitignore
├── README.md
├── pyproject.toml                 # プロジェクト設定
└── main.py                        # アプリケーションエントリーポイント

```