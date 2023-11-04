"""EC2を起動するモジュール
"""
import json

import aws

# jsonの読み込み処理
with open("credentials.json", "r", encoding="utf-8") as credentials:
    credential: dict[str, list] = json.load(credentials)


def start_ec2(ec2_machines: list):
    """start"""
    if ec2_machines is None or len(ec2_machines) == 0:
        return
    for machine in ec2_machines:
        ec2 = aws.EC2(
            instance_id=machine["InstanceId"], region_name=machine["RegionName"]
        )
        ec2.fetch_ec2_info()


if __name__ == "__main__":
    start_ec2(credential["EC2"])
