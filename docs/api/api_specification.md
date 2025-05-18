# 米国子会社向け見積書・請求書管理システム API設計書

## 1. API概要

### 1.1 アーキテクチャ概要
- RESTful API設計
- JSON形式のデータ交換
- JWT（JSON Web Token）による認証
- HTTPS通信のみサポート
- ステートレスな設計
- バージョニング対応（URLパスにバージョン番号含む）

### 1.2 ベースURL
```
https://api.invoicesystem.example.com/v1
```

### 1.3 共通仕様

#### 1.3.1 認証ヘッダー
```
Authorization: Bearer {jwt_token}
```

#### 1.3.2 標準レスポンス形式
```json
{
  "success": true,
  "data": {
    // レスポンスデータ
  },
  "meta": {
    "timestamp": "2023-01-01T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

#### 1.3.3 エラーレスポンス形式
```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "入力データが不正です",
    "details": [
      {
        "field": "email",
        "message": "有効なメールアドレスを入力してください"
      }
    ]
  },
  "meta": {
    "timestamp": "2023-01-01T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

#### 1.3.4 ページネーション仕様
リクエスト:
```
GET /resources?page=2&per_page=25&sort=created_at:desc
```

レスポンス:
```json
{
  "success": true,
  "data": [
    // リソースの配列
  ],
  "meta": {
    "pagination": {
      "page": 2,
      "per_page": 25,
      "total_items": 143,
      "total_pages": 6,
      "has_next_page": true,
      "has_prev_page": true
    },
    "timestamp": "2023-01-01T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

## 3. ユーザー管理API

### 3.1 ユーザー一覧取得

**エンドポイント**: `GET /users`

**クエリパラメータ**:
- `page`: ページ番号（デフォルト: 1）
- `per_page`: 1ページあたりの件数（デフォルト: 20、最大: 100）
- `sort`: ソート条件（例: `last_name:asc`, `created_at:desc`）
- `status`: ステータスによるフィルタ（例: `active`, `inactive`）
- `department`: 部署によるフィルタ
- `search`: 検索キーワード（名前、メールアドレスなど）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "user_id": "usr-123456789",
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "department": "Sales",
      "position": "Sales Manager",
      "status": "active",
      "last_login": "2023-01-01T10:30:00Z",
      "created_at": "2022-01-01T09:00:00Z"
    },
    {
      "user_id": "usr-987654321",
      "email": "jane.smith@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "department": "Finance",
      "position": "Accountant",
      "status": "active",
      "last_login": "2023-01-01T11:45:00Z",
      "created_at": "2022-02-15T14:30:00Z"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_items": 42,
      "total_pages": 3,
      "has_next_page": true,
      "has_prev_page": false
    },
    "timestamp": "2023-01-01T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 3.2 ユーザー詳細取得

**エンドポイント**: `GET /users/{user_id}`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "user_id": "usr-123456789",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "department": "Sales",
    "position": "Sales Manager",
    "phone": "+1-234-567-8900",
    "status": "active",
    "create_quote_permission": true,
    "approve_quote_permission": true,
    "manage_order_permission": true,
    "create_invoice_permission": false,
    "approve_invoice_permission": false,
    "manage_revenue_permission": false,
    "admin_permission": false,
    "roles": [
      {
        "role_id": "role-123456789",
        "role_name": "Sales Manager"
      }
    ],
    "last_login": "2023-01-01T10:30:00Z",
    "created_at": "2022-01-01T09:00:00Z",
    "created_by": {
      "user_id": "usr-admin",
      "first_name": "Admin",
      "last_name": "User"
    },
    "updated_at": "2022-06-15T14:20:00Z",
    "updated_by": {
      "user_id": "usr-admin",
      "first_name": "Admin",
      "last_name": "User"
    }
  },
  "meta": {
    "timestamp": "2023-01-01T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 3.3 ユーザー作成

**エンドポイント**: `POST /users`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "email": "new.user@example.com",
  "first_name": "New",
  "last_name": "User",
  "department": "Marketing",
  "position": "Marketing Specialist",
  "phone": "+1-234-567-8901",
  "create_quote_permission": true,
  "approve_quote_permission": false,
  "manage_order_permission": true,
  "create_invoice_permission": false,
  "approve_invoice_permission": false,
  "manage_revenue_permission": false,
  "admin_permission": false,
  "role_ids": ["role-123456789"]
}
```

**レスポンス (201 Created)**:
```json
{
  "success": true,
  "data": {
    "user_id": "usr-new123456",
    "email": "new.user@example.com",
    "first_name": "New",
    "last_name": "User",
    "department": "Marketing",
    "position": "Marketing Specialist",
    "phone": "+1-234-567-8901",
    "status": "active",
    "temporary_password": "Temp1234!",
    "created_at": "2023-01-01T12:00:00Z",
    "created_by": {
      "user_id": "usr-admin",
      "first_name": "Admin",
      "last_name": "User"
    }
  },
  "meta": {
    "timestamp": "2023-01-01T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 3.4 ユーザー更新

**エンドポイント**: `PUT /users/{user_id}`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "first_name": "Updated",
  "last_name": "User",
  "department": "Marketing",
  "position": "Senior Marketing Specialist",
  "phone": "+1-234-567-8901",
  "create_quote_permission": true,
  "approve_quote_permission": true,
  "manage_order_permission": true,
  "create_invoice_permission": false,
  "approve_invoice_permission": false,
  "manage_revenue_permission": false,
  "admin_permission": false,
  "role_ids": ["role-123456789", "role-987654321"]
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "user_id": "usr-123456789",
    "email": "user@example.com",
    "first_name": "Updated",
    "last_name": "User",
    "department": "Marketing",
    "position": "Senior Marketing Specialist",
    "phone": "+1-234-567-8901",
    "status": "active",
    "created_at": "2022-01-01T09:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z",
    "updated_by": {
      "user_id": "usr-admin",
      "first_name": "Admin",
      "last_name": "User"
    }
  },
  "meta": {
    "timestamp": "2023-01-01T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

## 4. 見積書API

### 4.1 見積書一覧取得

**エンドポイント**: `GET /quotations`

**クエリパラメータ**:
- `page`: ページ番号（デフォルト: 1）
- `per_page`: 1ページあたりの件数（デフォルト: 20、最大: 100）
- `sort`: ソート条件（例: `quotation_date:desc`, `total_amount:desc`）
- `status`: ステータスによるフィルタ（例: `draft`, `approved`, `issued`）
- `customer_id`: 顧客IDによるフィルタ
- `date_from`: 見積日の開始日（ISO 8601形式）
- `date_to`: 見積日の終了日（ISO 8601形式）
- `search`: 検索キーワード（見積書番号、顧客名など）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "quotation_id": "qt-123456789",
      "quotation_number": "QT-202301-0001",
      "quotation_date": "2023-01-15",
      "expiration_date": "2023-02-15",
      "customer": {
        "customer_id": "cus-123456789",
        "company_name": "Acme Corporation"
      },
      "subtotal": 5000.00,
      "tax_amount": 400.00,
      "total_amount": 5400.00,
      "status": "issued",
      "created_at": "2023-01-10T09:30:00Z",
      "created_by": {
        "user_id": "usr-123456789",
        "first_name": "John",
        "last_name": "Doe"
      }
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_items": 42,
      "total_pages": 3,
      "has_next_page": true,
      "has_prev_page": false
    },
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 4.2 見積書詳細取得

**エンドポイント**: `GET /quotations/{quotation_id}`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "quotation_id": "qt-123456789",
    "quotation_number": "QT-202301-0001",
    "quotation_date": "2023-01-15",
    "expiration_date": "2023-02-15",
    "customer": {
      "customer_id": "cus-123456789",
      "company_name": "Acme Corporation",
      "address_line1": "123 Main Street",
      "address_line2": "Suite 100",
      "city": "New York",
      "state": "NY",
      "zip_code": "10001",
      "country": "USA",
      "contact_name": "John Contact"
    },
    "items": [
      {
        "item_id": "qti-123456789",
        "product": {
          "product_id": "prod-123456789",
          "product_code": "SRV-CONSULT",
          "product_name": "Consulting Services"
        },
        "quantity": 10,
        "unit_price": 400.00,
        "subtotal": 4000.00,
        "tax_rate": 8.00,
        "tax_amount": 320.00,
        "total_amount": 4320.00,
        "description": "Strategic consulting sessions",
        "sort_order": 1
      }
    ],
    "subtotal": 5000.00,
    "tax_amount": 400.00,
    "total_amount": 5400.00,
    "status": "issued",
    "notes": "Thank you for your business!",
    "status_history": [
      {
        "status": "draft",
        "changed_at": "2023-01-10T09:30:00Z",
        "changed_by": {
          "user_id": "usr-123456789",
          "first_name": "John",
          "last_name": "Doe"
        }
      }
    ],
    "created_at": "2023-01-10T09:30:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    },
    "approver": {
      "user_id": "usr-manager",
      "first_name": "Manager",
      "last_name": "Approval"
    },
    "approved_at": "2023-01-12T14:30:00Z",
    "updated_at": "2023-01-13T09:45:00Z",
    "updated_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 4.3 見積書作成

**エンドポイント**: `POST /quotations`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "quotation_date": "2023-01-25",
  "expiration_date": "2023-02-25",
  "customer_id": "cus-123456789",
  "items": [
    {
      "product_id": "prod-123456789",
      "quantity": 10,
      "unit_price": 400.00,
      "tax_rate": 8.00,
      "description": "Strategic consulting sessions",
      "sort_order": 1
    }
  ],
  "notes": "Thank you for your business!"
}
```

**レスポンス (201 Created)**:
```json
{
  "success": true,
  "data": {
    "quotation_id": "qt-new123456",
    "quotation_number": "QT-202301-0003",
    "quotation_date": "2023-01-25",
    "expiration_date": "2023-02-25",
    "customer": {
      "customer_id": "cus-123456789",
      "company_name": "Acme Corporation"
    },
    "items": [
      {
        "item_id": "qti-new123456",
        "product": {
          "product_id": "prod-123456789",
          "product_code": "SRV-CONSULT",
          "product_name": "Consulting Services"
        },
        "quantity": 10,
        "unit_price": 400.00,
        "subtotal": 4000.00,
        "tax_rate": 8.00,
        "tax_amount": 320.00,
        "total_amount": 4320.00,
        "description": "Strategic consulting sessions",
        "sort_order": 1
      }
    ],
    "subtotal": 5000.00,
    "tax_amount": 400.00,
    "total_amount": 5400.00,
    "status": "draft",
    "notes": "Thank you for your business!",
    "created_at": "2023-01-21T12:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 4.4 見積書承認申請

**エンドポイント**: `POST /quotations/{quotation_id}/request-approval`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "approver_id": "usr-manager",
  "notes": "Please review this quotation"
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "quotation_id": "qt-123456789",
    "quotation_number": "QT-202301-0003",
    "status": "pending_approval",
    "previous_status": "draft",
    "approver": {
      "user_id": "usr-manager",
      "first_name": "Manager",
      "last_name": "Approval"
    },
    "updated_at": "2023-01-21T12:15:00Z"
  },
  "meta": {
    "timestamp": "2023-01-21T12:15:00Z",
    "request_id": "req-123456789"
  }
}
```

### 4.5 見積書承認処理

**エンドポイント**: `POST /quotations/{quotation_id}/approve`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "notes": "Approved with minor comments"
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "quotation_id": "qt-123456789",
    "quotation_number": "QT-202301-0003",
    "status": "approved",
    "previous_status": "pending_approval",
    "approved_at": "2023-01-21T14:30:00Z",
    "approver": {
      "user_id": "usr-manager",
      "first_name": "Manager",
      "last_name": "Approval"
    },
    "updated_at": "2023-01-21T14:30:00Z"
  },
  "meta": {
    "timestamp": "2023-01-21T14:30:00Z",
    "request_id": "req-123456789"
  }
}
```

### 4.6 見積書発行

**エンドポイント**: `POST /quotations/{quotation_id}/issue`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "email_recipient": "client@acmecorp.com",
  "email_cc": ["account.manager@example.com"],
  "email_subject": "Quotation QT-202301-0003 for Consulting Services",
  "email_body": "Please find attached our quotation for consulting services. Feel free to contact us if you have any questions."
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "quotation_id": "qt-123456789",
    "quotation_number": "QT-202301-0003",
    "status": "issued",
    "previous_status": "approved",
    "issued_at": "2023-01-21T15:00:00Z",
    "issued_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    },
    "email_sent": true,
    "email_recipient": "client@acmecorp.com",
    "updated_at": "2023-01-21T15:00:00Z"
  },
  "meta": {
    "timestamp": "2023-01-21T15:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 4.7 見積書PDF取得

**エンドポイント**: `GET /quotations/{quotation_id}/pdf`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス**:
- PDF ファイル（Content-Type: application/pdf）

## 5. 請求書API

### 5.1 請求書一覧取得

**エンドポイント**: `GET /invoices`

**クエリパラメータ**:
- `page`: ページ番号（デフォルト: 1）
- `per_page`: 1ページあたりの件数（デフォルト: 20、最大: 100）
- `sort`: ソート条件（例: `invoice_date:desc`, `total_amount:desc`）
- `status`: ステータスによるフィルタ（例: `draft`, `approved`, `issued`, `paid`）
- `customer_id`: 顧客IDによるフィルタ
- `date_from`: 請求日の開始日（ISO 8601形式）
- `date_to`: 請求日の終了日（ISO 8601形式）
- `search`: 検索キーワード（請求書番号、顧客名など）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "invoice_id": "inv-123456789",
      "invoice_number": "INV-202301-0001",
      "invoice_date": "2023-01-15",
      "due_date": "2023-02-15",
      "customer": {
        "customer_id": "cus-123456789",
        "company_name": "Acme Corporation"
      },
      "subtotal": 5000.00,
      "tax_amount": 400.00,
      "total_amount": 5400.00,
      "status": "issued",
      "payment_status": "unpaid",
      "created_at": "2023-01-10T09:30:00Z",
      "created_by": {
        "user_id": "usr-123456789",
        "first_name": "John",
        "last_name": "Doe"
      }
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_items": 42,
      "total_pages": 3,
      "has_next_page": true,
      "has_prev_page": false
    },
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 5.2 請求書詳細取得

**エンドポイント**: `GET /invoices/{invoice_id}`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "invoice_id": "inv-123456789",
    "invoice_number": "INV-202301-0001",
    "invoice_date": "2023-01-15",
    "due_date": "2023-02-15",
    "customer": {
      "customer_id": "cus-123456789",
      "company_name": "Acme Corporation",
      "address_line1": "123 Main Street",
      "address_line2": "Suite 100",
      "city": "New York",
      "state": "NY",
      "zip_code": "10001",
      "country": "USA",
      "contact_name": "John Contact"
    },
    "items": [
      {
        "item_id": "ivi-123456789",
        "product": {
          "product_id": "prod-123456789",
          "product_code": "SRV-CONSULT",
          "product_name": "Consulting Services"
        },
        "quantity": 10,
        "unit_price": 400.00,
        "subtotal": 4000.00,
        "tax_rate": 8.00,
        "tax_amount": 320.00,
        "total_amount": 4320.00,
        "description": "Strategic consulting sessions",
        "sort_order": 1
      }
    ],
    "subtotal": 5000.00,
    "tax_amount": 400.00,
    "total_amount": 5400.00,
    "status": "issued",
    "payment_status": "unpaid",
    "payment_due_date": "2023-02-15",
    "payment_terms": "Net 30",
    "notes": "Thank you for your business!",
    "status_history": [
      {
        "status": "draft",
        "changed_at": "2023-01-10T09:30:00Z",
        "changed_by": {
          "user_id": "usr-123456789",
          "first_name": "John",
          "last_name": "Doe"
        }
      }
    ],
    "created_at": "2023-01-10T09:30:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    },
    "approver": {
      "user_id": "usr-manager",
      "first_name": "Manager",
      "last_name": "Approval"
    },
    "approved_at": "2023-01-12T14:30:00Z",
    "updated_at": "2023-01-13T09:45:00Z",
    "updated_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 5.3 請求書作成

**エンドポイント**: `POST /invoices`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "invoice_date": "2023-01-25",
  "due_date": "2023-02-25",
  "customer_id": "cus-123456789",
  "items": [
    {
      "product_id": "prod-123456789",
      "quantity": 10,
      "unit_price": 400.00,
      "tax_rate": 8.00,
      "description": "Strategic consulting sessions",
      "sort_order": 1
    }
  ],
  "payment_terms": "Net 30",
  "notes": "Thank you for your business!"
}
```

**レスポンス (201 Created)**:
```json
{
  "success": true,
  "data": {
    "invoice_id": "inv-new123456",
    "invoice_number": "INV-202301-0003",
    "invoice_date": "2023-01-25",
    "due_date": "2023-02-25",
    "customer": {
      "customer_id": "cus-123456789",
      "company_name": "Acme Corporation"
    },
    "items": [
      {
        "item_id": "ivi-new123456",
        "product": {
          "product_id": "prod-123456789",
          "product_code": "SRV-CONSULT",
          "product_name": "Consulting Services"
        },
        "quantity": 10,
        "unit_price": 400.00,
        "subtotal": 4000.00,
        "tax_rate": 8.00,
        "tax_amount": 320.00,
        "total_amount": 4320.00,
        "description": "Strategic consulting sessions",
        "sort_order": 1
      }
    ],
    "subtotal": 5000.00,
    "tax_amount": 400.00,
    "total_amount": 5400.00,
    "status": "draft",
    "payment_status": "unpaid",
    "payment_terms": "Net 30",
    "notes": "Thank you for your business!",
    "created_at": "2023-01-21T12:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 5.4 請求書承認申請

**エンドポイント**: `POST /invoices/{invoice_id}/request-approval`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "approver_id": "usr-manager",
  "notes": "Please review this invoice"
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "invoice_id": "inv-123456789",
    "invoice_number": "INV-202301-0003",
    "status": "pending_approval",
    "previous_status": "draft",
    "approver": {
      "user_id": "usr-manager",
      "first_name": "Manager",
      "last_name": "Approval"
    },
    "updated_at": "2023-01-21T12:15:00Z"
  },
  "meta": {
    "timestamp": "2023-01-21T12:15:00Z",
    "request_id": "req-123456789"
  }
}
```

### 5.5 請求書承認処理

**エンドポイント**: `POST /invoices/{invoice_id}/approve`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "notes": "Approved with minor comments"
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "invoice_id": "inv-123456789",
    "invoice_number": "INV-202301-0003",
    "status": "approved",
    "previous_status": "pending_approval",
    "approved_at": "2023-01-21T14:30:00Z",
    "approver": {
      "user_id": "usr-manager",
      "first_name": "Manager",
      "last_name": "Approval"
    },
    "updated_at": "2023-01-21T14:30:00Z"
  },
  "meta": {
    "timestamp": "2023-01-21T14:30:00Z",
    "request_id": "req-123456789"
  }
}
```

### 5.6 請求書発行

**エンドポイント**: `POST /invoices/{invoice_id}/issue`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "email_recipient": "client@acmecorp.com",
  "email_cc": ["account.manager@example.com"],
  "email_subject": "Invoice INV-202301-0003 for Consulting Services",
  "email_body": "Please find attached our invoice for consulting services. Payment is due within 30 days."
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "invoice_id": "inv-123456789",
    "invoice_number": "INV-202301-0003",
    "status": "issued",
    "previous_status": "approved",
    "issued_at": "2023-01-21T15:00:00Z",
    "issued_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    },
    "email_sent": true,
    "email_recipient": "client@acmecorp.com",
    "updated_at": "2023-01-21T15:00:00Z"
  },
  "meta": {
    "timestamp": "2023-01-21T15:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 5.7 請求書PDF取得

**エンドポイント**: `GET /invoices/{invoice_id}/pdf`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス**:
- PDF ファイル（Content-Type: application/pdf）

### 5.8 入金登録

**エンドポイント**: `POST /invoices/{invoice_id}/payments`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "payment_date": "2023-02-10",
  "payment_amount": 5400.00,
  "payment_method": "bank_transfer",
  "reference_number": "BT123456789",
  "notes": "Payment received via bank transfer"
}
```

**レスポンス (201 Created)**:
```json
{
  "success": true,
  "data": {
    "payment_id": "pay-123456789",
    "invoice_id": "inv-123456789",
    "invoice_number": "INV-202301-0003",
    "payment_date": "2023-02-10",
    "payment_amount": 5400.00,
    "payment_method": "bank_transfer",
    "reference_number": "BT123456789",
    "notes": "Payment received via bank transfer",
    "payment_status": "completed",
    "created_at": "2023-02-10T10:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-02-10T10:00:00Z",
    "request_id": "req-123456789"
  }
}
```

## 6. 顧客API

### 6.1 顧客一覧取得

**エンドポイント**: `GET /customers`

**クエリパラメータ**:
- `page`: ページ番号（デフォルト: 1）
- `per_page`: 1ページあたりの件数（デフォルト: 20、最大: 100）
- `sort`: ソート条件（例: `company_name:asc`, `created_at:desc`）
- `status`: ステータスによるフィルタ（例: `active`, `inactive`）
- `search`: 検索キーワード（会社名、担当者名など）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "customer_id": "cus-123456789",
      "company_name": "Acme Corporation",
      "contact_name": "John Contact",
      "email": "contact@acmecorp.com",
      "phone": "+1-234-567-8900",
      "status": "active",
      "created_at": "2022-01-01T09:00:00Z",
      "created_by": {
        "user_id": "usr-123456789",
        "first_name": "John",
        "last_name": "Doe"
      }
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_items": 42,
      "total_pages": 3,
      "has_next_page": true,
      "has_prev_page": false
    },
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 6.2 顧客詳細取得

**エンドポイント**: `GET /customers/{customer_id}`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "customer_id": "cus-123456789",
    "company_name": "Acme Corporation",
    "contact_name": "John Contact",
    "email": "contact@acmecorp.com",
    "phone": "+1-234-567-8900",
    "address": {
      "address_line1": "123 Main Street",
      "address_line2": "Suite 100",
      "city": "New York",
      "state": "NY",
      "zip_code": "10001",
      "country": "USA"
    },
    "billing_address": {
      "address_line1": "123 Main Street",
      "address_line2": "Suite 100",
      "city": "New York",
      "state": "NY",
      "zip_code": "10001",
      "country": "USA"
    },
    "payment_terms": "Net 30",
    "tax_id": "12-3456789",
    "status": "active",
    "notes": "Important client",
    "created_at": "2022-01-01T09:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    },
    "updated_at": "2022-06-15T14:20:00Z",
    "updated_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 6.3 顧客作成

**エンドポイント**: `POST /customers`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "company_name": "New Company Inc.",
  "contact_name": "Jane Smith",
  "email": "contact@newcompany.com",
  "phone": "+1-234-567-8901",
  "address": {
    "address_line1": "456 Business Ave",
    "address_line2": "Floor 5",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94105",
    "country": "USA"
  },
  "billing_address": {
    "address_line1": "456 Business Ave",
    "address_line2": "Floor 5",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94105",
    "country": "USA"
  },
  "payment_terms": "Net 30",
  "tax_id": "98-7654321",
  "notes": "New client from referral"
}
```

**レスポンス (201 Created)**:
```json
{
  "success": true,
  "data": {
    "customer_id": "cus-new123456",
    "company_name": "New Company Inc.",
    "contact_name": "Jane Smith",
    "email": "contact@newcompany.com",
    "phone": "+1-234-567-8901",
    "address": {
      "address_line1": "456 Business Ave",
      "address_line2": "Floor 5",
      "city": "San Francisco",
      "state": "CA",
      "zip_code": "94105",
      "country": "USA"
    },
    "billing_address": {
      "address_line1": "456 Business Ave",
      "address_line2": "Floor 5",
      "city": "San Francisco",
      "state": "CA",
      "zip_code": "94105",
      "country": "USA"
    },
    "payment_terms": "Net 30",
    "tax_id": "98-7654321",
    "status": "active",
    "notes": "New client from referral",
    "created_at": "2023-01-21T12:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 6.4 顧客更新

**エンドポイント**: `PUT /customers/{customer_id}`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "company_name": "Updated Company Inc.",
  "contact_name": "Jane Smith",
  "email": "contact@updatedcompany.com",
  "phone": "+1-234-567-8902",
  "address": {
    "address_line1": "789 Corporate Blvd",
    "address_line2": "Suite 200",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94105",
    "country": "USA"
  },
  "billing_address": {
    "address_line1": "789 Corporate Blvd",
    "address_line2": "Suite 200",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94105",
    "country": "USA"
  },
  "payment_terms": "Net 45",
  "tax_id": "98-7654321",
  "notes": "Updated contact information"
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "customer_id": "cus-123456789",
    "company_name": "Updated Company Inc.",
    "contact_name": "Jane Smith",
    "email": "contact@updatedcompany.com",
    "phone": "+1-234-567-8902",
    "address": {
      "address_line1": "789 Corporate Blvd",
      "address_line2": "Suite 200",
      "city": "San Francisco",
      "state": "CA",
      "zip_code": "94105",
      "country": "USA"
    },
    "billing_address": {
      "address_line1": "789 Corporate Blvd",
      "address_line2": "Suite 200",
      "city": "San Francisco",
      "state": "CA",
      "zip_code": "94105",
      "country": "USA"
    },
    "payment_terms": "Net 45",
    "tax_id": "98-7654321",
    "status": "active",
    "notes": "Updated contact information",
    "created_at": "2022-01-01T09:00:00Z",
    "updated_at": "2023-01-21T12:00:00Z",
    "updated_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 6.5 顧客ステータス更新

**エンドポイント**: `PATCH /customers/{customer_id}/status`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "status": "inactive",
  "notes": "Customer requested to be marked as inactive"
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "customer_id": "cus-123456789",
    "company_name": "Acme Corporation",
    "status": "inactive",
    "previous_status": "active",
    "updated_at": "2023-01-21T12:00:00Z",
    "updated_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

## 7. 製品API

### 7.1 製品一覧取得

**エンドポイント**: `GET /products`

**クエリパラメータ**:
- `page`: ページ番号（デフォルト: 1）
- `per_page`: 1ページあたりの件数（デフォルト: 20、最大: 100）
- `sort`: ソート条件（例: `product_name:asc`, `created_at:desc`）
- `category`: カテゴリによるフィルタ
- `status`: ステータスによるフィルタ（例: `active`, `inactive`）
- `search`: 検索キーワード（製品名、製品コードなど）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "product_id": "prod-123456789",
      "product_code": "SRV-CONSULT",
      "product_name": "Consulting Services",
      "category": "Services",
      "unit_price": 400.00,
      "tax_rate": 8.00,
      "status": "active",
      "created_at": "2022-01-01T09:00:00Z",
      "created_by": {
        "user_id": "usr-123456789",
        "first_name": "John",
        "last_name": "Doe"
      }
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_items": 42,
      "total_pages": 3,
      "has_next_page": true,
      "has_prev_page": false
    },
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 7.2 製品詳細取得

**エンドポイント**: `GET /products/{product_id}`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "product_id": "prod-123456789",
    "product_code": "SRV-CONSULT",
    "product_name": "Consulting Services",
    "description": "Professional consulting services for business strategy and implementation",
    "category": "Services",
    "unit_price": 400.00,
    "tax_rate": 8.00,
    "unit": "hour",
    "minimum_quantity": 1,
    "status": "active",
    "notes": "Standard consulting rate",
    "created_at": "2022-01-01T09:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    },
    "updated_at": "2022-06-15T14:20:00Z",
    "updated_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 7.3 製品作成

**エンドポイント**: `POST /products`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "product_code": "SRV-TRAIN",
  "product_name": "Training Services",
  "description": "Professional training services for software and business processes",
  "category": "Services",
  "unit_price": 500.00,
  "tax_rate": 8.00,
  "unit": "day",
  "minimum_quantity": 1,
  "notes": "Standard training rate per day"
}
```

**レスポンス (201 Created)**:
```json
{
  "success": true,
  "data": {
    "product_id": "prod-new123456",
    "product_code": "SRV-TRAIN",
    "product_name": "Training Services",
    "description": "Professional training services for software and business processes",
    "category": "Services",
    "unit_price": 500.00,
    "tax_rate": 8.00,
    "unit": "day",
    "minimum_quantity": 1,
    "status": "active",
    "notes": "Standard training rate per day",
    "created_at": "2023-01-21T12:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 7.4 製品更新

**エンドポイント**: `PUT /products/{product_id}`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "product_code": "SRV-TRAIN-PREMIUM",
  "product_name": "Premium Training Services",
  "description": "Advanced professional training services for software and business processes",
  "category": "Services",
  "unit_price": 750.00,
  "tax_rate": 8.00,
  "unit": "day",
  "minimum_quantity": 1,
  "notes": "Premium training rate per day"
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "product_id": "prod-123456789",
    "product_code": "SRV-TRAIN-PREMIUM",
    "product_name": "Premium Training Services",
    "description": "Advanced professional training services for software and business processes",
    "category": "Services",
    "unit_price": 750.00,
    "tax_rate": 8.00,
    "unit": "day",
    "minimum_quantity": 1,
    "status": "active",
    "notes": "Premium training rate per day",
    "created_at": "2022-01-01T09:00:00Z",
    "updated_at": "2023-01-21T12:00:00Z",
    "updated_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 7.5 製品ステータス更新

**エンドポイント**: `PATCH /products/{product_id}/status`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "status": "inactive",
  "notes": "Product temporarily discontinued"
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "product_id": "prod-123456789",
    "product_code": "SRV-TRAIN-PREMIUM",
    "product_name": "Premium Training Services",
    "status": "inactive",
    "previous_status": "active",
    "updated_at": "2023-01-21T12:00:00Z",
    "updated_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

## 8. レポートAPI

### 8.1 売上レポート取得

**エンドポイント**: `GET /reports/sales`

**クエリパラメータ**:
- `date_from`: 開始日（ISO 8601形式）
- `date_to`: 終了日（ISO 8601形式）
- `group_by`: グループ化条件（例: `day`, `week`, `month`, `quarter`, `year`）
- `product_id`: 製品IDによるフィルタ
- `customer_id`: 顧客IDによるフィルタ
- `format`: 出力形式（例: `json`, `csv`, `pdf`）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_sales": 150000.00,
      "total_tax": 12000.00,
      "total_amount": 162000.00,
      "total_invoices": 25,
      "average_invoice_amount": 6000.00
    },
    "periods": [
      {
        "period": "2023-01",
        "sales": 50000.00,
        "tax": 4000.00,
        "total": 54000.00,
        "invoice_count": 8
      },
      {
        "period": "2023-02",
        "sales": 100000.00,
        "tax": 8000.00,
        "total": 108000.00,
        "invoice_count": 17
      }
    ],
    "products": [
      {
        "product_id": "prod-123456789",
        "product_name": "Consulting Services",
        "quantity": 250,
        "sales": 100000.00,
        "tax": 8000.00,
        "total": 108000.00
      }
    ],
    "customers": [
      {
        "customer_id": "cus-123456789",
        "company_name": "Acme Corporation",
        "sales": 75000.00,
        "tax": 6000.00,
        "total": 81000.00,
        "invoice_count": 12
      }
    ]
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 8.2 請求書レポート取得

**エンドポイント**: `GET /reports/invoices`

**クエリパラメータ**:
- `date_from`: 開始日（ISO 8601形式）
- `date_to`: 終了日（ISO 8601形式）
- `status`: ステータスによるフィルタ（例: `issued`, `paid`, `overdue`）
- `customer_id`: 顧客IDによるフィルタ
- `format`: 出力形式（例: `json`, `csv`, `pdf`）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_invoices": 25,
      "total_amount": 162000.00,
      "paid_amount": 108000.00,
      "unpaid_amount": 54000.00,
      "overdue_amount": 27000.00
    },
    "status_summary": {
      "issued": 25,
      "paid": 17,
      "overdue": 8
    },
    "invoices": [
      {
        "invoice_id": "inv-123456789",
        "invoice_number": "INV-202301-0001",
        "invoice_date": "2023-01-15",
        "due_date": "2023-02-15",
        "customer": {
          "customer_id": "cus-123456789",
          "company_name": "Acme Corporation"
        },
        "amount": 5400.00,
        "status": "paid",
        "paid_date": "2023-02-10"
      }
    ],
    "aging_summary": {
      "current": 27000.00,
      "1-30_days": 13500.00,
      "31-60_days": 8100.00,
      "61-90_days": 5400.00,
      "over_90_days": 0.00
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 8.3 顧客別レポート取得

**エンドポイント**: `GET /reports/customers`

**クエリパラメータ**:
- `date_from`: 開始日（ISO 8601形式）
- `date_to`: 終了日（ISO 8601形式）
- `customer_id`: 顧客IDによるフィルタ
- `format`: 出力形式（例: `json`, `csv`, `pdf`）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_customers": 15,
      "active_customers": 12,
      "total_sales": 150000.00,
      "average_sales_per_customer": 10000.00
    },
    "customers": [
      {
        "customer_id": "cus-123456789",
        "company_name": "Acme Corporation",
        "status": "active",
        "total_sales": 75000.00,
        "total_invoices": 12,
        "average_invoice_amount": 6250.00,
        "last_purchase_date": "2023-01-15",
        "payment_history": {
          "on_time": 10,
          "late": 2,
          "average_days_to_pay": 25
        },
        "products": [
          {
            "product_id": "prod-123456789",
            "product_name": "Consulting Services",
            "quantity": 150,
            "amount": 60000.00
          }
        ]
      }
    ],
    "top_customers": [
      {
        "customer_id": "cus-123456789",
        "company_name": "Acme Corporation",
        "total_sales": 75000.00,
        "percentage": 50.00
      }
    ]
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 8.4 製品別レポート取得

**エンドポイント**: `GET /reports/products`

**クエリパラメータ**:
- `date_from`: 開始日（ISO 8601形式）
- `date_to`: 終了日（ISO 8601形式）
- `product_id`: 製品IDによるフィルタ
- `format`: 出力形式（例: `json`, `csv`, `pdf`）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_products": 10,
      "active_products": 8,
      "total_sales": 150000.00,
      "average_sales_per_product": 15000.00
    },
    "products": [
      {
        "product_id": "prod-123456789",
        "product_code": "SRV-CONSULT",
        "product_name": "Consulting Services",
        "status": "active",
        "total_sales": 100000.00,
        "total_quantity": 250,
        "average_price": 400.00,
        "customers": [
          {
            "customer_id": "cus-123456789",
            "company_name": "Acme Corporation",
            "quantity": 150,
            "amount": 60000.00
          }
        ]
      }
    ],
    "top_products": [
      {
        "product_id": "prod-123456789",
        "product_name": "Consulting Services",
        "total_sales": 100000.00,
        "percentage": 66.67
      }
    ],
    "sales_trend": [
      {
        "period": "2023-01",
        "total_sales": 50000.00,
        "quantity": 125
      },
      {
        "period": "2023-02",
        "total_sales": 50000.00,
        "quantity": 125
      }
    ]
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 8.5 税務レポート取得

**エンドポイント**: `GET /reports/tax`

**クエリパラメータ**:
- `date_from`: 開始日（ISO 8601形式）
- `date_to`: 終了日（ISO 8601形式）
- `tax_rate`: 税率によるフィルタ
- `format`: 出力形式（例: `json`, `csv`, `pdf`）

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_taxable_sales": 150000.00,
      "total_tax_amount": 12000.00,
      "total_invoices": 25
    },
    "tax_rates": [
      {
        "tax_rate": 8.00,
        "taxable_sales": 150000.00,
        "tax_amount": 12000.00,
        "invoice_count": 25
      }
    ],
    "periods": [
      {
        "period": "2023-01",
        "taxable_sales": 50000.00,
        "tax_amount": 4000.00,
        "invoice_count": 8
      },
      {
        "period": "2023-02",
        "taxable_sales": 100000.00,
        "tax_amount": 8000.00,
        "invoice_count": 17
      }
    ],
    "products": [
      {
        "product_id": "prod-123456789",
        "product_name": "Consulting Services",
        "tax_rate": 8.00,
        "taxable_sales": 100000.00,
        "tax_amount": 8000.00
      }
    ]
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

## 9. システム設定API

### 9.1 税率設定一覧取得

**エンドポイント**: `GET /settings/tax-rates`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "tax_rates": [
      {
        "tax_rate_id": "tax-123456789",
        "rate": 8.00,
        "name": "Standard Rate",
        "description": "Standard sales tax rate",
        "is_default": true,
        "effective_from": "2023-01-01",
        "effective_to": null,
        "created_at": "2022-12-01T09:00:00Z",
        "created_by": {
          "user_id": "usr-123456789",
          "first_name": "John",
          "last_name": "Doe"
        }
      }
    ]
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 9.2 税率設定作成

**エンドポイント**: `POST /settings/tax-rates`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "rate": 10.00,
  "name": "Reduced Rate",
  "description": "Reduced sales tax rate for specific products",
  "is_default": false,
  "effective_from": "2023-04-01"
}
```

**レスポンス (201 Created)**:
```json
{
  "success": true,
  "data": {
    "tax_rate_id": "tax-new123456",
    "rate": 10.00,
    "name": "Reduced Rate",
    "description": "Reduced sales tax rate for specific products",
    "is_default": false,
    "effective_from": "2023-04-01",
    "effective_to": null,
    "created_at": "2023-01-21T12:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 9.3 支払い条件設定一覧取得

**エンドポイント**: `GET /settings/payment-terms`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "payment_terms": [
      {
        "term_id": "term-123456789",
        "name": "Net 30",
        "description": "Payment due within 30 days",
        "days": 30,
        "is_default": true,
        "created_at": "2022-01-01T09:00:00Z",
        "created_by": {
          "user_id": "usr-123456789",
          "first_name": "John",
          "last_name": "Doe"
        }
      }
    ]
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 9.4 支払い条件設定作成

**エンドポイント**: `POST /settings/payment-terms`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "name": "Net 45",
  "description": "Payment due within 45 days",
  "days": 45,
  "is_default": false
}
```

**レスポンス (201 Created)**:
```json
{
  "success": true,
  "data": {
    "term_id": "term-new123456",
    "name": "Net 45",
    "description": "Payment due within 45 days",
    "days": 45,
    "is_default": false,
    "created_at": "2023-01-21T12:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 9.5 メールテンプレート一覧取得

**エンドポイント**: `GET /settings/email-templates`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "templates": [
      {
        "template_id": "tpl-123456789",
        "name": "Invoice Issued",
        "subject": "Invoice {{invoice_number}} for {{company_name}}",
        "body": "Dear {{contact_name}},\n\nPlease find attached our invoice {{invoice_number}} for {{company_name}}.\n\nTotal Amount: {{total_amount}}\nDue Date: {{due_date}}\n\nThank you for your business!\n\nBest regards,\n{{company_name}}",
        "variables": [
          "invoice_number",
          "company_name",
          "contact_name",
          "total_amount",
          "due_date"
        ],
        "created_at": "2022-01-01T09:00:00Z",
        "created_by": {
          "user_id": "usr-123456789",
          "first_name": "John",
          "last_name": "Doe"
        }
      }
    ]
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 9.6 メールテンプレート作成

**エンドポイント**: `POST /settings/email-templates`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "name": "Quotation Issued",
  "subject": "Quotation {{quotation_number}} for {{company_name}}",
  "body": "Dear {{contact_name}},\n\nPlease find attached our quotation {{quotation_number}} for {{company_name}}.\n\nTotal Amount: {{total_amount}}\nValid Until: {{expiration_date}}\n\nWe look forward to your response.\n\nBest regards,\n{{company_name}}",
  "variables": [
    "quotation_number",
    "company_name",
    "contact_name",
    "total_amount",
    "expiration_date"
  ]
}
```

**レスポンス (201 Created)**:
```json
{
  "success": true,
  "data": {
    "template_id": "tpl-new123456",
    "name": "Quotation Issued",
    "subject": "Quotation {{quotation_number}} for {{company_name}}",
    "body": "Dear {{contact_name}},\n\nPlease find attached our quotation {{quotation_number}} for {{company_name}}.\n\nTotal Amount: {{total_amount}}\nValid Until: {{expiration_date}}\n\nWe look forward to your response.\n\nBest regards,\n{{company_name}}",
    "variables": [
      "quotation_number",
      "company_name",
      "contact_name",
      "total_amount",
      "expiration_date"
    ],
    "created_at": "2023-01-21T12:00:00Z",
    "created_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 9.7 システム設定取得

**エンドポイント**: `GET /settings/system`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "company": {
      "name": "Example Corporation",
      "address": {
        "address_line1": "123 Business Street",
        "address_line2": "Suite 100",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94105",
        "country": "USA"
      },
      "phone": "+1-234-567-8900",
      "email": "contact@example.com",
      "website": "https://example.com",
      "tax_id": "12-3456789"
    },
    "invoice": {
      "prefix": "INV",
      "next_number": 1001,
      "default_payment_terms": "Net 30",
      "default_tax_rate": 8.00,
      "notes": "Thank you for your business!"
    },
    "quotation": {
      "prefix": "QT",
      "next_number": 501,
      "default_expiration_days": 30,
      "default_tax_rate": 8.00,
      "notes": "We look forward to your response."
    },
    "email": {
      "from_name": "Example Corporation",
      "from_email": "invoices@example.com",
      "reply_to": "accounting@example.com",
      "cc": ["accounting@example.com"]
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
```

### 9.8 システム設定更新

**エンドポイント**: `PUT /settings/system`

**ヘッダー**:
```
Authorization: Bearer {jwt_token}
```

**リクエスト**:
```json
{
  "company": {
    "name": "Updated Corporation",
    "address": {
      "address_line1": "456 Business Avenue",
      "address_line2": "Floor 5",
      "city": "San Francisco",
      "state": "CA",
      "zip_code": "94105",
      "country": "USA"
    },
    "phone": "+1-234-567-8901",
    "email": "contact@updated.com",
    "website": "https://updated.com",
    "tax_id": "98-7654321"
  },
  "invoice": {
    "prefix": "INV",
    "next_number": 1001,
    "default_payment_terms": "Net 45",
    "default_tax_rate": 8.00,
    "notes": "Thank you for choosing our services!"
  },
  "quotation": {
    "prefix": "QT",
    "next_number": 501,
    "default_expiration_days": 45,
    "default_tax_rate": 8.00,
    "notes": "We appreciate your interest in our services."
  },
  "email": {
    "from_name": "Updated Corporation",
    "from_email": "invoices@updated.com",
    "reply_to": "accounting@updated.com",
    "cc": ["accounting@updated.com", "sales@updated.com"]
  }
}
```

**レスポンス (200 OK)**:
```json
{
  "success": true,
  "data": {
    "company": {
      "name": "Updated Corporation",
      "address": {
        "address_line1": "456 Business Avenue",
        "address_line2": "Floor 5",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94105",
        "country": "USA"
      },
      "phone": "+1-234-567-8901",
      "email": "contact@updated.com",
      "website": "https://updated.com",
      "tax_id": "98-7654321"
    },
    "invoice": {
      "prefix": "INV",
      "next_number": 1001,
      "default_payment_terms": "Net 45",
      "default_tax_rate": 8.00,
      "notes": "Thank you for choosing our services!"
    },
    "quotation": {
      "prefix": "QT",
      "next_number": 501,
      "default_expiration_days": 45,
      "default_tax_rate": 8.00,
      "notes": "We appreciate your interest in our services."
    },
    "email": {
      "from_name": "Updated Corporation",
      "from_email": "invoices@updated.com",
      "reply_to": "accounting@updated.com",
      "cc": ["accounting@updated.com", "sales@updated.com"]
    },
    "updated_at": "2023-01-21T12:00:00Z",
    "updated_by": {
      "user_id": "usr-123456789",
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "meta": {
    "timestamp": "2023-01-21T12:00:00Z",
    "request_id": "req-123456789"
  }
}
``` 