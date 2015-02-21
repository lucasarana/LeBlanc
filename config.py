# -*- coding: utf-8 *-*
import ssl
# from LeanderCommon import sslconf

listenAddress = '0.0.0.0'
port = 8888
processes = 1

ssl_options = {
    'certfile':'',
    'keyfile':'',
    #'ssl_version':ssl.PROTOCOL_TLSv1,
    #'ciphers':sslconf.ciphers_high7,
}

# dbInfoAnnie = {'host':'192.168.0.6', 'port':5432, 'database':'lega_partitions', 'user':'bo-admin', 'password':'J9vSTgCm'}