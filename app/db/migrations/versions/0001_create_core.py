import sqlalchemy as sa
from alembic import op

revision = '0001_create_core'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'skus',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('code', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=64)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )
    op.create_index('ix_skus_code', 'skus', ['code'], unique=True)

    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('lead_time_days', sa.Integer(), nullable=False, server_default='7'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    op.create_table(
        'inventory',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('sku_id', sa.Integer(), sa.ForeignKey('skus.id', ondelete='CASCADE'), nullable=False),
        sa.Column('supplier_id', sa.Integer(), sa.ForeignKey('suppliers.id', ondelete='SET NULL')),
        sa.Column('on_hand', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('reorder_point', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('reorder_qty', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    op.create_index('ix_inventory_sku_id', 'inventory', ['sku_id'])

    op.create_table(
        'purchase_orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('sku_id', sa.Integer(), sa.ForeignKey('skus.id', ondelete='CASCADE'), nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='created'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )
    op.create_index('ix_purchase_orders_sku_id', 'purchase_orders', ['sku_id'])


def downgrade():
    op.drop_index('ix_purchase_orders_sku_id', table_name='purchase_orders')
    op.drop_table('purchase_orders')
    op.drop_index('ix_inventory_sku_id', table_name='inventory')
    op.drop_table('inventory')
    op.drop_table('suppliers')
    op.drop_index('ix_skus_code', table_name='skus')
    op.drop_table('skus')
