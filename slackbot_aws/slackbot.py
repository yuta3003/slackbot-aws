"""slackbotのスラッシュコマンド用モジュール
"""
import os

import aws
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_app_token = os.environ["SLACK_APP_TOKEN"]

app = App(token=slack_bot_token)


@app.command("/run")
def handle_some_command(ack, body, command, logger):
    """command"""
    ack("EC2が起動します。")
    instance_id, region_name = command["text"].split()
    ec2 = aws.EC2()
    ec2.start(instance_id=instance_id, region_name=region_name)
    logger.info(body)


@app.command("/stop")
def handle_some_command(ack, body, command, logger):
    """command"""
    ack("EC2が停止します。")
    instance_id, region_name = command["text"].split()
    ec2 = aws.EC2()
    ec2.stop(instance_id=instance_id, region_name=region_name)
    logger.info(body)


@app.command("/state")
def handle_some_command(ack, body, command, logger):
    """command"""
    ack("EC2のステータスを確認します。")
    instance_id, region_name = command["text"].split()
    ec2 = aws.EC2()
    ec2.status(instance_id=instance_id, region_name=region_name)
    logger.info(body)


@app.command("/getip")
def handle_some_command(ack, body, command, logger):
    """command"""
    ack("EC2のIPアドレスを取得します。")
    instance_id, region_name = command["text"].split()
    ec2 = aws.EC2()
    ec2.get_ip(instance_id=instance_id, region_name=region_name)
    logger.info(body)


@app.command("/fetchEC2")
def handle_some_command(ack, body, logger):
    """command"""
    ack("EC2のステータスを取得します。")
    ec2 = aws.EC2()
    ec2.fetch_ec2_info()
    logger.info(body)


SocketModeHandler(app, slack_app_token).start()
