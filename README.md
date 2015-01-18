# fabric-slack-tools - Tools to integrate Fabric with Slack

Easily send messages during your deployments or any other Fabric command using slack.

## Installation
* `pip install fabric-slack-tools`

## Example fabfile
```python
from fabric.api import *
from fabric_slack_tools import *

def do_build():
    send_slack_message("This is the text", channel="#mychannel", username="TheBot")

@roles("webserver")
@announce_deploy("MyProject", channel="builds", username="MyBuildBot")
def deploy_server():
    run("do something")


init_slack("https://examplecorp.slack.com/services/hooks/incoming-webhook?token=xxxxxxxxxxx")
```
