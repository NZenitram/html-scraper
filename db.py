import mysql.connector
from contextlib import contextmanager

@contextmanager
def cursor(conn,
           buffered=None,
           raw=None,
           prepared=None,
           cursor_class=None,
           dictionary=None,
           named_tuple=None):
    cur = None
    try:
        cur = conn.cursor(buffered, raw=raw, prepared=prepared, cursor_class=cursor_class, dictionary=dictionary,
                          named_tuple=named_tuple)
        yield cur
    finally:
        if cur:
            cur.close()

@contextmanager
def connection(*args, **kwargs):
    conn = None
    try:
        conn = mysql.connector.connect(*args, **kwargs)
        yield conn
    finally:
        if conn:
            conn.close()