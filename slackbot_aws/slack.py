import os
import requests


class Slack:
    """
    Slack操作Class
    """

    def __init__(self):
        self.slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
        self.slack_app_token = os.environ["SLACK_APP_TOKEN"]

    def post(self, postChannel, postMessage):
        """
        投稿
		:param channel: 投稿チャンネル
		:param postMessage: 投稿メッセージ
        """
        url = "https://slack.com/api/chat.postMessage"
        headers = {"Authorization": "Bearer " + self.slack_bot_token}
        data  = {
            'channel': postChannel,
            'text': postMessage
        }
        r = requests.post(url, headers=headers, data=data)
