from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey
    )

from sqlalchemy.orm import relationship

from sqlalchemy.types import (
    Boolean,
    DateTime,
    Enum,
    Integer,
    Unicode
    )

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StateEnum:
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    PENDING = 'PENDING'

    enum = (SUCCESS, FAILURE, PENDING)


class Environment(Base):
    __tablename__ = 'environment'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    busy = Column(Boolean, default=False)


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    requester = Column(Unicode)
    files = Column(Unicode, nullable=False)
    output = Column(Unicode)
    created = Column(DateTime, default=datetime.utcnow)
    state = Column(Enum(*StateEnum.enum), default=StateEnum.PENDING)
    environment_id = Column(Integer, ForeignKey('environment.id'),
                            nullable=False)

    environment = relationship('Environment', backref='request')
