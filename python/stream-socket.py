import os
import sys
import json
import socket
import client


if  __name__ =='__main__':
    '''
    QUERY: keyword1,keyword2,...
    PORT: defaults to 9999
    run: python stream-socket.py QUERY GEO PORT
    '''
    soc = socket.socket()
    host = os.environ['NODEIP']

    query = ''
    if len(sys.argv) > 1:
        query = sys.argv[1]

    geo = False
    if len(sys.argv) > 2:
        geo = True

    port = 9999
    if len(sys.argv) > 3:
        port = int(sys.argv[3])

    soc.bind((host, port))
    soc.listen(5) # wait for connection
    con, addr = soc.accept()
    
    twitter = client.TwitterClient()
    twitter.stream(query,
                   geo = geo,
                   broadcast = lambda data: con.send(data.encode('utf-8')),
                   timer = 100)
