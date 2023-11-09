""" Slack
    Slack: Slack操作Class
"""
import os

import requests
from requests import Response


class Slack:
    """Slack Class
    post: post to slack
    """

    def __init__(self):
        self.slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
        self.slack_app_token = os.environ["SLACK_APP_TOKEN"]

    def post(self, post_channel: str, post_message):
        """Post to Slack

        :param post_channel: 投稿チャンネル
        :param post_message: 投稿メッセージ
        :return none:
        """
        url: str = "https://slack.com/api/chat.postMessage"
        headers: dict[str, str] = {"Authorization": "Bearer " + self.slack_bot_token}
        data: dict[str, str] = {"channel": post_channel, "attachments": [post_message]}
        res: Response = requests.post(url, headers=headers, data=data)


# {
#   "channel": "C123ABC456",
#   "attachments": [
#       {
#           "fallback": "Plain-text summary of the attachment.",
#           "color": "#2eb886",
#           "pretext": "Optional text that appears above the attachment block",
#           "author_name": "Bobby Tables",
#           "author_link": "http://flickr.com/bobby/",
#           "author_icon": "http://flickr.com/icons/bobby.jpg",
#           "title": "Slack API Documentation",
#           "title_link": "https://api.slack.com/",
#           "text": "Optional text that appears within the attachment",
#           "fields": [
#               {
#                   "title": "Priority",
#                   "value": "High",
#                   "short": false
#               }
#           ],
#           "image_url": "http://my-website.com/path/to/image.jpg",
#           "thumb_url": "http://example.com/path/to/thumb.png",
#           "footer": "Slack API",
#           "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
#           "ts": 123456789
#       }
#   ]
# }
