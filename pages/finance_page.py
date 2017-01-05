from base_page import BasePage
from config import finance_config as CONST


class FinancePage(BasePage):
    def __init__(self):
        super(FinancePage, self).__init__(CONST.finance_url)

    def delete_ad_text_block(self, table):
        """
        deletes advertisement in proposal table
        :param table: table of proposals taken from http://miniaylo.finance.ua/
        :return: table without advertisement block
        """
        index = 0
        for tr in table:
            index +=1
            if tr.get_attribute('class') == 'ad-text-block':
                del table[index-1]
        return table

    def parse_table_in_rows(self, table):
        """
        prses table object to rows
        :param table: unparsed table object
        :return: parsed table
        """
        parsed_table = []
        for tr in table.find_elements_by_tag_name('tr'):
            parsed_table.append(tr)
        return parsed_table

    def extract_table(self):
        """
        extract of proposals taken from http://miniaylo.finance.ua/.
        it takes only 3 values - type of proposal, amount and rate
        :return: extracted table
        """
        table = self.driver.find_element_by_xpath(CONST.table)
        parsed_table = self.parse_table_in_rows(table)
        self.delete_ad_text_block(parsed_table)

        exctracted_table = []
        for tr in parsed_table:
            row = []
            row.append(tr.find_elements_by_tag_name('td')[1].text)
            row.append(tr.find_elements_by_tag_name('td')[2].text[:-3])
            row.append(float(tr.find_elements_by_tag_name('td')[3].text[2:]))
            exctracted_table.append(row)

        return exctracted_table
