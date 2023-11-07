"""EC2を起動するモジュール
"""
import json

import aws

# jsonの読み込み処理
with open("credentials.json", "r", encoding="utf-8") as credentials:
    credential: dict[str, list] = json.load(credentials)


def start_ec2(ec2_machines: list, instance):
    """start"""
    instance_list = instance.split()
    instance_id = instance_list[0]
    region_name = instance_list[1]
    ec2 = aws.EC2()
    ec2.start(
        instance_id=instance_id, region_name=region_name
    )


if __name__ == "__main__":
    start_ec2(credential["EC2"])
