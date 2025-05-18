# データベース設計

## 1. データベース概要

### 1.1 データベース選定
- データベース：PostgreSQL
- バージョン：14.x以上
- 文字コード：UTF-8
- 照合順序：en_US.UTF-8

### 1.2 設計方針
- 正規化：第三正規形（3NF）を基本とする
- インデックス：検索条件に応じた適切なインデックス設計
- パーティショニング：大量データテーブルは月次パーティショニング
- バックアップ：日次増分、週次完全バックアップ

## 2. テーブル設計

### 2.1 マスターテーブル

#### 2.1.1 ユーザーマスタ（users）
```sql
CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    department VARCHAR(50),
    position VARCHAR(50),
    contact VARCHAR(100),
    account_status BOOLEAN DEFAULT true,
    last_login_at TIMESTAMP,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_department (department)
);
```

#### 2.1.2 顧客マスタ（customers）
```sql
CREATE TABLE customers (
    customer_id VARCHAR(36) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    contact_name VARCHAR(100),
    contact_department VARCHAR(50),
    contact_phone VARCHAR(20),
    tax_id VARCHAR(50),
    vat_number VARCHAR(50),
    payment_terms VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_company_name (company_name),
    INDEX idx_status (status)
);
```

#### 2.1.3 商品マスタ（products）
```sql
CREATE TABLE products (
    product_id VARCHAR(36) PRIMARY KEY,
    product_code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    unit_price DECIMAL(15,2) NOT NULL,
    tax_category VARCHAR(50),
    category VARCHAR(50),
    unit VARCHAR(20),
    revenue_recognition_method VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_product_code (product_code),
    INDEX idx_category (category)
);
```

### 2.2 トランザクションテーブル

#### 2.2.1 見積書マスタ（quotations）
```sql
CREATE TABLE quotations (
    quotation_id VARCHAR(36) PRIMARY KEY,
    quotation_number VARCHAR(20) NOT NULL UNIQUE,
    quotation_date DATE NOT NULL,
    valid_until DATE NOT NULL,
    customer_id VARCHAR(36) NOT NULL,
    total_amount DECIMAL(15,2) NOT NULL,
    tax_amount DECIMAL(15,2) NOT NULL,
    total_amount_with_tax DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_by VARCHAR(36) NOT NULL,
    approved_by VARCHAR(36),
    approved_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id),
    FOREIGN KEY (approved_by) REFERENCES users(user_id),
    INDEX idx_quotation_number (quotation_number),
    INDEX idx_status (status),
    INDEX idx_customer (customer_id)
);
```

#### 2.2.2 見積書明細（quotation_items）
```sql
CREATE TABLE quotation_items (
    item_id VARCHAR(36) PRIMARY KEY,
    quotation_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    tax_rate DECIMAL(5,2) NOT NULL,
    tax_amount DECIMAL(15,2) NOT NULL,
    amount_with_tax DECIMAL(15,2) NOT NULL,
    description TEXT,
    display_order INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (quotation_id) REFERENCES quotations(quotation_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX idx_quotation (quotation_id)
);
```

### 2.3 監査・ログテーブル

#### 2.3.1 監査ログ（audit_logs）
```sql
CREATE TABLE audit_logs (
    log_id VARCHAR(36) PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(36) NOT NULL,
    action_type VARCHAR(20) NOT NULL,
    old_values JSON,
    new_values JSON,
    user_id VARCHAR(36) NOT NULL,
    ip_address VARCHAR(45),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_entity (entity_type, entity_id),
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_created (created_at)
);
```

#### 2.3.2 エラーログ（error_logs）
```sql
CREATE TABLE error_logs (
    error_id VARCHAR(36) PRIMARY KEY,
    error_type VARCHAR(50) NOT NULL,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    user_id VARCHAR(36),
    entity_type VARCHAR(50),
    entity_id VARCHAR(36),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_error_type (error_type),
    INDEX idx_error_created (created_at)
);
```

## 3. インデックス設計

### 3.1 検索条件に基づくインデックス
- 顧客名検索：customers(company_name)
- 見積書番号検索：quotations(quotation_number)
- ステータス検索：quotations(status), purchase_orders(status), invoices(status)
- 日付範囲検索：quotations(quotation_date), purchase_orders(order_date), invoices(invoice_date)

### 3.2 結合条件に基づくインデックス
- 顧客ID：quotations(customer_id), purchase_orders(customer_id), invoices(customer_id)
- 商品ID：quotation_items(product_id), purchase_order_items(product_id), invoice_items(product_id)

## 4. パーティショニング設計

### 4.1 パーティショニング対象テーブル
- 監査ログ（audit_logs）
- エラーログ（error_logs）
- 請求書（invoices）
- 請求書明細（invoice_items）

### 4.2 パーティショニング方式
- 範囲パーティショニング（月次）
- パーティションキー：created_at
- 保持期間：2年

## 5. バックアップ設計

### 5.1 バックアップ方式
- 完全バックアップ：週1回（日曜日深夜）
- 増分バックアップ：毎日深夜
- トランザクションログ：リアルタイム

### 5.2 バックアップ保持期間
- 完全バックアップ：3ヶ月
- 増分バックアップ：1週間
- トランザクションログ：1ヶ月 