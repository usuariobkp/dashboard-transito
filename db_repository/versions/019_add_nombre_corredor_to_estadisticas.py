from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    estadisticas = Table('estadisticas', meta, autoload=True)
    tipo_grafico = Column('nombre_corredor', String(77), nullable=True)
    tipo_grafico.create(estadisticas)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    estadisticas = Table('estadisticas', meta, autoload=True)
    estadisticas.c.nombre_corredor.drop()