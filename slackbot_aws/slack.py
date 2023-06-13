"""
slackに投稿するモジュール
"""
import os
import requests


class Slack:
    """
    Slack操作Class
    """

    def __init__(self):
        self.slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
        self.slack_app_token = os.environ["SLACK_APP_TOKEN"]

    def post(self, post_channel, post_message):
        """
        投稿

        :param post_channel: 投稿チャンネル
        :param post_message: 投稿メッセージ
        :return none:
        """
        url = "https://slack.com/api/chat.postMessage"
        headers = {"Authorization": "Bearer " + self.slack_bot_token}
        data = {"channel": post_channel, "text": post_message}
        request = requests.post(url, headers=headers, data=data)
