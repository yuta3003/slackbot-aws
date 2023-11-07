"""EC2を起動するモジュール
"""
import aws

def start_ec2(instance):
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
