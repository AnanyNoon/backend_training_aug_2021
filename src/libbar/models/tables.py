from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, types
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import UniqueConstraint, Index
import sqlalchemy as sa

import libbar


def create_all():
    Base.metadata.create_all(libbar.engine)


def recreate_all():
    import os
    assert os.getenv('ENV') == 'dev', 'must be dev'
    assert libbar.engine.url.username == 'root'
    assert libbar.engine.url.password == 'root'
    Base.metadata.drop_all(libbar.engine)
    Base.metadata.create_all(libbar.engine)


Base = declarative_base()


class Model(Base):
    __abstract__ = True
    __bind_key__ = 'bar'


TINYINT = mysql.TINYINT(unsigned=True)
SMALLINT = mysql.SMALLINT(unsigned=True)
MEDIUMINT = mysql.MEDIUMINT(unsigned=True)
INT = mysql.INTEGER(unsigned=True)
BIGINT = mysql.BIGINT(unsigned=True)
SINT = mysql.INTEGER(unsigned=False)
SBIGINT = mysql.BIGINT(unsigned=False)
CCY = sa.Numeric(13, 2)


class Pastebin(Model):
    __tablename__ = 'pastebin'
    id_pastebin = sa.Column(sa.Integer, primary_key=True)
    code = sa.Column(sa.String(50), nullable=False, unique=True)
    txt = sa.Column(sa.String(1000), nullable=False)
    created_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                        nullable=False)


