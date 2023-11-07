"""EC2を起動するモジュール
"""
import json

import aws

# jsonの読み込み処理
with open("credentials.json", "r", encoding="utf-8") as credentials:
    credential: dict[str, list] = json.load(credentials)


def fetch_ec2(ec2_machines: list):
    """start"""
    ec2 = aws.EC2()
    ec2.fetch_ec2_info()


if __name__ == "__main__":
    fetch_ec2(credential["EC2"])
