from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import MetaData, Table, Column, String, Integer, BigInteger, DateTime
from datetime import datetime
import os
import time

import randkanjiname

metadata = MetaData()

bbs = Table(
    'bbs', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('uid', Integer),
    Column('date', DateTime),
    Column('comment', String),
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('uid', BigInteger, unique=True),
    Column('name', String(16), unique=True),
)


engine = create_engine(os.getenv("DBURI", "sqlite://"), echo=True)
conn = engine.connect()
metadata.create_all(engine)


def init_tables():
    init_bbs_table()
    init_users_table()


def init_bbs_table():
    bbs.drop(engine, checkfirst=True)
    bbs.create(engine)


def init_users_table():
    users.drop(engine, checkfirst=True)
    users.create(engine)
    values = [{'name': nid} for nid in randkanjiname.get_shuffled_names()]
    query = users.insert()
    conn.execute(query, values)


class UserNotFoundError(Exception):
    pass

def save_comment(uid, comment):
    if type(uid) is not int:
        raise UserNotFoundError('Uid\'s type is not int.')
    user = get_user_by_uid(uid)
    if not user:
        raise UserNotFoundError('User does not exists.')
    query = bbs.insert().values(uid=uid, date=datetime.now(), comment=comment)
    conn.execute(query)
    return


def get_comments():
    query = select([users.c.name, bbs.c.comment, bbs.c.date]
                   ).where(bbs.c.uid == users.c.uid)
    result = conn.execute(query)
    return result


def get_user_by_uid(uid):
    query = select([users.c.id, users.c.uid, users.c.name]) \
        .where(users.c.uid == uid)
    result = conn.execute(query)
    return result.fetchone()


def create_new_user():
    # 未使用のUserを探す
    query = select([users.c.id, users.c.uid, users.c.name]) \
        .where(users.c.uid == None) \
        .order_by(users.c.id) \
        .limit(1)
    result = conn.execute(query).fetchone()
    unused_utbid = result[users.c.id]

    # uidを生成
    uid = hash(time.time())

    # uidを設定
    query = users.update() \
        .values(uid=uid) \
        .where(users.c.id == unused_utbid)
    conn.execute(query)

    return uid
