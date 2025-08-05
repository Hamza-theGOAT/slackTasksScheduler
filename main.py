import json
import os
from dotenv import load_dotenv
from slack_sdk import WebClient
import pystray
from pystray import MenuItem as Item, Menu
import PIL.Image


def getCredz():
    load_dotenv()
    userToken = os.getenv('userToken')
    # print(f"Bot Token fetched from .env: {botToken}")
    client = WebClient(token=userToken)

    with open('tasks.json', 'r') as j:
        tasks = json.load(j)

    return client, tasks


def slackMsg(client, channelID, msg):
    response = client.chat_postMessage(
        channel=channelID,
        text=msg
    )

    return response['ts']


def buildMenu(client, tasks):
    def taskItems(taskInfo):
        return lambda icon, item: slackMsg(
            client,
            channelID=taskInfo['assignee'],
            msg=taskInfo['message']
        )

    def taskGroups(gruopTasks):
        return Menu(*(Item(taskName, taskItems(info))
                      for taskName, info in gruopTasks.items()))

    menuItems = []

    for groupName, groupTasks in tasks.items():
        menuItems.append(Item(groupName, taskGroups(groupTasks)))

    menuItems.append(Item("Exit", lambda icon, item: icon.stop()))

    return Menu(*menuItems)


def iconTray(client, tasks):
    img = PIL.Image.open(os.path.join(
        "source_dir", "menuIcon.png"
    ))

    icon = pystray.Icon("TasksTray", img, "Slack Task Menu",
                        buildMenu(client, tasks)
                        )
    icon.run()


def main():
    client, tasks = getCredz()
    iconTray(client, tasks)


if __name__ == '__main__':
    main()
