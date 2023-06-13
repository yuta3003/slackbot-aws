import json
import aws


# jsonの読み込み処理
with open("credentials.json", "r", encoding="utf-8") as credentials:
    json = json.load(credentials)


def status_ec2(ec2_machines):
    if ec2_machines is None or len(ec2_machines) == 0:
        return
    for machine in ec2_machines:
        ec2 = aws.EC2(
            instance_id=machine["InstanceId"], region_name=machine["RegionName"]
        )
        ec2.status()


if __name__ == "__main__":
    status_ec2(json["EC2"])
