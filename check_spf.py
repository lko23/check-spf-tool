from netaddr import IPNetwork, IPSet, IPAddress
import sys
import dns.resolver

if len(sys.argv) < 2:
  print "Usuage check_spf.py domain_name ip_address [ip_address] ..."
  sys.exit(1)

host = sys.argv[1] 
ips = None
if len(sys.argv) > 2: 
  ips = sys.argv[2:]

def spf_ips(host):
  ips = []
  for txtrecord in dns.resolver.query(host, 'TXT'):
    record = txtrecord.to_text().strip('"')
    if record.startswith('v=spf1'):
      parts = record.split(' ')[1:-1]
      resolved_ips = [i for i in parts if not i.startswith('include:')]
      ips = ips + resolved_ips

      includes = [i for i in parts if i.startswith('include:')]
      hosts = [i[8:] for i in includes]
      for host in hosts:
        resolved_ips = spf_ips(host)
        ips = ips + resolved_ips
  return ips

def spf_ip_set(host):
  records = spf_ips(host)
  networks = [n[4:] for n in records]
  return IPSet(networks)
  

if ips is None:
  print spf_ips(host)
else:
  ip_set = spf_ip_set(host)
  for ip in ips:
    if ip in ip_set:
      print "%s is whitelisted" % ip
    else:
      print "%s is not whitelisted" % ip
