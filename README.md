p.py
==============

Fuck GFW with 25 lines of code. Currently only HTTP supported.

Install Twisted

    apt-get install python-twisted
    
Or

    pip install twisted

On your server:

    python p.py server
    
On your client:

    python p.py client server_ip

Set your browser proxy:

    HTTP 127.0.0.1:8080
