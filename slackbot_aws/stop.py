"""EC2を停止するモジュール
"""
import aws


def stop_ec2(instance_id, region_name):
    """stop ec2"""
    ec2 = aws.EC2()
    ec2.stop(instance_id=instance_id, region_name=region_name)
