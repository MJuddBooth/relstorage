# -*- coding: utf-8 -*-
"""
Compatibility shims.

"""

from __future__ import print_function, absolute_import, division

# pylint:disable=unused-import

import sys
PY3 = sys.version_info[0] == 3

# Dict support

if PY3:
    def list_keys(d):
        return list(d.keys())
    def list_items(d):
        return list(d.items())
    def list_values(d):
        return list(d.values())
    iteritems = dict.items
    iterkeys = dict.keys
else:
    list_keys = dict.keys
    list_items = dict.items
    list_values = dict.values
    iteritems = dict.iteritems
    iterkeys = dict.iterkeys

# Types

if PY3:
    string_types = (str,)
    unicode = str
else:
    string_types = (basestring,)
    unicode = unicode


# Functions
if PY3:
    xrange = range
    intern = sys.intern
    from base64 import encodebytes as base64_encodebytes
    from base64 import decodebytes as base64_decodebytes
else:
    xrange = xrange
    intern = intern
    from base64 import encodestring as base64_encodebytes
    from base64 import decodestring as base64_decodebytes

# Database types

if PY3:
    # psycopg2 is smart enough to return memoryview or
    # buffer on Py3/Py2, respectively, for bytea columns
    _db_binary_types = (memoryview,)
    def bytes_to_pg_binary(data):
        # bytes under Py3 is perfectly acceptable
        return data
else:
    _db_binary_types = (memoryview, buffer)
    # bytes is str under py2, so must be memoryview
    # There is a psycopg2.Binary type that should do basically the same thing
    # XXX: Use the driver layer for this. Binary is a standard field!
    try:
        from psycopg2 import Binary as _psyBinary
    except ImportError:
        # On PyPy and/or with psycopg2cffi up through at least
        # 2.6, we must use buffer, not memoryview. otherwise the string
        # representation of the wrong thing gets passed to the DB.
        bytes_to_pg_binary = buffer
    else:
        bytes_to_pg_binary = _psyBinary

def db_binary_to_bytes(data):
    if isinstance(data, _db_binary_types):
        data = bytes(data)
    return data


# mysqlclient, a binary driver that works for Py2, Py3 and
# PyPy (claimed), uses a connection that is a weakref. MySQLdb
# and PyMySQL use a hard reference
from weakref import ref as _wref
def mysql_connection(cursor):
    conn = cursor.connection
    if isinstance(conn, _wref):
        conn = conn()
    return conn



from ZODB._compat import BytesIO
StringIO = BytesIO

# XXX: This is a private module in ZODB, but it has a lot
# of knowledge about how to choose the right implementation
# based on Python version and implementation. We at least
# centralize the import from here.
from ZODB._compat import dumps, loads
