# fabric-slack-tools - Tools to integrate Fabric with Slack

Easily send messages during your deployments or any other Fabric command using slack.

## Installation
* `pip install fabric-slack-tools`

## Slack webhook setup
Create an incoming webhook on Slack integration configuration. There, you will be asked which user to post as and which
channel to announce to. This means you only need send data to the webhook URL, no need for any other configuration
on client side other than the URL itself and the message to announce

You can always override the relevnat parameters in the code and pass the channel or username in the decorator call (see one of the examples below).

## Example fabfile
```python
from fabric.api import *
from fabric_slack_tools import *

def do_build():
    send_slack_message("This is the text")

@roles("webserver")
@announce_deploy("MyProject")
def deploy_server():
    run("do something")

@roles("webserver")
@announce_deploy("MyProject", channel="anotherchannel", username="the other bot")
def deploy_something_else():
    run("do something")


init_slack("https://hooks.slack.com/services/XXXXXXXXX/YYYYYYYYY/ZZZZZZZZZZZZZZZZZZZZZZZZ")
```
