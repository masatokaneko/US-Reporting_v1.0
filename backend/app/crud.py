from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from . import models, schemas
from datetime import datetime
import uuid

# User CRUD operations
def get_user(db: Session, user_id: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> List[models.User]:
    query = db.query(models.User)
    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.User, sort_by)))
    else:
        query = query.order_by(asc(getattr(models.User, sort_by)))
    return query.offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        id=str(uuid.uuid4()),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        department=user.department,
        position=user.position,
        phone=user.phone,
        hashed_password=hashed_password,
        is_active=user.is_active,
        create_quote_permission=user.create_quote_permission,
        approve_quote_permission=user.approve_quote_permission,
        manage_order_permission=user.manage_order_permission,
        create_invoice_permission=user.create_invoice_permission,
        approve_invoice_permission=user.approve_invoice_permission,
        manage_revenue_permission=user.manage_revenue_permission,
        admin_permission=user.admin_permission,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(
    db: Session, user_id: str, user: schemas.UserUpdate
) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# Customer CRUD operations
def get_customer(db: Session, customer_id: str) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    status: Optional[str] = None,
) -> List[models.Customer]:
    query = db.query(models.Customer)
    if status:
        query = query.filter(models.Customer.status == status)
    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.Customer, sort_by)))
    else:
        query = query.order_by(asc(getattr(models.Customer, sort_by)))
    return query.offset(skip).limit(limit).all()

def create_customer(
    db: Session, customer: schemas.CustomerCreate, user_id: str
) -> models.Customer:
    db_customer = models.Customer(
        id=str(uuid.uuid4()),
        **customer.dict(),
        created_by=user_id,
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(
    db: Session, customer_id: str, customer: schemas.CustomerUpdate, user_id: str
) -> Optional[models.Customer]:
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None

    update_data = customer.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)
    db_customer.updated_by = user_id

    db.commit()
    db.refresh(db_customer)
    return db_customer

# Product CRUD operations
def get_product(db: Session, product_id: str) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_code(db: Session, product_code: str) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.product_code == product_code).first()

def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    category: Optional[str] = None,
    status: Optional[str] = None,
) -> List[models.Product]:
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category == category)
    if status:
        query = query.filter(models.Product.status == status)
    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.Product, sort_by)))
    else:
        query = query.order_by(asc(getattr(models.Product, sort_by)))
    return query.offset(skip).limit(limit).all()

def create_product(
    db: Session, product: schemas.ProductCreate, user_id: str
) -> models.Product:
    db_product = models.Product(
        id=str(uuid.uuid4()),
        **product.dict(),
        created_by=user_id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(
    db: Session, product_id: str, product: schemas.ProductUpdate, user_id: str
) -> Optional[models.Product]:
    db_product = get_product(db, product_id)
    if not db_product:
        return None

    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    db_product.updated_by = user_id

    db.commit()
    db.refresh(db_product)
    return db_product

# Quotation CRUD operations
def get_quotation(db: Session, quotation_id: str) -> Optional[models.Quotation]:
    return db.query(models.Quotation).filter(models.Quotation.id == quotation_id).first()

def get_quotations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
) -> List[models.Quotation]:
    query = db.query(models.Quotation)
    if status:
        query = query.filter(models.Quotation.status == status)
    if customer_id:
        query = query.filter(models.Quotation.customer_id == customer_id)
    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.Quotation, sort_by)))
    else:
        query = query.order_by(asc(getattr(models.Quotation, sort_by)))
    return query.offset(skip).limit(limit).all()

def create_quotation(
    db: Session, quotation: schemas.QuotationCreate, user_id: str
) -> models.Quotation:
    # Generate quotation number
    quotation_number = generate_quotation_number(db)

    # Calculate totals
    subtotal = sum(item.quantity * item.unit_price for item in quotation.items)
    tax_amount = sum(
        item.quantity * item.unit_price * get_product(db, item.product_id).tax_rate
        for item in quotation.items
    )
    total_amount = subtotal + tax_amount

    # Create quotation
    db_quotation = models.Quotation(
        id=str(uuid.uuid4()),
        quotation_number=quotation_number,
        **quotation.dict(exclude={"items"}),
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        status="draft",
        created_by=user_id,
    )
    db.add(db_quotation)
    db.flush()

    # Create quotation items
    for item in quotation.items:
        product = get_product(db, item.product_id)
        db_item = models.QuotationItem(
            id=str(uuid.uuid4()),
            quotation_id=db_quotation.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.quantity * item.unit_price,
            tax_rate=product.tax_rate,
            tax_amount=item.quantity * item.unit_price * product.tax_rate,
            total_amount=item.quantity * item.unit_price * (1 + product.tax_rate),
            description=item.description,
            sort_order=item.sort_order,
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_quotation)
    return db_quotation

def update_quotation(
    db: Session, quotation_id: str, quotation: schemas.QuotationUpdate, user_id: str
) -> Optional[models.Quotation]:
    db_quotation = get_quotation(db, quotation_id)
    if not db_quotation:
        return None

    # Update quotation fields
    update_data = quotation.dict(exclude={"items"}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_quotation, field, value)
    db_quotation.updated_by = user_id

    # Update items if provided
    if quotation.items is not None:
        # Delete existing items
        db.query(models.QuotationItem).filter(
            models.QuotationItem.quotation_id == quotation_id
        ).delete()

        # Create new items
        for item in quotation.items:
            product = get_product(db, item.product_id)
            db_item = models.QuotationItem(
                id=str(uuid.uuid4()),
                quotation_id=db_quotation.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.quantity * item.unit_price,
                tax_rate=product.tax_rate,
                tax_amount=item.quantity * item.unit_price * product.tax_rate,
                total_amount=item.quantity * item.unit_price * (1 + product.tax_rate),
                description=item.description,
                sort_order=item.sort_order,
            )
            db.add(db_item)

        # Recalculate totals
        subtotal = sum(item.quantity * item.unit_price for item in quotation.items)
        tax_amount = sum(
            item.quantity * item.unit_price * get_product(db, item.product_id).tax_rate
            for item in quotation.items
        )
        total_amount = subtotal + tax_amount

        db_quotation.subtotal = subtotal
        db_quotation.tax_amount = tax_amount
        db_quotation.total_amount = total_amount

    db.commit()
    db.refresh(db_quotation)
    return db_quotation

def request_quotation_approval(
    db: Session, quotation_id: str, approver_id: str, notes: Optional[str] = None
) -> Optional[models.Quotation]:
    db_quotation = get_quotation(db, quotation_id)
    if not db_quotation:
        return None

    db_quotation.status = "pending_approval"
    db_quotation.approver_id = approver_id
    if notes:
        db_quotation.notes = notes

    db.commit()
    db.refresh(db_quotation)
    return db_quotation

def approve_quotation(
    db: Session, quotation_id: str, approver_id: str, notes: Optional[str] = None
) -> Optional[models.Quotation]:
    db_quotation = get_quotation(db, quotation_id)
    if not db_quotation or db_quotation.status != "pending_approval":
        return None

    db_quotation.status = "approved"
    db_quotation.approver_id = approver_id
    db_quotation.approved_at = datetime.utcnow()
    if notes:
        db_quotation.notes = notes

    db.commit()
    db.refresh(db_quotation)
    return db_quotation

# Invoice CRUD operations
def get_invoice(db: Session, invoice_id: str) -> Optional[models.Invoice]:
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

def get_invoices(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
) -> List[models.Invoice]:
    query = db.query(models.Invoice)
    if status:
        query = query.filter(models.Invoice.status == status)
    if customer_id:
        query = query.filter(models.Invoice.customer_id == customer_id)
    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.Invoice, sort_by)))
    else:
        query = query.order_by(asc(getattr(models.Invoice, sort_by)))
    return query.offset(skip).limit(limit).all()

def create_invoice(
    db: Session, invoice: schemas.InvoiceCreate, user_id: str
) -> models.Invoice:
    # Generate invoice number
    invoice_number = generate_invoice_number(db)

    # Calculate totals
    subtotal = sum(item.quantity * item.unit_price for item in invoice.items)
    tax_amount = sum(
        item.quantity * item.unit_price * get_product(db, item.product_id).tax_rate
        for item in invoice.items
    )
    total_amount = subtotal + tax_amount

    # Create invoice
    db_invoice = models.Invoice(
        id=str(uuid.uuid4()),
        invoice_number=invoice_number,
        **invoice.dict(exclude={"items"}),
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        status="draft",
        payment_status="unpaid",
        created_by=user_id,
    )
    db.add(db_invoice)
    db.flush()

    # Create invoice items
    for item in invoice.items:
        product = get_product(db, item.product_id)
        db_item = models.InvoiceItem(
            id=str(uuid.uuid4()),
            invoice_id=db_invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.quantity * item.unit_price,
            tax_rate=product.tax_rate,
            tax_amount=item.quantity * item.unit_price * product.tax_rate,
            total_amount=item.quantity * item.unit_price * (1 + product.tax_rate),
            description=item.description,
            sort_order=item.sort_order,
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def update_invoice(
    db: Session, invoice_id: str, invoice: schemas.InvoiceUpdate, user_id: str
) -> Optional[models.Invoice]:
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return None

    # Update invoice fields
    update_data = invoice.dict(exclude={"items"}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_invoice, field, value)
    db_invoice.updated_by = user_id

    # Update items if provided
    if invoice.items is not None:
        # Delete existing items
        db.query(models.InvoiceItem).filter(
            models.InvoiceItem.invoice_id == invoice_id
        ).delete()

        # Create new items
        for item in invoice.items:
            product = get_product(db, item.product_id)
            db_item = models.InvoiceItem(
                id=str(uuid.uuid4()),
                invoice_id=db_invoice.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.quantity * item.unit_price,
                tax_rate=product.tax_rate,
                tax_amount=item.quantity * item.unit_price * product.tax_rate,
                total_amount=item.quantity * item.unit_price * (1 + product.tax_rate),
                description=item.description,
                sort_order=item.sort_order,
            )
            db.add(db_item)

        # Recalculate totals
        subtotal = sum(item.quantity * item.unit_price for item in invoice.items)
        tax_amount = sum(
            item.quantity * item.unit_price * get_product(db, item.product_id).tax_rate
            for item in invoice.items
        )
        total_amount = subtotal + tax_amount

        db_invoice.subtotal = subtotal
        db_invoice.tax_amount = tax_amount
        db_invoice.total_amount = total_amount

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def request_invoice_approval(
    db: Session, invoice_id: str, approver_id: str, notes: Optional[str] = None
) -> Optional[models.Invoice]:
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return None

    db_invoice.status = "pending_approval"
    db_invoice.approver_id = approver_id
    if notes:
        db_invoice.notes = notes

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def approve_invoice(
    db: Session, invoice_id: str, approver_id: str, notes: Optional[str] = None
) -> Optional[models.Invoice]:
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice or db_invoice.status != "pending_approval":
        return None

    db_invoice.status = "approved"
    db_invoice.approver_id = approver_id
    db_invoice.approved_at = datetime.utcnow()
    if notes:
        db_invoice.notes = notes

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def issue_invoice(
    db: Session, invoice_id: str, user_id: str, notes: Optional[str] = None
) -> Optional[models.Invoice]:
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice or db_invoice.status != "approved":
        return None

    db_invoice.status = "issued"
    if notes:
        db_invoice.notes = notes

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def register_payment(
    db: Session, invoice_id: str, payment: schemas.PaymentCreate, user_id: str
) -> Optional[models.Payment]:
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return None

    # Create payment
    db_payment = models.Payment(
        id=str(uuid.uuid4()),
        invoice_id=invoice_id,
        **payment.dict(),
        payment_status="completed",
        created_by=user_id,
    )
    db.add(db_payment)

    # Update invoice payment status
    total_paid = sum(p.payment_amount for p in db_invoice.payments) + payment.payment_amount
    if total_paid >= db_invoice.total_amount:
        db_invoice.payment_status = "paid"
    else:
        db_invoice.payment_status = "partially_paid"

    db.commit()
    db.refresh(db_payment)
    return db_payment

# Tax Rate CRUD operations
def get_tax_rate(db: Session, tax_rate_id: str) -> Optional[models.TaxRate]:
    return db.query(models.TaxRate).filter(models.TaxRate.id == tax_rate_id).first()

def get_tax_rates(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> List[models.TaxRate]:
    query = db.query(models.TaxRate)
    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.TaxRate, sort_by)))
    else:
        query = query.order_by(asc(getattr(models.TaxRate, sort_by)))
    return query.offset(skip).limit(limit).all()

def create_tax_rate(
    db: Session, tax_rate: schemas.TaxRateCreate, user_id: str
) -> models.TaxRate:
    db_tax_rate = models.TaxRate(
        id=str(uuid.uuid4()),
        **tax_rate.dict(),
        created_by=user_id,
    )
    db.add(db_tax_rate)
    db.commit()
    db.refresh(db_tax_rate)
    return db_tax_rate

def update_tax_rate(
    db: Session, tax_rate_id: str, tax_rate: schemas.TaxRateUpdate
) -> Optional[models.TaxRate]:
    db_tax_rate = get_tax_rate(db, tax_rate_id)
    if not db_tax_rate:
        return None

    update_data = tax_rate.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tax_rate, field, value)

    db.commit()
    db.refresh(db_tax_rate)
    return db_tax_rate

# Payment Term CRUD operations
def get_payment_term(db: Session, payment_term_id: str) -> Optional[models.PaymentTerm]:
    return db.query(models.PaymentTerm).filter(models.PaymentTerm.id == payment_term_id).first()

def get_payment_terms(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> List[models.PaymentTerm]:
    query = db.query(models.PaymentTerm)
    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.PaymentTerm, sort_by)))
    else:
        query = query.order_by(asc(getattr(models.PaymentTerm, sort_by)))
    return query.offset(skip).limit(limit).all()

def create_payment_term(
    db: Session, payment_term: schemas.PaymentTermCreate, user_id: str
) -> models.PaymentTerm:
    db_payment_term = models.PaymentTerm(
        id=str(uuid.uuid4()),
        **payment_term.dict(),
        created_by=user_id,
    )
    db.add(db_payment_term)
    db.commit()
    db.refresh(db_payment_term)
    return db_payment_term

def update_payment_term(
    db: Session, payment_term_id: str, payment_term: schemas.PaymentTermUpdate
) -> Optional[models.PaymentTerm]:
    db_payment_term = get_payment_term(db, payment_term_id)
    if not db_payment_term:
        return None

    update_data = payment_term.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_payment_term, field, value)

    db.commit()
    db.refresh(db_payment_term)
    return db_payment_term

# Email Template CRUD operations
def get_email_template(db: Session, template_id: str) -> Optional[models.EmailTemplate]:
    return db.query(models.EmailTemplate).filter(models.EmailTemplate.id == template_id).first()

def get_email_templates(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> List[models.EmailTemplate]:
    query = db.query(models.EmailTemplate)
    if sort_order == "desc":
        query = query.order_by(desc(getattr(models.EmailTemplate, sort_by)))
    else:
        query = query.order_by(asc(getattr(models.EmailTemplate, sort_by)))
    return query.offset(skip).limit(limit).all()

def create_email_template(
    db: Session, template: schemas.EmailTemplateCreate, user_id: str
) -> models.EmailTemplate:
    db_template = models.EmailTemplate(
        id=str(uuid.uuid4()),
        **template.dict(),
        created_by=user_id,
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def update_email_template(
    db: Session, template_id: str, template: schemas.EmailTemplateUpdate
) -> Optional[models.EmailTemplate]:
    db_template = get_email_template(db, template_id)
    if not db_template:
        return None

    update_data = template.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_template, field, value)

    db.commit()
    db.refresh(db_template)
    return db_template

# System Setting CRUD operations
def get_system_setting(db: Session) -> Optional[models.SystemSetting]:
    return db.query(models.SystemSetting).first()

def create_system_setting(
    db: Session, setting: schemas.SystemSettingCreate, user_id: str
) -> models.SystemSetting:
    db_setting = models.SystemSetting(
        id=str(uuid.uuid4()),
        **setting.dict(),
        updated_by=user_id,
    )
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

def update_system_setting(
    db: Session, setting: schemas.SystemSettingUpdate, user_id: str
) -> Optional[models.SystemSetting]:
    db_setting = get_system_setting(db)
    if not db_setting:
        return None

    update_data = setting.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_setting, field, value)
    db_setting.updated_by = user_id

    db.commit()
    db.refresh(db_setting)
    return db_setting

# Helper functions
def generate_quotation_number(db: Session) -> str:
    # Get the latest quotation number
    latest_quotation = (
        db.query(models.Quotation)
        .order_by(desc(models.Quotation.created_at))
        .first()
    )

    if not latest_quotation:
        # If no quotations exist, start with Q-0001
        return "Q-0001"

    # Extract the number from the latest quotation number
    try:
        number = int(latest_quotation.quotation_number.split("-")[1])
        return f"Q-{number + 1:04d}"
    except (IndexError, ValueError):
        # If the format is invalid, start with Q-0001
        return "Q-0001"

def generate_invoice_number(db: Session) -> str:
    # Get the latest invoice number
    latest_invoice = (
        db.query(models.Invoice)
        .order_by(desc(models.Invoice.created_at))
        .first()
    )

    if not latest_invoice:
        # If no invoices exist, start with INV-0001
        return "INV-0001"

    # Extract the number from the latest invoice number
    try:
        number = int(latest_invoice.invoice_number.split("-")[1])
        return f"INV-{number + 1:04d}"
    except (IndexError, ValueError):
        # If the format is invalid, start with INV-0001
        return "INV-0001" 