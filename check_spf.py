#!/usr/bin/python3
#
# install dns package:
# pip3 install dnspython

import re, sys, socket, argparse
import dns.resolver

class SpfCheck:

    MAX_LOOPS = 10

    _num = 0
    _warn_len = 254

    _ns = ''
    _zone = ''

    _rows = []
    _warnings = []

    def __init__(self, zone, ns):
        self._zone = zone
        self._ns = ns

    def set_warn_char(self, warn_len):
        l = int(warn_len)
        if l >= 200:
            self._warn_len = l

    def set_critical(self, txt):
        print('CRITICAL: %s' % txt, file=sys.stderr)
        exit(2)

    def set_warning(self, txt):
        self._warnings.append(txt)

    def git(self, zone, type):
        rows = []
        resolv = dns.resolver.Resolver()
        resolv.nameservers = [socket.gethostbyname(self._ns)]
        res = resolv.resolve(zone, type, raise_on_no_answer=False)

        if res.rrset is not None:
            for row in res.rrset:
                rows.append(str(row).strip('"'))
        return rows

    def get_spf_rec(self, zone):
        res = self.git(zone, 'TXT')
        for row in res:
            if "v=spf1" in row:
                return row
        return None
      
