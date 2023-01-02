import pandas as pd
import numpy as np
import os
import email
from email import parser as ep
import email.policy
from bs4 import BeautifulSoup


class Email_importer:
    """
    Klasse zum Konvertieren von Emails in ein Textformat

    Verwendung:
    NON_SPAM = 'dateipfad/zu/nichtspam_emails"
    SPAM = 'dateipfad/zu/spam_emails"
    importer = Email_importer(NON_SPAM, SPAM)
    list_non_spam, list_spam = importer.get_text()
    """

    def __init__(self, email_dir):
        """
        Konstruktor, dem die E-Mail-Verzeichnisse übergeben, werden in denen die Emails abgelegt sind
        """
        self.email_dir = email_dir
        self.__read_emails()

    def __read_email(self, directory, filename):
        with open(os.path.join(directory, filename), "rb") as f:
            return ep.BytesParser(policy=email.policy.default).parse(f)

    def __read_emails(self):
        email_filenames = [name for name in sorted(os.listdir(self.email_dir))]
        self.emails = [self.__read_email(directory=self.email_dir, filename=name) for name in email_filenames]

    def __get_email_structure(self, email):
        if isinstance(email, str):
            return email
        payload = email.get_payload()
        if isinstance(payload, list):
            return "multipart({})".format(", ".join([
                self.__get_email_structure(sub_email)
                for sub_email in payload
            ]))
        else:
            return email.get_content_type()

    def __html_to_plain(self, email):
        try:
            soup = BeautifulSoup(email.get_content(), 'html.parser')
            return soup.text.replace('\n\n', '')
        except:
            return "empty"

    def __email_to_plain(self, email):
        struct = self.__get_email_structure(email)
        for part in email.walk():
            partContentType = part.get_content_type()
            if partContentType not in ['text/plain', 'text/html']:
                continue
            try:
                partContent = part.get_content()
            except:  # in case of encoding issues
                partContent = str(part.get_payload())
            if partContentType == 'text/plain':
                return partContent
            else:
                return self.__html_to_plain(part)

    def get_text(self):
        """
        Diese Methode liefert eine Liste der Nicht-Spam- und Spam-E-Mails im Textformat
        :return: (Liste von Nicht-Spam-Emails im Textformat, Liste von Spam-Emails im Textformat)
        """
        mail = [self.__email_to_plain(email) for email in self.emails]
        mail = [item for item in mail if item is not None]
        return mail
