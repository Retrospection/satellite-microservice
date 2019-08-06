from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import rsa
import binascii


pubkey_n = '8d7e6949d411ce14d7d233d7160f5b2cc753930caba4d5ad24f' \
           '923a505253b9c39b09a059732250e56c594d735077cfcb0c350' \
           '8e9f544f101bdf7e97fe1b0d97f273468264b8b24caaa2a90cd' \
           '9708a417c51cf8ba35444d37c514a0490441a773ccb121034f2' \
           '9748763c6c4f76eb0303559c57071fd89234d140c8bb965f9725'

pubkey_e = '10001'


n = int(pubkey_n, 16)
e = int(pubkey_e, 16)


def encrypt_password(password):
    return _rsa_encrypt(n, e, password)


def _rsa_encrypt(rsa_n, rsa_e, message):
    key = rsa.PublicKey(rsa_n, rsa_e)
    message = rsa.encrypt(message.encode(), key)
    message = binascii.b2a_hex(message)
    return message.decode()
