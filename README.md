# fabric-slack-tools - Tools to integrate Fabric with Slack

Easily send messages during your deployments or any other Fabric command using slack.

## Installation
* `pip install fabric-slack-tools`

## Slack webhook setup
Create an incoming webhook on Slack integration configuration. There, you will be asked which user to post as and which
channel to announce to. This means you only need send data to the webhook URL, no need for any other configuration
on client side other than the URL itself and the message to announce.

However, if you want to customise the `channel` and `username`, you can still do that by specifying the optional
parameters in the `announce_deploy` annotation.

You can always override the relevant parameters in the code and pass the channel or username in the decorator call (see one of the examples below).

## Example fabfile

- Minimal setup, with `channel` and `username` set on Slack settings:

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

@roles("webserver")
@announce_deploy("MyProject", channel="anotherchannel", username="the other bot", icon_emoji=":panda_face:")
def deploy_something_else():
    run("do something")


init_slack("https://hooks.slack.com/services/XXXXXXXXX/YYYYYYYYY/ZZZZZZZZZZZZZZZZZZZZZZZZ")
```

- To announce to a specific channel or want your bot to act under a particular username, you can do:

```python

@roles("webserver")
@announce_deploy("MyProject", channel="#devops", username="deployment-bot")
def deploy_server():
    run("do something")

```

- To change the default webook icon to a specific emoji, you can do:

```python

@roles("webserver")
@announce_deploy("MyProject", channel="#devops", username="deployment-bot", icon_emoji=":panda_face:")
def deploy_server():
    run("do something")

```
