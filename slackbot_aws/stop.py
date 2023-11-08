"""EC2を停止するモジュール
"""
import aws


def stop_ec2(instance):
    """stop ec2"""
    instance_list = instance.split()
    instance_id = instance_list[0]
    region_name = instance_list[1]
    ec2 = aws.EC2()
    ec2.stop(instance_id=instance_id, region_name=region_name)
