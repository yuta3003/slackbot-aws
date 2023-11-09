"""Public IP Addressを取得
"""
import aws


def get_ec2_ip(instance_id, region_name):
    """
    ec2のパブリックIPアドレスを取得します

    :param none:
    :return none:
    """
    ec2 = aws.EC2()
    ec2.get_ip(instance_id=instance_id, region_name=region_name)
