import sqlalchemy
from models.models import *
import time as t


def create(lists, table):
    t0 = t.time()

    try:
        conn = engine.connect()
        table = sqlalchemy.Table(table, Base.metadata, autoreload=True)
        conn.execute(table.insert(), lists)
        print(f"all {table} saved, it took  %8.8f seconds" % (t.time() - t0))

    except:
        print(f'Error during {table} insert ')

    finally:
        db_session.commit()
        db_session.close()


def add_population_column(table):
    t0 = t.time()

    try:
        conn = engine.connect()
        table = sqlalchemy.Table(table, Base.metadata, autoreload=True)
        conn.execute('alter table departement add column population int8')
        print(f"alter table {table} saved, it took  %8.8f seconds" % (t.time() - t0))

    except:
        print(f'Error during {table} alter ')

    finally:
        db_session.commit()
        db_session.close()

def insert_population(table,list):

    t0 = t.time()

    try:
        conn = engine.connect()
        table = sqlalchemy.Table(table, Base.metadata, autoreload=True)
        conn.execute('update departement set population =%s where name =%s',(list['Total'], list['Departement']))
        print(f"alter table {table} saved, it took  %8.8f seconds" % (t.time() - t0))

    except:
        print(f'Error during {table} alter ')

    finally:
        db_session.commit()
        db_session.close()

def add_population_column_Region(table):
    t0 = t.time()

    try:
        conn = engine.connect()
        table = sqlalchemy.Table(table, Base.metadata, autoreload=True)
        conn.execute('alter table region add column population int8')
        print(f"alter table {table} saved, it took  %8.8f seconds" % (t.time() - t0))

    except:
        print(f'Error during {table} alter ')

    finally:
        db_session.commit()
        db_session.close()


def insert_region_population(table,list):

    t0 = t.time()

    try:
        conn = engine.connect()
        table = sqlalchemy.Table(table, Base.metadata, autoreload=True)
        conn.execute('update region set population =%s where name =%s',(list['Total'], list['Region']))
        print(f"alter table {table} saved, it took  %8.8f seconds" % (t.time() - t0))

    except:
        print(f'Error during {table} alter ')

    finally:
        db_session.commit()
        db_session.close()
