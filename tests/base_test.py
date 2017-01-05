#-*- coding: utf-8 -*-
import unittest
from config.driver import Driver
import xml.etree.cElementTree as ET
import smtplib, os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class BaseTest(unittest.TestCase):
    def setUp(self):
        """
        starts a browser, maximize browser window and waits for a 10 sec for page load
        """
        self.driver = Driver.get()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        """
        close browser and webdriver session
        """
        self.driver.quit()

    def change_sell_chars(self, data):
        """
        changes first element in 'sell' list from 'ПРОДАМ' to 'sell'
        :param data: list of sell proposals
        :return: changed list
        """
        converted_data = []
        for proposal in data:
            proposal = list(proposal)
            proposal[0] = 'sell'
            converted_data.append(proposal)
        return converted_data

    def change_buy_chars(self, data):
        """
        changes first element in 'buy' list from 'КУПЛЮ' to 'buy'
        :param data: list of buy proposals
        :return: changed list
        """
        converted_data = []
        for proposal in data:
            proposal = list(proposal)
            proposal[0] = 'buy'
            converted_data.append(proposal)
        return converted_data

    # TODO
    # Need refactor
    def convert_data_to_xml(self, best_buys, best_sells):
        """
        converts data taken from sql database to xml file
        :param best_buys: list of the buy proposals
        :param best_sells: list of the sell proposals
        """
        results = ET.Element("results")
        buys = ET.SubElement(results, "buys")
        sells = ET.SubElement(results, "sells")
        for element in best_buys:
            proposal = ET.SubElement(buys, "type")
            amount = ET.SubElement(buys, "amount")
            rate = ET.SubElement(buys, "rate")

            proposal.text = str(element[0])
            amount.text = str(element[1])
            rate.text = str(element[2])

        for element in best_sells:
            proposal = ET.SubElement(sells, "type")
            amount = ET.SubElement(sells, "amount")
            rate = ET.SubElement(sells, "rate")

            proposal.text = str(element[0])
            amount.text = str(element[1])
            rate.text = str(element[2])

        tree = ET.ElementTree(results)
        tree.write("currency.xml")

    def send_email_to_misha(self, send_from, send_to, subject, message):
        """
        sends an email with xml file attached
        :param send_from: email from
        :param send_to: email to
        :param subject: a subject
        :param message: body message
        """
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Subject'] = subject

        text = MIMEText(message, 'plain')
        msg.attach(text)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open('currency.xml', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename('currency.xml')))
        msg.attach(part)

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()

        mail.login(send_from, password)# password is deleted for security
        mail.sendmail(send_from, send_to, msg.as_string())
        mail.quit()

