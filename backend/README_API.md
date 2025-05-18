# シンプルなFastAPI アプリケーション

これは固定値を返すシンプルなFastAPIアプリケーションです。

## 機能

- 複数のエンドポイントが用意されています
- すべてのエンドポイントは固定値を返します
- JSONレスポンスを提供します

## エンドポイント一覧

- `GET /` - ウェルカムメッセージを返します
- `GET /hello` - 挨拶メッセージを返します
- `GET /users` - 固定のユーザーリストを返します
- `GET /product` - 固定の商品情報を返します
- `GET /info` - APIの情報を返します

## インストール方法

1. リポジトリをクローン
2. 依存関係をインストール
```
pip install -r requirements.txt
```

## 実行方法

```
uvicorn main:app --reload
```

または

```
python main.py
```

サーバーは `http://localhost:8000` で起動します。

## API ドキュメント

FastAPIが自動生成するSwaggerドキュメントは以下のURLで確認できます：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 