# DNS Server
 Domain Name System (DNS) Server using Python. Once DNS query received, server finds it using upstream server (I used Google) and then caches it for 5 minutes. 

## Running
Install the dependencies in ```requirements.txt``` and run the server
```
pip3 install -r requirements.txt
python3 server.py
```
## How to test a server
Open second terminal, where you'll be sending requests. There, write ```dig @localhost <website.com>``` to request any website you want
### Example using dig:
```
dig @localhost lehigh.edu
dig @localhost bk.com
dig @localhost lehigh.edu
dig @localhost harvard.edu
```
### Expected Output
DNS query with answer section of website, including ip adresses of server, indicating that your DNS server has processed the request

### Example using nslookup
```
nslookup <website> localhost
nslookup lehigh.edu localhost
```
# Expected Output
A list of server ip adresses and domains

