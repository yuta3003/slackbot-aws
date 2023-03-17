import boto3
import json
import logger
import os
import requests
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
        self.__log = logger.Logger('EC2')
        self.__instance_id = instance_id
        self.__local_session = boto3.session.Session(
            aws_access_key_id=os.environ["AccessKey"],
            aws_secret_access_key=os.environ["SecretAccessKey"],
            region_name=region_name
        )
        self.slack = slack.Slack()
        self.postChannel = 'aws'

    def start(self):
        """
        起動
        """
        ec2 = self.__create_ec2()
        try:
            state_name = ec2.state['Name']
        except AttributeError as e:
            self.__log.error(e)

        self.__log.debug('state is %s' % (state_name,))
        if state_name == 'running':
            self.__log.info('ec2(%s) is already started.' % (self.__instance_id,))
            return
        elif state_name in {'pending', 'shutting-down', 'terminated', 'stopping'}:
            return
        elif state_name == 'stopped':
            self.__log.info('try start ec2(%s).' % (self.__instance_id,))
            self.slack.post(
                self.postChannel,
                'EC2を起動します。 \nInstance ID: %s'
                % (self.__instance_id,))

            ec2.start()
            ec2.wait_until_running()

            self.__log.info('ec2(%s) is started.' % (self.__instance_id,))
            self.slack.post(
                self.postChannel,
                'Public IP Address: {}\nPrivate IP Address: {}'
                .format(
                    ec2.network_interfaces_attribute\
                        [0]\
                        ["Association"]\
                        ["PublicIp"],
                    ec2.network_interfaces_attribute\
                        [0]\
                        ["PrivateIpAddresses"]\
                        [0]\
                        ["PrivateIpAddress"]))

    def stop(self):
        """
        停止
        """
        ec2 = self.__create_ec2()
        try:
            state_name = ec2.state['Name']
        except AttributeError as e:
            # AttributeErrorは、昔あったインスタンスIDを使うと、（Pythonの）インスタンスは生成されるが、
            # 属性stateにアクセスできず例外が発生する
            self.__log.error(e)
            # raise NotFoundResource(e)

        self.__log.debug('state is %s' % (state_name,))
        if state_name == 'stopped':
            self.__log.info('ec2(%s) is already stopped.' % (self.__instance_id,))
            return
        elif state_name in {'pending', 'shutting-down', 'terminated', 'stopping'}:
            # raise NotSupportError('ec2(%s) is %s.' % (self.__instance_id, state_name))
            return
        elif state_name == 'running':

            self.__log.info('try stop ec2(%s).' % (self.__instance_id,))
            self.slack.post(
                self.postChannel,
                'EC2を停止します。 \nInstance ID: {}'
                .format(
                    self.__instance_id,))

            ec2.stop()

            self.__log.info('ec2(%s) is stopping.' % (self.__instance_id,))
            self.slack.post(
                self.postChannel,
                'EC2を停止しました。')

    def status(self):
        """
        ステータス
        """
        ec2 = self.__create_ec2()
        try:
            state_name = ec2.state['Name']
        except AttributeError as e:
            # AttributeErrorは、昔あったインスタンスIDを使うと、（Pythonの）インスタンスは生成されるが、
            # 属性stateにアクセスできず例外が発生する
            self.__log.error(e)
            # raise NotFoundResource(e)
        self.__log.info('ec2(%s) is %s.' % (self.__instance_id, state_name))
        self.slack.post(
            self.postChannel,
            'ec2({}) is {}.'
            .format(
                self.__instance_id,
                state_name))

    def get_ec2_ip(self):
        """
        IP アドレスを取得
        """
        ec2 = self.__create_ec2()
        try:
            state_name = ec2.state['Name']
        except AttributeError as e:
            # AttributeErrorは、昔あったインスタンスIDを使うと、（Pythonの）インスタンスは生成されるが、
            # 属性stateにアクセスできず例外が発生する
            self.__log.error(e)

        self.__log.debug('state is %s' % (state_name,))
        if state_name in {'pending', 'shutting-down', 'stopped','terminated', 'stopping'}:
            self.__log.info('ec2(%s) is already stopped.' % (self.__instance_id,))
            self.slack.post(
                self.postChannel,
                'EC2は起動していません。')
            return
        elif state_name == 'running':
            self.__log.info('ec2(%s)\'s public ip address is %s.' % (self.__instance_id, ec2.network_interfaces_attribute[0]["Association"]["PublicIp"]))
            self.slack.post(
                self.postChannel,
                'Public IP Address: {}\nPrivate IP Address: {}'
                .format(
                    ec2.network_interfaces_attribute\
                        [0]\
                        ["Association"]\
                        ["PublicIp"],
                    ec2.network_interfaces_attribute\
                        [0]\
                        ["PrivateIpAddresses"]\
                        [0]\
                        ["PrivateIpAddress"]))

    def __create_ec2(self):
        """
        EC2を操作するオブジェクトを生成する
        :return: EC2を操作するオブジェクト
        """
        self.__log.debug('ec2: %s' % (self.__instance_id,))
        ec2_resource = self.__local_session.resource('ec2')
        try:
            return ec2_resource.Instance(self.__instance_id)
        except ClientError as e:
            self.__log.error(e)
            # raise NotFoundResource(e)
