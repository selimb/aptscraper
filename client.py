import rpyc

from donna.config import CONF

conn = rpyc.connect(CONF.RPYC_HOST, CONF.RPYC_PORT)
service = conn.root
