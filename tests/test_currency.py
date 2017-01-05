# TODO
# Task:
# - go to http://miniaylo.finance.ua/
# - extract usd/uah currency table (type, amount, rate)
# - save data in local sqllite database
# - select data from DB and convert it to xml file
# - send email to mykhailo.poliarush@gmail.com with best currency buy\sell option in email body and xml filed attached
# - all actions should be logged during execution in separate log file for debug purposes
# - write unit tests on your code to test your application


from tests.base_test import BaseTest
from pages.finance_page import FinancePage
from config.database import DataBase
from config import mail_consts as MAIL_CONSTS


class TestCurrency(BaseTest):
    def test_currency(self):
        finance_page = FinancePage()
        database = DataBase()

        table = finance_page.extract_table()
        database.save_data_in_database(table)
        best_buys = self.change_buy_chars(database.get_best_buy())
        best_sells = self.change_sell_chars(database.get_best_sell())
        database.close_database()
        self.convert_data_to_xml(best_buys, best_sells)

        message = "best buy is " + str(best_buys[0][2]) + " and best sell is " + str(best_sells[0][2])
        self.send_email_to_misha(MAIL_CONSTS.send_from,
                                 MAIL_CONSTS.send_to,
                                 MAIL_CONSTS.subject,
                                 message,
                                 )
