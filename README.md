# dns-server
 Domain Name System (DNS) Server using Python. Once DNS query received, server finds it using upstream server (I used Google) and then caches it for 5 minutes. 

## Running
Install the dependencies in ```requirements.txt``` and run the server
```
pip3 install -r requirements.txt
python3 server.py
```
## How to test a server
Open second terminal, where you'll be sending requests. There, write ```dig @localhost <website.com>``` to request any website you want. 
### Example using dig:
```
dig @localhost lehigh.edu
dig @localhost bk.com
dig @localhost lehigh.edu
dig @localhost harvard.edu
```
### Expected Output
You should see DNS query results for example.com, indicating that your DNS server has processed the request.

### Example using nslookup
```
add later
```
# Expected Output
bla bla bla

