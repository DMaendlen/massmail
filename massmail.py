#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

# This script takes a list of recipients and sends an e-mail. Both, the list of
# recipients and the e-mail are given as files.

# fill out the following sender-related values:
senderAddress = '1_shack@bifroe.st'
subject = 'shack Beitrag / Verwendungszweck'
sendHost = 'localhost'

import csv
import sys
import smtplib
#import gnupg

from email.mime.text import MIMEText

def parseRecipientListFile(filename):
    """
    Reads recipients info from csv-file. Parses file according to following rules:
    - First line has to be a column heading, containing the names of the fields
    - File has to contain at least the fields 'id', 'last_name', 'first_name', 'mail_address'
    - Each line has to be ended by a ';'
    - Each line must only contain one set of data

    Returns a list of dicts with the first row as keys for each following row, e.g.
    [last_name] [Mändlen]
    [first_name] [David]
    [id] [123]
    [mail_address] [f00@bar.baz]
    """

    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile)
        csvdata = list(csvreader)
    return csvdata

def readMailTextFile(filename):
    """
    Reads text from a file.
    Returns string containing the whole text.
    """

    with open(filename) as textFile:
        text = textFile.read()
    return text

def sendMail(recipientList, mailText, key):
    for member in recipientList:
        recipientAddress = member['mail_address']
        msg = MIMEText(mailText.format(**member), _charset='utf-8')
        msg['From'] = senderAddress
        msg['To'] = recipientAddress
        msg['Subject'] = subject

#    if key:
#        gpg = gnupg.GPG()
#        if gpg.list_keys():
#            basemsg = msg
#            basetext = basemsg.as_string().replace('\n', '\r\n')
#            signature = str(gpg.sign(basetext, detach=True, keyid=key))
#            if signature:
#                signmsg = messageFromSignature(signature)
#                msg = MIMEMultipart(_subtype="signed", micalg="pgp-sha1",
#                protocol="application/pgp-signature")
#                msg.attach(basemsg)
#                msg.attach(signmsg)
#            else:
#                sys.exit('Error: failed to sign message!')
#        else:
#            sys.exit('Error: no GPG keys available!')

        s = smtplib.SMTP(sendHost)
        s.sendmail(senderAddress, recipientAddress, msg.as_string())
        s.quit()

def main():

    args = sys.argv[1:]

    if len(args) < 2:
        print('usage: mailsender <recipientlist> <mailtext> <GPG-keyid>(optional)')
        sys.exit(1)

    recipientListFile = args[0]
    mailTextFile = args[1]
    if len(args) == 3:
        key = args[2]
    else:
        key = ''

    recipientList = parseRecipientListFile(recipientListFile)
    mailText = readMailTextFile(mailTextFile)

    sendMail(recipientList, mailText, key)

    sys.exit(0)
    
if __name__ == '__main__':
        main()
