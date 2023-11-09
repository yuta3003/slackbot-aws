"""EC2を起動するモジュール
"""
import aws


def start_ec2(instance_id, region_name):
    """start"""
    ec2 = aws.EC2()
    ec2.start(instance_id=instance_id, region_name=region_name)
