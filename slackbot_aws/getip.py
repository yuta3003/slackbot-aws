"""Public IP Addressを取得
"""
import aws


def get_ec2_ip(instance):
    """
    ec2のパブリックIPアドレスを取得します

    :param none:
    :return none:
    """
    instance_list = instance.split()
    instance_id = instance_list[0]
    region_name = instance_list[1]
    ec2 = aws.EC2()
    ec2.get_ip(instance_id=instance_id, region_name=region_name)
