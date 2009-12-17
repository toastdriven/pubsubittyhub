"""
A tiny implementation of pubsubhubbub with webhooks.

Not recommended at scale, but maybe fun for little projects.
Based off ``watercoolr`` (http://github.com/jcapote/watercoolr).
"""
import httplib2
import os
import random
import sqlite3
import time
from bitty import *
from itty import *

try:
    from hashlib import sha1
except ImportError:
    from sha import sha as sha1

try:
    import json
except ImportError:
    import simplejson


DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')
CREATE_CHANNELS = """CREATE TABLE channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32) UNIQUE
);"""
CREATE_SUBSCRIBERS = """CREATE TABLE subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER,
    url VARCHAR(128),
    FOREIGN KEY (channel_id) REFERENCES channels(id)
);"""


def get_db():
    return Bitty("sqlite://%s" % DB_PATH)


def initialize_db(bit):
    try:
        bit.raw(CREATE_CHANNELS.replace('\n', ''))
    except:
        pass
    
    try:
        bit.raw(CREATE_SUBSCRIBERS.replace('\n', ''))
    except:
        pass


def generate_id():
    base = random.randint(0, 100000000)
    salt = time.time()
    return sha1("%s%s" % (base, salt)).hexdigest()[:32]


@get('/')
def index(request):
    return 'Post to `/channels`, `/subscribers` or `/messages`.'


@post('/channels')
def channels(request):
    bit = get_db()
    channel_id = generate_id()
    bit.add('channels', name=channel_id)
    return Response(json.dumps({'id': channel_id}), content_type='application/json')


@post('/subscribers')
def subscribers(request):
    bit = get_db()
    success = False
    raw_data = request.POST.get('data')
    
    if raw_data:
        data = json.loads(raw_data)
        channel = data.get('channel', 'boo')
        url = data.get('url', None)
        channel = bit.get('channels', name=channel)
        
        if channel:
            channel_id = channel['id']
            
            if url and channel_id:
                subs = bit.find('subscribers', channel_id=channel_id, url=url)
                
                if not len(subs):
                    bit.add('subscribers', channel_id=channel_id, url=url)
                    success = True
    
    return Response(json.dumps({'status': success}), content_type='application/json')


@post('/messages')
def messages(request):
    bit = get_db()
    success = False
    raw_data = request.POST.get('data')
    
    if raw_data:
        data = json.loads(raw_data)
        channel = data.get('channel', 'boo')
        message = data.get('message', None)
        channel = bit.get('channels', name=channel)
        
        if channel:
            channel_id = channel['id']
            
            if message and channel_id:
                subs = bit.find('subscribers', channel_id=channel_id)
                
                for sub in subs:
                    success = True
                    http = httplib2.Http(timeout=10)
                    resp, content = http.request(sub['url'], "POST", body=message, headers={'content-type':'text/plain'} )
    
    return Response(json.dumps({'status': success}), content_type='application/json')


run_itty()
