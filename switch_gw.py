# need package resolvconf in ubuntu 16+ 
# apt install resolvconf
# ssh tunnel is already running between client and server
# already have tun0 interface on both client and server
# ssh -vf -w 0:0 server_IP -t 'ifconfig tun0 up; ip addr add 10.0.2.100/32 peer 10.0.2.200 dev tun0'
# GW= client_GW_IP // this script 105.145.28.1
# ip link set tun0 up
# ip addr add 10.0.2.200/32 peer 10.0.2.100 dev tun0
# ip route add server_IP/32 via $GW
# 
import os,sys,subprocess,argparse,re

parser = argparse.ArgumentParser()
parser.add_argument('-s', help="Enter on to switch Gateway")
parser.add_argument('-d', help="Enter off to default Gateway")


def Switch_Gateway():
   os.system("ip route replace default via 10.0.2.100")

def Default_Gateway():
   os.system("ip route replace default via 105.145.28.1")

if len(sys.argv) == 1:
   parser.print_help()
   sys.exit(1)

args = parser.parse_args()


if args.s:
   Switch_Gateway()
   print "Switch Default Gateway to 10.0.2.100"
   with open("/etc/resolvconf/resolv.conf.d/head",'r') as dns:
	lines = dns.readlines()
   with open("/etc/resolvconf/resolv.conf.d/head",'w') as dns:
	for line in lines:
	     dns.write(re.sub(r'^#nameserver', 'nameserver',line))
   dns.close()
   print "add nameserver 8.8.8.8 and restart resolvconf"
   os.system("service resolvconf restart")
   sys.exit(0)

if args.d:
   Default_Gateway()
   print "Switch Default Gateway to 105.145.28.1"
   with open("/etc/resolvconf/resolv.conf.d/head",'r') as dns:      
        lines = dns.readlines()
   with open("/etc/resolvconf/resolv.conf.d/head",'w') as dns:
        for line in lines:
             dns.write(re.sub(r'^nameserver', '#nameserver',line))
   dns.close()
   print "remove nameserver 8.8.8.8 and restart resolvconf"
   os.system("service resolvconf restart")
   sys.exit(0)
