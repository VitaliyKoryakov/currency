#-*- coding: utf-8 -*-
import sqlite3


class DataBase(object):
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()

    def create_database(self, table):
        """
        creates database in mamory with content taken from 'table'
        :param table: table of buy/sell proposals
        """
        self.c.execute('''CREATE TABLE currency
             (type text, amount text, rate real)''')
        self.c.executemany("INSERT INTO currency VALUES (?,?,?)", table)
        self.conn.commit()

    def close_database(self):
        """
        closes database
        """
        self.conn.close()

    def get_best_buy(self):
        """
        takes 'buy' proposals in DESC order
        :return: list of 'buy' proposals
        """
        self.c.execute("SELECT * FROM currency WHERE type = 'КУПЛЮ' ORDER BY rate DESC")
        return self.c.fetchall()

    def get_best_sell(self):
        """
        takes 'sell' proposals in order
        :return: list of 'sell' proposals
        """
        self.c.execute("SELECT * FROM currency WHERE type = 'ПРОДАМ' ORDER BY rate")
        return self.c.fetchall()

    def save_data_in_database(self, table):
        self.create_database(table)
