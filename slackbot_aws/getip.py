import json
import aws


# jsonの読み込み処理
with open('credentials.json', 'r', encoding="utf-8") as credentials:
    json = json.load(credentials)


def get_ip(ec2_machines):
    if ec2_machines is None or len(ec2_machines) == 0:
        return
    for machine in ec2_machines:
        ec2 = aws.EC2(
            instance_id=machine['InstanceId'],
            region_name=machine['RegionName']
        )
        ec2.get_ec2_ip()

if __name__ == '__main__':
    get_ip(json['EC2'])
