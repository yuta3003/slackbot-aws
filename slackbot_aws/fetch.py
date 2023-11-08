"""EC2を起動するモジュール
"""
import aws


def ec2_info():
    """start"""
    ec2 = aws.EC2()
    ec2.fetch_ec2_info()
