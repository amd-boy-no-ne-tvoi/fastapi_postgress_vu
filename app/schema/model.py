from ctypes.wintypes import tagSIZE
import datetime
from email.policy import default
from sqlalchemy import Boolean, Column, String, Enum, DateTime, Integer, PickleType
from sqlalchemy.orm import relationships
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import ARRAY
import enum
from app.schema.engine import Base
from app.schema.model import *
from app.utils.user_utils import * 


# роли пользователей админ, выполнитель, дилер
class Role(enum.Enum):
    admin = 0
    contractor = 1
    dealer = 2


# приоритет: Обычная, Высокий, Критический;
class Priority(enum.Enum):
    normal = 0
    high = 1
    critical = 2


# Статус – Открыта, в работе, закрыта предварительно, закрыта;
class Status(enum.Enum):
    open = 0
    in_work = 1
    pre_closed = 2
    closed = 2


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key = True)
    email = Column(String(50))
    hashedPassword = Column(String(255))
    secret = Column(String(25))
    phone = Column(String(15))
    role = Column(Enum(Role))


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer(), primary_key = True)
    theme = Column(String(255))
    title = Column(String(255))
    text = Column(String())
    priority = Column(Enum(Priority))
    status = Column(Enum(Status))
    dealer_id = Column(Integer())
    contractor_id = Column(Integer(), default=None)

    date_of_closing = Column(DateTime, default=None)

    date_of_submission = Column(DateTime, default=datetime.datetime.utcnow)
    tags = Column(ARRAY(String(255)))
    files = Column(ARRAY(String(255)))

    store_name = Column(String(255))
    phone_number = Column(String(15))
