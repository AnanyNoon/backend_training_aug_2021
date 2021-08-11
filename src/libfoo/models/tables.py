from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, types
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import UniqueConstraint, Index
import sqlalchemy as sa

import libfoo


def create_all():
    Base.metadata.create_all(libfoo.engine)


def recreate_all():
    import os
    assert os.getenv('ENV') == 'dev', 'must be dev'
    assert libfoo.engine.url.username == 'root'
    assert libfoo.engine.url.password == 'root'
    Base.metadata.drop_all(libfoo.engine)
    Base.metadata.create_all(libfoo.engine)


Base = declarative_base()


class Model(Base):
    __abstract__ = True
    __bind_key__ = 'foo'


TINYINT = mysql.TINYINT(unsigned=True)
SMALLINT = mysql.SMALLINT(unsigned=True)
MEDIUMINT = mysql.MEDIUMINT(unsigned=True)
INT = mysql.INTEGER(unsigned=True)
BIGINT = mysql.BIGINT(unsigned=True)
SINT = mysql.INTEGER(unsigned=False)
SBIGINT = mysql.BIGINT(unsigned=False)
CCY = sa.Numeric(13, 2)



class KeyVal(Model):
    __tablename__ = 'key_val'
    id_key_val = sa.Column(sa.Integer, primary_key=True)
    ns = sa.Column(sa.String(30), nullable=False)
    k = sa.Column(sa.String(30), nullable=False)
    v = sa.Column(sa.String(30), nullable=False)
    created_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                        nullable=False)

    __table_args__ = (
        UniqueConstraint('ns', 'k', name='uq_k'),
        Index('ix_value', 'v', 'ns'),
    )


