
from socket import *
from dnslib import DNSRecord, DNSHeader, RR, QTYPE, RCODE, A, CLASS
import time


cache = {} # Cache key is the domain name
upstream_DNS_server_ip = '8.8.8.8' #Gogole's upstream server
CACHE_TTL = 300  # time for cache to stay

#get raw dns query data, return turple structured

def parse_dns_query(data):
    query = DNSRecord.parse(data)

    transaction_id = query.header.id
    domain_name = str(query.q.qname)
    query_type = query.q.qtype
    query_class = query.q.qclass

    print("Transaction ID:", transaction_id)
    print("Domain Name:", domain_name)
    print("Query Type:", QTYPE[query_type])
    print("Query Class:", CLASS[query.q.qclass])

    return transaction_id, domain_name, query_type, query_class


def handler(data, addr, server_socket):
    transaction_id, domain_name, query_type, query_class = parse_dns_query(data)
    current_time = time.time() 
    request = DNSRecord.parse(data)
    
    # Cache key is the domain name
    if domain_name in cache and cache[domain_name][1] > current_time:
        # Serve from cache
        ip_addresses = cache[domain_name][0]
        response = DNSRecord(DNSHeader(id=transaction_id, qr=1, aa=1, ra=1), q=request.q)

        #append ip addresses to answers
        for ip in ip_addresses:
            response.add_answer(RR(domain_name, query_type, rdata=A(ip), ttl=CACHE_TTL))

        response = response.pack()
        print("Cache hit: ", domain_name)


    else:
        # Forward the query to the upstream DNS server
        upstream_socket = socket(AF_INET, SOCK_DGRAM)
        upstream_socket.settimeout(5) #wait for 5 seconds
        upstream_socket.sendto(data, (upstream_DNS_server_ip, 53))

        try:
            #request and parse response from upstream DNS server
            response_data, response_addr = upstream_socket.recvfrom(2048)
            upstream_response = DNSRecord.parse(response_data)

            #extract ip addresses
            ip_addresses = [str(rr.rdata) for rr in upstream_response.rr if rr.rtype == QTYPE.A]

            #cache ip addresses
            cache[domain_name] = (ip_addresses, current_time + CACHE_TTL)
            print("Cache miss: ", domain_name)

            # edit response to have same transaction ID
            upstream_response.header.id = transaction_id
            response = upstream_response.pack()
        except timeout:
            #return None
            print("Timed out, too slow broski")
            response = None
            source = 'timeout'
        finally:
            upstream_socket.close()

    # Send the response back to the client
    if response:
        server_socket.sendto(response, addr)
    else:
        print("No response to send to client")
    print("=========================================")

def socker_server(ip: str, port: int = 53):
    serv_socket = socket(AF_INET, SOCK_DGRAM)
    serv_socket.bind((ip, port))

    print('The server is ready to receive') 

    # continuous loop
    while True:
        message, clientAddress = serv_socket.recvfrom(2048)
        handler(message, clientAddress, serv_socket)

        
if __name__ == "__main__":
    socker_server('', 53)