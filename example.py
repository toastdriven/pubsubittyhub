import urllib2
import sys
from urllib import urlencode
try:
    import json
except ImportError:
    import simplejson as json

print 'Testing index...'
content = urllib2.urlopen('http://localhost:8080/').read()

print 'Creating a channel...'
content = urllib2.urlopen('http://localhost:8080/channels', data={}).read()
channel_id = json.loads(content)['id']

print "Adding subscriber to channel '%s'..." % channel_id
body = urlencode({'data': json.dumps({'channel': channel_id, 'url': sys.argv[1]})})
content = urllib2.urlopen('http://localhost:8080/subscribers', data=body).read()
print content

print "Posting message to channel '%s'..." % channel_id
body = urlencode({'data': json.dumps({'channel': channel_id, 'message': 'O HAI'})})
content = urllib2.urlopen('http://localhost:8080/messages', data=body).read()
print content
