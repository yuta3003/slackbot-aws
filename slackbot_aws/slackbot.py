"""slackbotのスラッシュコマンド用モジュール
"""
import json
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import getip
import run
import stop
import status

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_app_token = os.environ["SLACK_APP_TOKEN"]

# jsonの読み込み処理
with open("credentials.json", "r", encoding="utf-8") as credentials:
    credential: dict[str, list] = json.load(credentials)

app = App(token=slack_bot_token)


@app.command("/run")
def handle_some_command(ack, body, logger):
    """ command """
    ack("EC2が起動します。")
    logger.info(body)
    run.start_ec2(credential["EC2"])


@app.command("/stop")
def handle_some_command(ack, body, logger):
    """ command """
    ack("EC2が停止します。")
    stop.stop_ec2(credential["EC2"])
    logger.info(body)


@app.command("/state")
def handle_some_command(ack, body, logger):
    """ command """
    ack("EC2のステータスを確認します。")
    status.status_ec2(credential["EC2"])
    logger.info(body)


@app.command("/getip")
def handle_some_command(ack, body, logger):
    """ command """
    ack("EC2のIPアドレスを取得します。")
    getip.get_ip(credential["EC2"])
    logger.info(body)


# @app.command("/ip")
# def handle_some_command(ack, body, logger):
#    ack("IPアドレスを取得します。")
#    getIp.get_ip_ec2(credential["EC2"])
#    logger.info(body)

SocketModeHandler(app, slack_app_token).start()
