"""
AWS 操作モジュール
"""
import os

import boto3
import logger

# import requests
from botocore.exceptions import ClientError

import slack


class EC2:
    """
    EC2を起動・停止する機能を提供する
    """

    def __init__(self, instance_id, region_name):
        """
        コンストラクタ
        :param instance_id: EC2のインスタンスID
        :param region_name: リージョン名
        """
        self.__log = logger.Logger("EC2")
        self.__instance_id = instance_id
        self.__local_session = boto3.session.Session(
            aws_access_key_id=os.environ["AccessKey"],
            aws_secret_access_key=os.environ["SecretAccessKey"],
            region_name=region_name,
        )
        self.slack = slack.Slack()
        self.post_channel = "aws"

    def start(self):
        """
        起動

        :param none:
        :return none:
        """
        ec2 = self.__create_ec2()
        try:
            state_name = ec2.state["Name"]
        except AttributeError as error:
            self.__log.error(error)

        self.__log.debug(f"state is {state_name}")
        if state_name == "running":
            self.__log.info(f"ec2({self.__instance_id}) is already started.")
            return
        # elif state_name in {'pending', 'shutting-down', 'terminated', 'stopping'}:
        #     return
        if state_name == "stopped":
            self.__log.info(f"try start ec2({self.__instance_id}).")
            self.slack.post(
                self.post_channel, f"EC2を起動します。 \nInstance ID: {self.__instance_id}"
            )

            ec2.start()
            ec2.wait_until_running()

            self.__log.info(f"ec2({self.__instance_id}) is started.")
            self.slack.post(
                self.post_channel,
                "Public IP Address: "
                f"{ec2.network_interfaces_attribute[0]['Association']['PublicIp']}"
                "\n"
                "Private IP Address: "
                f"{ec2.network_interfaces_attribute[0]['PrivateIpAddresses'][0]['PrivateIpAddress']}",
            )

    def stop(self):
        """
        停止

        :param none:
        :return none:
        """
        ec2 = self.__create_ec2()
        try:
            state_name = ec2.state["Name"]
        except AttributeError as error:
            # AttributeErrorは、昔あったインスタンスIDを使うと、（Pythonの）インスタンスは生成されるが、
            # 属性stateにアクセスできず例外が発生する
            self.__log.error(error)
            # raise NotFoundResource(e)

        self.__log.debug(f"state is {state_name}")
        if state_name == "stopped":
            self.__log.info(f"ec2({self.__instance_id}) is already stopped.")
            return
        # elif state_name in {'pending', 'shutting-down', 'terminated', 'stopping'}:
        #     # raise NotSupportError('ec2(%s) is %s.' % (self.__instance_id, state_name))
        #     return
        if state_name == "running":
            self.__log.info(f"try stop ec2({self.__instance_id}).")
            self.slack.post(
                self.post_channel, f"EC2を停止します。 \nInstance ID: {self.__instance_id}"
            )

            ec2.stop()

            self.__log.info(f"ec2({self.__instance_id}) is stopping.")
            self.slack.post(self.post_channel, "EC2を停止しました。")

    def status(self):
        """
        ステータス

        :param none:
        :return none:
        """
        ec2 = self.__create_ec2()
        try:
            state_name = ec2.state["Name"]
        except AttributeError as error:
            # AttributeErrorは、昔あったインスタンスIDを使うと、（Pythonの）インスタンスは生成されるが、
            # 属性stateにアクセスできず例外が発生する
            self.__log.error(error)
            # raise NotFoundResource(e)
        self.__log.info(f"ec2({self.__instance_id}) is {state_name}.")
        self.slack.post(
            self.post_channel, f"ec2({self.__instance_id}) is {state_name}."
        )

    def get_ec2_ip(self):
        """
        IP アドレスを取得

        :param none:
        :return none:
        """
        ec2 = self.__create_ec2()
        try:
            state_name = ec2.state["Name"]
        except AttributeError as error:
            # AttributeErrorは、昔あったインスタンスIDを使うと、（Pythonの）インスタンスは生成されるが、
            # 属性stateにアクセスできず例外が発生する
            self.__log.error(error)

        self.__log.debug(f"state is {state_name}")
        if state_name in {
            "pending",
            "shutting-down",
            "stopped",
            "terminated",
            "stopping",
        }:
            self.__log.info(f"ec2({self.__instance_id}) is already stopped.")
            self.slack.post(self.post_channel, "EC2は起動していません。")
            return
        if state_name == "running":
            self.__log.info(
                f"ec2({self.__instance_id})\'s "
                "public ip address is "
                f"{ec2.network_interfaces_attribute[0]['Association']['PublicIpi']}."
            )
            self.slack.post(
                self.post_channel,
                "Public IP Address: "
                f"{ec2.network_interfaces_attribute[0]['Association']['PublicIp']}"
                "\n"
                "Private IP Address: "
                f"{ec2.network_interfaces_attribute[0]['PrivateIpAddresses'][0]['PrivateIpAddress']}",
            )

    def __create_ec2(self):
        """
        EC2を操作するオブジェクトを生成する
        :return: EC2を操作するオブジェクト
        """
        self.__log.debug(f"ec2: {self.__instance_id}")
        ec2_resource = self.__local_session.resource("ec2")
        try:
            return ec2_resource.Instance(self.__instance_id)
        except ClientError as error:
            self.__log.error(error)
            return None
            # raise NotFoundResource(e)
