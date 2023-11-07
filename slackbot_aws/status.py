"""EC2のステータスを取得するモジュール
"""
import aws

def status_ec2(instance):
    """get status"""
    instance_list = instance.split()
    instance_id = instance_list[0]
    region_name = instance_list[1]
    ec2 = aws.EC2()
    ec2.status(
        instance_id=instance_id, region_name=region_name
    )

if __name__ == "__main__":
    status_ec2(credential["EC2"])
