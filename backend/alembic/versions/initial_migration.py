"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-03-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # ユーザーテーブル
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('admin_permission', sa.Boolean(), nullable=False, default=False),
        sa.Column('create_quote_permission', sa.Boolean(), nullable=False, default=False),
        sa.Column('approve_quote_permission', sa.Boolean(), nullable=False, default=False),
        sa.Column('create_invoice_permission', sa.Boolean(), nullable=False, default=False),
        sa.Column('approve_invoice_permission', sa.Boolean(), nullable=False, default=False),
        sa.Column('manage_revenue_permission', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # 顧客テーブル
    op.create_table(
        'customers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('contact_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 商品テーブル
    op.create_table(
        'products',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('product_code', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('product_code')
    )

    # 見積書テーブル
    op.create_table(
        'quotations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('quotation_number', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=False),
        sa.Column('issue_date', sa.Date(), nullable=False),
        sa.Column('expiry_date', sa.Date(), nullable=False),
        sa.Column('subtotal', sa.Float(), nullable=False),
        sa.Column('tax_amount', sa.Float(), nullable=False),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, default='draft'),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('approved_by', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('quotation_number')
    )

    # 見積書明細テーブル
    op.create_table(
        'quotation_items',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('quotation_id', sa.String(), nullable=False),
        sa.Column('product_id', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['quotation_id'], ['quotations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 請求書テーブル
    op.create_table(
        'invoices',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('invoice_number', sa.String(), nullable=False),
        sa.Column('quotation_id', sa.String(), nullable=True),
        sa.Column('customer_id', sa.String(), nullable=False),
        sa.Column('issue_date', sa.Date(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('subtotal', sa.Float(), nullable=False),
        sa.Column('tax_amount', sa.Float(), nullable=False),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, default='draft'),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('approved_by', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['quotation_id'], ['quotations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('invoice_number')
    )

    # 請求書明細テーブル
    op.create_table(
        'invoice_items',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('invoice_id', sa.String(), nullable=False),
        sa.Column('product_id', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 支払いテーブル
    op.create_table(
        'payments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('invoice_id', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('payment_date', sa.Date(), nullable=False),
        sa.Column('payment_method', sa.String(), nullable=False),
        sa.Column('reference_number', sa.String(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 税率テーブル
    op.create_table(
        'tax_rates',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('rate', sa.Float(), nullable=False),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 支払い条件テーブル
    op.create_table(
        'payment_terms',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('days', sa.Integer(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # メールテンプレートテーブル
    op.create_table(
        'email_templates',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('subject', sa.String(), nullable=False),
        sa.Column('body', sa.String(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # システム設定テーブル
    op.create_table(
        'system_settings',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('company_address', sa.String(), nullable=True),
        sa.Column('company_phone', sa.String(), nullable=True),
        sa.Column('company_email', sa.String(), nullable=True),
        sa.Column('default_tax_rate', sa.Float(), nullable=False),
        sa.Column('default_payment_term_id', sa.String(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['default_payment_term_id'], ['payment_terms.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('system_settings')
    op.drop_table('email_templates')
    op.drop_table('payment_terms')
    op.drop_table('tax_rates')
    op.drop_table('payments')
    op.drop_table('invoice_items')
    op.drop_table('invoices')
    op.drop_table('quotation_items')
    op.drop_table('quotations')
    op.drop_table('products')
    op.drop_table('customers')
    op.drop_table('users') 