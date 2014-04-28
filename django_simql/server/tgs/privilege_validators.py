def check_strong_read_on_columns(table, columns, permissions):
    columns = columns[:]
    column_restrictions = {}
    for perm in permissions:
        perm_table = perm[0].split('.')[0]
        perm_column = perm[0].split('.')[1]
        perm_scope = perm[1]
        perm_selects = perm[2]
        if perm_table == table.__name__ and perm_column in columns and perm_scope == 'R':
            if perm_column not in column_restrictions:
                column_restrictions[perm_column] = False
            if perm_selects != ():
                column_restrictions[perm_column] = True
    for column in columns:
        if column in column_restrictions and column_restrictions[column]:
            return False
    return True


def check_read_on_columns(table, columns, permissions):
    columns = columns[:]
    #import sys
    #print >>sys.stderr, columns
    for perm in permissions:
        perm_table = perm[0].split('.')[0]
        perm_column = perm[0].split('.')[1]
        perm_scope = perm[1]
        perm_selects = perm[2]
        #print >>sys.stderr, priv_table, priv_column, priv_scope, str(table.__name__)
        if perm_table == table.__name__ and perm_column in columns and perm_scope == 'R':
            columns.remove(perm_column)

    #print >>sys.stderr, columns
    return len(columns) == 0


def append_weak_read_filter_by_conditions(table, columns, permissions, filter_by, fn_compile_filter_by):
    for perm in permissions:
        perm_table = perm[0].split('.')[0]
        perm_column = perm[0].split('.')[1]
        perm_scope = perm[1]
        perm_selects = perm[2]
        if perm_table == table.__name__ and perm_column in columns and perm_scope == 'R' and perm_selects != ():
            filter_by &= fn_compile_filter_by(table, perm_selects)
   # print >>sys.stderr, filter_by
    return filter_by

