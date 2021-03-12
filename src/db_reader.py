import sqlite3

from consts import *


class SqlDatabase(object):
    ID_INDEX = 0
    NAME_INDEX = 1

    def __init__(self, db_path, read_only=True, default_table=None):
        self.db_path = db_path if not read_only else URI_STRING.format(path=db_path)
        self.db_conn = None
        self.cursor = None
        self.default_table = default_table
        self.table_headers = dict()

    def open(self):
        self.db_conn = sqlite3.connect(self.db_path, uri='mode=ro' in self.db_path)
        self.cursor = self.db_conn.cursor()

    def execute(self, sql_statement):
        assert sql_statement[-1] == ';', 'SQL commands must end in ;'
        self.cursor.execute(sql_statement)
        return self.cursor.fetchall()

    def close(self):
        self.db_conn.close()
    
    def _choose_table_name(self, table):
        assert table or self.default_table, "Unclear which table to use"
        return table if table else self.default_table

    def get_column_names(self, table=None):
        """
        :param table: Name of the table, if None is given then using the default table 
        :return: Names of all columns in table
        """
        table = self._choose_table_name(table)
        
        if table in self.table_headers:
            return [col[self.NAME_INDEX] for col in self.table_headers[table]]
        
        headers = self.execute("PRAGMA table_info({table});".format(table=table))
        self.table_headers[table] = headers
        
        if table in self.table_headers:
            return [col[self.NAME_INDEX] for col in self.table_headers[table]]

    def header_to_id(self, header, table=None):
        table = self._choose_table_name(table)

        if table not in self.table_headers.keys():
            self.get_column_names(table)

        for cur_header in self.table_headers[table]:
            if cur_header[self.NAME_INDEX] == header:
                return cur_header[self.ID_INDEX]