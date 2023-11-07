"""EC2を起動するモジュール
"""
import aws

def ec2():
    """start"""
    ec2 = aws.EC2()
    ec2.fetch_ec2_info()

if __name__ == "__main__":
    ec2(credential["EC2"])
