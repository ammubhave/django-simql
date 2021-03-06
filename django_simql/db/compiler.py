import datetime
import sys

from .low_level import SimqlLowLevelQuery
from .utils import SimqlDatabaseError
from django.db.utils import DatabaseError, IntegrityError

from functools import wraps

from djangotoolbox.db.basecompiler import NonrelQuery, NonrelCompiler, \
    NonrelInsertCompiler, NonrelUpdateCompiler, NonrelDeleteCompiler

# TODO: Change this to match your DB
# Valid query types (a dictionary is used for speedy lookups).
OPERATORS_MAP = {
    'exact': '=',
    'gt': '>',
    'gte': '>=',
    'lt': '<',
    'lte': '<=',
    'in': 'IN',
    'isnull': lambda lookup_type, value: ('=' if value else '!=', None),

    #'startswith': lambda lookup_type, value: ...,
    #'range': lambda lookup_type, value: ...,
    #'year': lambda lookup_type, value: ...,
}

NEGATION_MAP = {
    'exact': '!=',
    'gt': '<=',
    'gte': '<',
    'lt': '>=',
    'lte': '>',
    'in': 'NOTIN',
    'isnull': lambda lookup_type, value: ('!=' if value else '=', None),

    #'startswith': lambda lookup_type, value: ...,
    #'range': lambda lookup_type, value: ...,
    #'year': lambda lookup_type, value: ...,
}


def safe_call(func):
    @wraps(func)
    def _func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # TODO: Replace this with your DB error class
        except SimqlDatabaseError, e:
            raise DatabaseError, DatabaseError(*tuple(e)), sys.exc_info()[2]
    return _func


class SimqlBackendQuery(NonrelQuery):
    def __init__(self, compiler, fields):
        super(SimqlBackendQuery, self).__init__(compiler, fields)
        # TODO: add your initialization code here
        self.db_query = SimqlLowLevelQuery(self.connection.db_connection)

    # This is needed for debugging
    def __repr__(self):
        # TODO: add some meaningful query string for debugging
        return '<SimqlBackendQuery: ...>'

    @safe_call
    def fetch(self):
        # TODO: run your low-level query here
        low_mark, high_mark = self.limits
        if high_mark is None:
            # Infinite fetching
            results = self.db_query.fetch_infinite(offset=low_mark)
        elif high_mark > low_mark:
            # Range fetching
            results = self.db_query.fetch_range(high_mark - low_mark, low_mark)
        else:
            results = ()

        for entity in results:
            entity[self.query.get_meta().pk.column] = entity['_id']
            del entity['_id']
            yield entity

    @safe_call
    def count(self, limit=None):
        # TODO: implement this
        return self.db_query.count(limit)

    @safe_call
    def delete(self):
        # TODO: implement this
        self.db_query.delete()

    @safe_call
    def order_by(self, ordering):
        # TODO: implement this
        for order in ordering:
            if order.startswith('-'):
                column, direction = order[1:], 'DESC'
            else:
                column, direction = order, 'ASC'
            if column == self.query.get_meta().pk.column:
                column = '_id'
            self.db_query.add_ordering(column, direction)

    # This function is used by the default add_filters() implementation which
    # only supports ANDed filter rules and simple negation handling for
    # transforming OR filters to AND filters:
    # NOT (a OR b) => (NOT a) AND (NOT b)
    @safe_call
    def add_filter(self, column, lookup_type, negated, db_type, value):
        # TODO: implement this or the add_filters() function (see the base
        # class for a sample implementation)

        # Emulated/converted lookups
        if column == self.query.get_meta().pk.column:
            column = '_id'

        if negated:
            try:
                op = NEGATION_MAP[lookup_type]
            except KeyError:
                raise DatabaseError("Lookup type %r can't be negated" % lookup_type)
        else:
            try:
                op = OPERATORS_MAP[lookup_type]
            except KeyError:
                raise DatabaseError("Lookup type %r isn't supported" % lookup_type)

        # Handle special-case lookup types
        if callable(op):
            op, value = op(lookup_type, value)

        db_value = self.convert_value_for_db(db_type, value)
        self.db_query.filter(column, op, db_value)


class SQLCompiler(NonrelCompiler):
    query_class = SimqlBackendQuery


class SQLInsertCompiler(NonrelInsertCompiler, SQLCompiler):
    @safe_call
    def insert(self, data, return_id=False):
        # TODO: implement this
        pk_column = self.query.get_meta().pk.column
        if pk_column in data:
            data['_id'] = data[pk_column]
            del data[pk_column]

        pk = save_entity(self.connection.db_connection,
            self.query.get_meta().db_table, data)
        return pk


class SQLUpdateCompiler(NonrelUpdateCompiler, SQLCompiler):
    pass


class SQLDeleteCompiler(NonrelDeleteCompiler, SQLCompiler):
    pass
