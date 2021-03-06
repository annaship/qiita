__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Qiita project"
__credits__ = ["Jose Antonio Navas Molina", "Adam Robbins-Pianka",
               "Joshua Shorenstein"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"

from psycopg2 import connect, Error as PostgresError

from .connections import postgres
from .exceptions import QiitaDBSQLExecutionError, QiitaDBSQLConnectionError
from qiita_db.config import qiita_db_config


class SQLConnectionHandler(object):
    """Encapsulates the DB connection with the Postgres DB"""
    def __init__(self):
        self._connection = connect(user=qiita_db_config.user,
                                   database=qiita_db_config.database,
                                   host=qiita_db_config.host,
                                   port=qiita_db_config.port)
        self._dflt_cursor = self.connection.cursor()
        self._cursors = []

    def __del__(self):
        """"""
        self._dflt_cursor.close()
        for cur in self._cursors:
            if not cur.closed:
                cur.close()

    def get_postgres_cursor(self):
        """ Returns a Postgres cursor

        Inputs: None

        Returns:
            pgcursor: the postgres.cursor()

        Raises a RuntimeError if the cursor cannot be created
        """
        try:
            pgcursor = self.connection.cursor()
        except PostgresError, e:
            raise QiitaDBSQLConnectionError("Cannot get postgres cursor! %s"
                                            % e)
        self._cursors.append(pgcursor)
        return pgcursor

    def _check_sql_args(self, sql_args):
        """ Checks that sql_args have the correct type

        Inputs:
            sql_args: SQL arguments

        Raises a TypeError if sql_args does not have the correct type,
            otherwise it just returns the execution to the caller
        """
        # Check that sql arguments have the correct type
        if sql_args and type(sql_args) not in [tuple, list]:
            raise TypeError("sql_args should be tuple or list. Found %s " %
                            type(sql_args))

    def execute_fetchall(self, sql, sql_args=None, pgcursor=None):
        """ Executes a fetchall SQL query

        Inputs:
            sql: string with the SQL query
            sql_args: tuple with the arguments for the SQL query
            pgcursor: the postgres cursor

        Returns:
            The results of the fetchall query as a list of tuples

        Raises a QiitaDBSQLExecutionError if there is some error executing the
            SQL query

        Note: from psycopg2 documentation, only variable values should be bound
            via sql_args, it shouldn't be used to set table or field names. For
            those elements, ordinary string formatting should be used before
            running execute.
        """
        if not pgcursor:
            pgcursor = self._dflt_cursor
        # Check that sql arguments have the correct type
        _check_sql_args(sql_args)
        # Execute the query
        try:
            pgcursor.execute(sql, sql_args)
            result = pgcursor.fetchall()
            postgres.commit()
        except PostgresError, e:
            postgres.rollback()
            raise QiitaDBSQLExecutionError("Error running SQL query: %s", e)
        return result

    def execute_fetchone(self, sql, sql_args=None, pgcursor=None):
        """ Executes a fetchone SQL query

        Inputs:
            pgcursor: the postgres cursor
            sql: string with the SQL query
            sql_args: tuple with the arguments for the SQL query

        Returns:
            The results of the fetchone query as a tuple

        Raises a QiitaDBSQLExecutionError if there is some error executing the
            SQL query

        Note: from psycopg2 documentation, only variable values should be bound
            via sql_args, it shouldn't be used to set table or field names. For
            those elements, ordinary string formatting should be used before
            running execute.
        """
        if not pgcursor:
                pgcursor = self._dflt_cursor
        # Check that sql arguments have the correct type
        _check_sql_args(sql_args)
        # Execute the query
        try:
            pgcursor.execute(sql, sql_args)
            result = pgcursor.fetchone()
            postgres.commit()
        except PostgresError, e:
            postgres.rollback()
            raise QiitaDBSQLExecutionError("Error running SQL query: %s", e)
        return result

    def execute(self, sql, sql_args=None, pgcursor=None):
        """ Executes an SQL query with no results

        Inputs:
            pgcursor: the postgres cursor
            sql: string with the SQL query
            sql_args: tuple with the arguments for the SQL query

        Raises a QiitaDBSQLExecutionError if there is some error executing the
            SQL query

        Note: from psycopg2 documentation, only variable values should be bound
            via sql_args, it shouldn't be used to set table or field names. For
            those elements, ordinary string formatting should be used before
            running execute.
        """
        if not pgcursor:
            pgcursor = self._dflt_cursor
        # Check that sql arguments have the correct type
        _check_sql_args(sql_args)
        # Execute the query
        try:
            pgcursor.execute(sql, sql_args)
            postgres.commit()
        except PostgresError, e:
            postgres.rollback()
            raise QiitaDBSQLExecutionError("Error running SQL query: %s", e)

    def executemany(self, sql, sql_args_list, pgcursor=None):
        """ Executes an executemany SQL query with no results

        Inputs:
            pgcursor: the postgres cursor
            sql: string with the SQL query
            sql_args_list: list with tuples with the arguments for the SQL
                query

        Raises a QiitaDBSQLExecutionError if there is some error executing the
            SQL query

        Note: from psycopg2 documentation, only variable values should be bound
            via sql_args, it shouldn't be used to set table or field names. For
            those elements, ordinary string formatting should be used before
            running execute.
        """
        if not pgcursor:
            pgcursor = self._dflt_cursor
        # Check that sql arguments have the correct type
        for sql_args in sql_args_list:
            _check_sql_args(sql_args)
        # Execute the query
        try:
            pgcursor.executemany(sql, sql_args_list)
            postgres.commit()
        except PostgresError, e:
            postgres.rollback()
            raise QiitaDBSQLExecutionError("Error running SQL query: %s", e)
