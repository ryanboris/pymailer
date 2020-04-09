from os import environ as ENV_VAR
from imapclient import IMAPClient
from typing import List
import re
import email


class IMAP(IMAPClient):
    USERNAME = ENV_VAR['USERNAME']
    PASSWORD = ENV_VAR['PASSWORD']
    HOST = ENV_VAR['HOST']
    subs: List[str] = []
    times: List[str] = []
    dates: List[str] = []

    def __init__(self):
        super().__init__(self.HOST)
        self.login(self.USERNAME, self.PASSWORD)


if __name__ == '__main__':
    imap = IMAP()
    with imap as server:
        server.select_folder('INBOX', readonly=True)

        messages = server.search('UNSEEN')
        for uid, data in server.fetch(messages, 'RFC822').items():
            email_msg = email.message_from_bytes(data[b'RFC822'])
            imap.subs.append(email_msg.get('subject'))

    for string in imap.subs:
        imap.times.extend(re.findall(r'[0-9][0-9]:[0-9][0-9][p|a]{1}', string))
        imap.dates.extend(re.findall(r'\w{3},\sApr\s\d+,\s{1}\d+', string))

    print(list(zip(imap.times, imap.dates)))
