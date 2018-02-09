from netaddr import IPNetwork, IPSet, IPAddress
import sys
import dns.resolver

if len(sys.argv) < 1:
  print("Usuage check_spf.py domain_name")
  sys.exit(1)

host = sys.argv[1]

global spf_count
spf_count = 0

def spf_ips(host):
  ips = []
  textrecords = []
  try:
    textrecords = dns.resolver.query(host, 'TXT')
  except :
    print("<<<<<raise error %s>>>>>>" % host)

  for txtrecord in textrecords:
    record = txtrecord.to_text().strip('"')
    global spf_count
    spf_count = spf_count + 1
    print("  %s / spf count : %i" % (host, spf_count))
    if record.startswith('v=spf1'):
      print(record)
      parts = record.split(' ')[1:-1]
      resolved_ips = [i for i in parts if not i.startswith('include:')]
      for i in resolved_ips:
        if i == 'a' or i == 'mx' or i.startswith('ptr'):
          spf_count = spf_count + 1
          print("    %s / spf count : %i" % (i, spf_count))

      ips = ips + resolved_ips

      includes = [i for i in parts if i.startswith('include:')]
      hosts = [i[8:] for i in includes]
      for host in hosts:
        resolved_ips = spf_ips(host)
        ips = ips + resolved_ips
  return ips

print(spf_ips(host))
