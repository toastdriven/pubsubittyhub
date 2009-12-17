=============
pubsubittyhub
=============


PubSubHubbub via webhooks. Mostly a port of watercoolr_.

.. _watercoolr: http://github.com/capotej/watercoolr


Usage
=====

Simply run ``python pubsubittyhub.py``. The daemon will start running.

For a client reference usage, please refer to the ``example.py`` file included
with the distribution.


Creating A Channel
==================

Send an empty POST request to ``http://localhost:8080/channels``. This will
return a JSON payload with the channel name (a hash).

Example Response::

    {"id": "5e0de16a5467cd0fe940b2f76f537a98"}


Adding A Subscriber To The Channel
==================================

Send a POST request to ``http://localhost:8080/subscribers`` with a single key
(``data``) that contains a url-encoded JSON string of the channel name and the
webhook URL for that subscriber.

You receive back a JSON payload of ``status`` (``true`` or ``false``).

Example Request::

    data='{"channel": "5e0de16a5467cd0fe940b2f76f537a98", "url": "http://mysite.com/api/hooks/notify"}'

Example Response::

    {"status": true}


Posting A Message To All Subscribers
====================================

Send a POST request to ``http://localhost:8080/messages`` with a single key
(``data``) that contains a url-encoded JSON string of the channel name and the
message to pass along to the subscribers.

You receive back a JSON payload of ``status`` (``true`` or ``false``).

Example Request::

    data='{"channel": "5e0de16a5467cd0fe940b2f76f537a98", "message": "We totally just rolled out a new beta feature! Check it out at http://mysite.com/feature/new"}'

Example Response::

    {"status": true}


Thanks to Julio Capote (capotej) for the awesome reference implementation. It
was a fun little side project.

:author: Daniel Lindsley
:date: 2009-12-17
