"""EC2のステータスを取得するモジュール
"""
import aws


def status_ec2(instance_id, region_name):
    """get status"""
    ec2 = aws.EC2()
    ec2.status(instance_id=instance_id, region_name=region_name)
