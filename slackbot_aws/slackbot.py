"""slackbotのスラッシュコマンド用モジュール
"""
import os

import fetch
import getip
import run
import status
import stop
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_app_token = os.environ["SLACK_APP_TOKEN"]

app = App(token=slack_bot_token)


@app.command("/run")
def handle_some_command(ack, body, command, logger):
    """command"""
    ack("EC2が起動します。")
    logger.info(body)
    run.start_ec2(command["text"])


@app.command("/stop")
def handle_some_command(ack, body, command, logger):
    """command"""
    ack("EC2が停止します。")
    stop.stop_ec2(command["text"])
    logger.info(body)


@app.command("/state")
def handle_some_command(ack, body, command, logger):
    """command"""
    ack("EC2のステータスを確認します。")
    status.status_ec2(command["text"])
    logger.info(body)


@app.command("/getip")
def handle_some_command(ack, body, command, logger):
    """command"""
    ack("EC2のIPアドレスを取得します。")
    getip.get_ip(command["text"])
    logger.info(body)


@app.command("/fetchEC2")
def handle_some_command(ack, body, logger):
    """command"""
    ack("EC2のステータスを取得します。")
    fetch.ec2_info()
    logger.info(body)


SocketModeHandler(app, slack_app_token).start()
