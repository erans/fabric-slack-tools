# The MIT License (MIT)
#
# Copyright (c) 2015 Eran Sandler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import
import functools
import urllib2
import datetime
import getpass
try:
    import simplejson as json
except ImportError:
    import json

from fabric.api import env

_web_hook_url = None

def init_slack(web_hook_url):
    global _web_hook_url
    _web_hook_url = web_hook_url

def send_slack_message(text, channel, username="SlackMessageBot", web_hook_url=None):
    """
    send_slack_message - allow sending a slack message to a channel via a webhook.
    To configure a web hook:
    - go to "Service Integrations -> Incoming WebHooks -> Add"
    - Copy the hook URL and use it via the web_hook_url function parameter or globally
      (so you won't have to repeat it) by calling init_slack once at the bottom
      of your fabfile
    """
    global _web_hook_url

    if web_hook_url is None:
        if _web_hook_url:
            web_hook_url = _web_hook_url
        else:
            raise ValueError("web_hook_url must be set")

    if channel is None:
        raise ValueError("channel must be set")

    data = {
        "text" : text,
        "channel" : channel,
        "username" : username
    }

    req = urllib2.Request(web_hook_url)
    req.add_header("Content-Type", "application/json")
    urllib2.urlopen(req, json.dumps(data))

def announce_deploy(project, channel="#ops", username="DeployBot", web_hook_url=None):
    """
    announce_deploy - a decorator to announces a new deploy of the specificed project start,
    who started it and when. Also sends a message when the deploy ends and how long it took.
    """

    def real_announce_deploy(func):
        @functools.wraps(func)
        def inner_decorator(*args, **kwargs):
            n = datetime.datetime.utcnow()
            send_slack_message("%s deploy started by %s on %s" % (project, getpass.getuser(), env.host), channel, username, web_hook_url)
            return_value = func(*args, **kwargs)
            send_slack_message("%s deploy ended by %s on %s. Took: %s" % (project, getpass.getuser(), env.host, str(datetime.datetime.utcnow() - n)), channel, username)

            return return_value
        return inner_decorator
    return real_announce_deploy

__all__ = ["send_slack_message", "announce_deploy"]
