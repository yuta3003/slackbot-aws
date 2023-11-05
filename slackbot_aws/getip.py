"""Public IP Addressを取得
"""
import json

import aws

# jsonの読み込み処理
with open("credentials.json", "r", encoding="utf-8") as credentials:
    credential: dict[str, list] = json.load(credentials)


def get_ip(ec2_machines: list, instance):
    """
    ec2のパブリックIPアドレスを取得します

    :param none:
    :return none:
    """
    instance_list = instance.split()
    instance_id = instance_list[0]
    region_name = instance_list[1]
    ec2 = aws.EC2()
    ec2.get_ec2_ip(
        instance_id=instance_id, region_name=region_name
    )


if __name__ == "__main__":
    get_ip(credential["EC2"])
