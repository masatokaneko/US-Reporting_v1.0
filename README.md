# US Reporting System

米国子会社向けの見積書・請求書管理システム

## 機能

- 見積書管理
- 請求書管理
- 顧客管理
- 製品管理
- レポート生成
- システム設定

## 技術スタック

### フロントエンド
- Next.js
- React
- v0.dev
- TypeScript

### バックエンド
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic

### インフラ
- Docker
- Nginx
- GitHub Actions

## 開発環境のセットアップ

### 必要条件
- Node.js 18以上
- Python 3.9以上
- Docker
- Docker Compose

### 環境変数の設定
`.env`ファイルを作成し、以下の環境変数を設定してください：

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=us_reporting
DATABASE_URL=postgresql://postgres:postgres@db:5432/us_reporting

# Backend
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Nginx
NGINX_HOST=localhost
NGINX_PORT=80
```

### インストール手順

1. リポジトリのクローン
```bash
git clone https://github.com/your-username/us-reporting.git
cd us-reporting
```

2. 依存関係のインストール
```bash
# バックエンド
cd backend
poetry install

# フロントエンド
cd ../frontend
npm install
```

3. 開発サーバーの起動
```bash
# Docker Composeを使用する場合
docker-compose -f docker/docker-compose.yml up

# 個別に起動する場合
# バックエンド
cd backend
poetry run uvicorn app.main:app --reload

# フロントエンド
cd frontend
npm run dev
```

## テスト

```bash
# バックエンド
cd backend
poetry run pytest

# フロントエンド
cd frontend
npm test
```

## デプロイ

1. 本番環境用の環境変数を設定
2. Dockerイメージのビルドとプッシュ
3. サーバーでのデプロイ

詳細な手順は `docs/deployment/` を参照してください。

## ドキュメント

- API仕様: `docs/api/`
- アーキテクチャ: `docs/architecture/`
- デプロイメント: `docs/deployment/`
- 開発ガイド: `docs/development/`

## ライセンス

MIT License