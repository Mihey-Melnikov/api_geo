"""Create db

Revision ID: 82029799a389
Revises: 
Create Date: 2024-05-10 20:15:28.942390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82029799a389'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('iso3116_alpha2', sa.String(length=2), nullable=False),
    sa.Column('iso3166_alpha3', sa.String(length=3), nullable=False),
    sa.Column('phone_code', sa.String(), nullable=True),
    sa.Column('phone_mask', sa.String(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('osm_id', sa.String(), nullable=False),
    sa.Column('osm_type', sa.String(length=1), nullable=False),
    sa.Column('last_updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('need_automatic_update', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('osm_id')
    )
    op.create_index(op.f('ix_country_id'), 'country', ['id'], unique=False)
    op.create_table('language',
    sa.Column('language_iso639', sa.String(length=2), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('language_iso639')
    )
    op.create_index(op.f('ix_language_language_iso639'), 'language', ['language_iso639'], unique=False)
    op.create_table('translate',
    sa.Column('entity', sa.String(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=False),
    sa.Column('translate', sa.String(), nullable=False),
    sa.Column('last_updated_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('entity', 'entity_id', 'language')
    )
    op.create_index(op.f('ix_translate_entity_id'), 'translate', ['entity_id'], unique=False)
    op.create_index(op.f('ix_translate_language'), 'translate', ['language'], unique=False)
    op.create_index(op.f('ix_translate_translate'), 'translate', ['translate'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('osm_id', sa.String(), nullable=False),
    sa.Column('osm_type', sa.String(length=1), nullable=False),
    sa.Column('last_updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('need_automatic_update', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('osm_id')
    )
    op.create_index(op.f('ix_region_id'), 'region', ['id'], unique=False)
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('iata', sa.String(length=3), nullable=True),
    sa.Column('timezone', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('osm_id', sa.String(), nullable=False),
    sa.Column('osm_type', sa.String(length=1), nullable=False),
    sa.Column('last_updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('need_automatic_update', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('osm_id')
    )
    op.create_index(op.f('ix_city_iata'), 'city', ['iata'], unique=False)
    op.create_index(op.f('ix_city_id'), 'city', ['id'], unique=False)
    op.create_table('airport',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('iata_en', sa.String(length=3), nullable=True),
    sa.Column('iata_ru', sa.String(length=3), nullable=True),
    sa.Column('timezone', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('osm_id', sa.String(), nullable=False),
    sa.Column('osm_type', sa.String(length=1), nullable=False),
    sa.Column('last_updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('need_automatic_update', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('osm_id')
    )
    op.create_index(op.f('ix_airport_iata_en'), 'airport', ['iata_en'], unique=False)
    op.create_index(op.f('ix_airport_iata_ru'), 'airport', ['iata_ru'], unique=False)
    op.create_index(op.f('ix_airport_id'), 'airport', ['id'], unique=False)
    op.create_table('railway',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('express3_code', sa.String(), nullable=False),
    sa.Column('is_main', sa.Boolean(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('timezone', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('osm_id', sa.String(), nullable=False),
    sa.Column('osm_type', sa.String(length=1), nullable=False),
    sa.Column('last_updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('need_automatic_update', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('osm_id')
    )
    op.create_index(op.f('ix_railway_express3_code'), 'railway', ['express3_code'], unique=False)
    op.create_index(op.f('ix_railway_id'), 'railway', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_railway_id'), table_name='railway')
    op.drop_index(op.f('ix_railway_express3_code'), table_name='railway')
    op.drop_table('railway')
    op.drop_index(op.f('ix_airport_id'), table_name='airport')
    op.drop_index(op.f('ix_airport_iata_ru'), table_name='airport')
    op.drop_index(op.f('ix_airport_iata_en'), table_name='airport')
    op.drop_table('airport')
    op.drop_index(op.f('ix_city_id'), table_name='city')
    op.drop_index(op.f('ix_city_iata'), table_name='city')
    op.drop_table('city')
    op.drop_index(op.f('ix_region_id'), table_name='region')
    op.drop_table('region')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_translate_translate'), table_name='translate')
    op.drop_index(op.f('ix_translate_language'), table_name='translate')
    op.drop_index(op.f('ix_translate_entity_id'), table_name='translate')
    op.drop_table('translate')
    op.drop_index(op.f('ix_language_language_iso639'), table_name='language')
    op.drop_table('language')
    op.drop_index(op.f('ix_country_id'), table_name='country')
    op.drop_table('country')
    # ### end Alembic commands ###
