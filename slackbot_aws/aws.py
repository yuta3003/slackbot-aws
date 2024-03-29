"""AWS
    EC2: EC2を操作するClass
"""

import boto3
import logger
import slack
from botocore.exceptions import ClientError


class EC2:
    """EC2を起動・停止する機能を提供する
    start: EC2を起動
    stop : EC2を停止
    status: EC2の状態を取得
    get_ec2_ip: EC2のIPアドレスを取得
    fetch_ec2_info: EC2の情報リストを取得
    """

    def __init__(self):
        self.__log = logger.Logger("EC2")

        self.__local_session = boto3.session.Session()
        self.slack = slack.Slack()
        self.post_channel = "aws"

    def start(self, instance_id, region_name):
        """起動

        :param instance_id:
        :param region_name:
        :return none:
        """
        ec2 = self.__create_ec2(instance_id, region_name)
        try:
            state_name = ec2.state["Name"]
        except AttributeError as error:
            self.__log.error(error)

        self.__log.debug(f"state is {state_name}")
        if state_name == "running":
            self.__log.info(f"ec2({instance_id}) is already started.")
            return
        if state_name == "stopped":
            self.__log.info(f"try start ec2({instance_id}).")
            post_message = {"text": f"EC2を起動します。 \nInstance ID: {instance_id}"}
            self.slack.post(self.post_channel, post_message)

            ec2.start()
            ec2.wait_until_running()

            self.__log.info(f"ec2({instance_id}) is started.")
            post_message = {
                "fields": [
                    {
                        "title": "Public IP Address",
                        "value": f"{ec2.network_interfaces_attribute[0]['Association']['PublicIp']}",
                        "short": "true",
                    },
                    {
                        "title": "Private IP Address",
                        "value": f"{ec2.network_interfaces_attribute[0]['PrivateIpAddresses'][0]['PrivateIpAddress']}",
                        "short": "true",
                    },
                ]
            }
            self.slack.post(self.post_channel, post_message)

    def stop(self, instance_id, region_name):
        """停止

        :param instance_id:
        :param region_name:
        :return none:
        """
        ec2 = self.__create_ec2(instance_id, region_name)
        try:
            state_name = ec2.state["Name"]
        except AttributeError as error:
            self.__log.error(error)

        self.__log.debug(f"state is {state_name}")
        if state_name == "stopped":
            self.__log.info(f"ec2({instance_id}) is already stopped.")
            return
        # elif state_name in {'pending', 'shutting-down', 'terminated', 'stopping'}:
        #     # raise NotSupportError('ec2(%s) is %s.' % (self.__instance_id, state_name))
        #     return
        if state_name == "running":
            self.__log.info(f"try stop ec2({instance_id}).")
            post_message = {"text": f"EC2を停止します。 \nInstance ID: {instance_id}"}
            self.slack.post(self.post_channel, post_message)

            ec2.stop()

            self.__log.info(f"ec2({instance_id}) is stopping.")
            self.slack.post(self.post_channel, "EC2を停止しました。")

    def status(self, instance_id, region_name):
        """statusを取得

        :param instance_id:
        :param region_name:
        :return none:
        """
        ec2 = self.__create_ec2(instance_id, region_name)
        try:
            state_name = ec2.state["Name"]
        except AttributeError as error:
            self.__log.error(error)

        self.__log.info(f"ec2({instance_id}) is {state_name}.")

        post_message = {"text": f"ec2({instance_id}) is {state_name}."}
        self.slack.post(self.post_channel, post_message)

    def get_ip(self, instance_id, region_name):
        """IP アドレスを取得

        :param instance_id:
        :param region_name:
        :return none:
        """
        ec2 = self.__create_ec2(instance_id, region_name)
        try:
            state_name = ec2.state["Name"]
        except AttributeError as error:
            self.__log.error(error)

        self.__log.debug(f"state is {state_name}")
        if state_name in {
            "pending",
            "shutting-down",
            "stopped",
            "terminated",
            "stopping",
        }:
            self.__log.info(f"ec2({instance_id}) is already stopped.")
            self.slack.post(self.post_channel, "EC2は起動していません。")
            return
        if state_name == "running":
            self.__log.info(
                f"ec2({instance_id})'s "
                "public ip address is "
                f"{ec2.network_interfaces_attribute[0]['Association']['PublicIp']}."
            )

            post_message = {
                "fields": [
                    {
                        "title": "Public IP Address",
                        "value": f"{ec2.network_interfaces_attribute[0]['Association']['PublicIp']}",
                        "short": "true",
                    },
                    {
                        "title": "Private IP Address",
                        "value": f"{ec2.network_interfaces_attribute[0]['PrivateIpAddresses'][0]['PrivateIpAddress']}",
                        "short": "true",
                    },
                ]
            }
            self.slack.post(self.post_channel, post_message)

    def __create_ec2(self, instance_id, region_name):
        """EC2を操作するオブジェクトを生成する

        :param instance_id:
        :param region_name:
        :return: EC2を操作するオブジェクト
        """
        ec2_resource = self.__local_session.resource(
            "ec2",
            region_name=region_name,
        )
        try:
            return ec2_resource.Instance(instance_id)
        except ClientError as error:
            self.__log.error(error)
            return None

    def fetch_ec2_info(self):
        """すべてのリージョンから作成されていEC2情報を取得

        :param none:
        :return:EC2情報リスト
        """
        answer_list = []

        available_regions = self.__local_session.get_available_regions("ec2")

        for region in available_regions:
            try:
                answer_dict = {}
                instances = []
                ec2 = boto3.client(
                    "ec2",
                    region_name=region,
                )
                ec2_data = ec2.describe_instances()
                for ec2_reservation in ec2_data["Reservations"]:
                    for ec2_instance in ec2_reservation["Instances"]:
                        if ec2_instance["InstanceId"]:
                            answer_dict["Region"] = region
                            answer_dict["Status"] = ec2_instance["State"]["Name"]
                            answer_dict["InstanceID"] = ec2_instance["InstanceId"]

                if answer_dict:
                    answer_list.append(answer_dict)
            except ClientError as error:
                print(f"{region}は有効になっていないリージョンです。スキップします。")

        post_message = {"text": f"ec2 list: {answer_list}"}
        self.slack.post(self.post_channel, post_message)
