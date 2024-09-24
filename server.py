
from socket import *
import dns
import dns.message
import dnslib
import time

cache = {}
upstream_DNS_server_ip = '8.8.8.8'

#get raw dns query data, return turple structured

def parse_dns_query(data):
    query = dnslib.DNSRecord.parse(data)

    print("Transaction ID:", query.header.id)
    print("Domain Name:", query.q.qname)
    print("Query Type:", dnslib.QTYPE[query.q.qtype])
    print("Query Class:", dnslib.CLASS[query.q.qclass])

    return query.header.id, query.q.qname, query.q.qtype, query.q.qclass


def handler(data, addr, server_socket):
    transaction_id, domain_name, query_type, query_class = parse_dns_query(data)
    current_time = time.time()
    

    if domain_name in cache and cache[domain_name][1] > current_time: #if cached
        response = cache[domain_name][0]

        cached_dns_record = dnslib.DNSRecord.parse(response)
        cached_dns_record.header.id = transaction_id
        response = cached_dns_record.pack()

    else: #if not cached, send it to google
        upstream_socket = socket(AF_INET, SOCK_DGRAM)
        upstream_socket.sendto(data, ('8.8.8.8', 53))

        response, data = upstream_socket.recvfrom(2048)
        cache[domain_name] = (response, current_time + 300)
        upstream_socket.close()

    return response

def socker_server(ip: str, port: int = 53):
    serv_socket = socket(AF_INET, SOCK_DGRAM)
    serv_socket.bind((ip, port))

    print('The server is ready to receive') 

    # continuous loop
    while True:
        message, clientAddress = serv_socket.recvfrom(2048)
        modifiedMessage = handler(message, clientAddress, serv_socket)

        serv_socket.sendto(modifiedMessage, clientAddress)
        
if __name__ == "__main__":
    socker_server('', 53)