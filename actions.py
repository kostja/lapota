#!/usr/bin/env python3
from abc import abstractmethod
import boto3
import subprocess
from pprint import pprint

registry = {}

def register(name, description):
    """Register the action in the action registry with the given name"""
    def decorator(Cls):
        Cls.name = name
        Cls.description = description
        registry[name] = Cls
        return Cls
    return decorator


def ami_by_name(name):
    client = boto3.client("ec2")
    response = client.describe_images(Filters = [
        {
            "Name": "name",
            "Values": [name],
        }
    ])
    return response["Images"][0]["ImageId"]


def instances_by_tag(tag):
    client = boto3.client("ec2")
    response = client.describe_instances(
        Filters=
        [
            {
                "Name": "tag:trawsers",
                "Values": [ tag ]
            },
            {
                "Name": "instance-state-name",
                "Values": ["pending", "running", "shutting-down", "stopping", "stopped"]
            },

        ],
    )
    if len(response["Reservations"]) > 0:
        return [instance["InstanceId"] for instance in response["Reservations"][0]["Instances"]]
    else:
        return []


class Action:

    @classmethod
    def setup_argparse(Cls, parsers):
        pass


@register("list", "List existing AWS instances")
class ListInstances(Action):

    def func(self, args):
        ec2 = boto3.resource("ec2")
        for instance in ec2.instances.all():
            print(instance.id, instance.state)


@register("ami", "Build AMI instances for benchmark client and server")
class BuildAMI(Action):
    def func(self, args):
        client = boto3.client("ec2")
        response = client.describe_images(Filters = [
            {
                "Name": "name",
                "Values": ["trawsers-*"],
            }
        ])
        built_images = { image["Name"]: image for image in response["Images"] }

        images = {
            "trawsers-scylla": "resource/packer/scylla.json",
            "trawsers-stress": "resource/packer/stress.json",
        }

        for key in images:
            if key not in built_images:
                subprocess.run(["packer", "build", images[key]])
            else:
                print("Reusing an existing image {} for {}".format(
                    built_images[key]["ImageId"], key))


@register("boot", "Boot AMI instances")
class BootInstances(Action):

    def func(self, args):
        instances = instances_by_tag("scylla")
        if len(instances) == 0:
            tag = {"Key": "trawsers", "Value": "scylla"}
            ec2 = boto3.resource("ec2")
            instances = ec2.create_instances(
                ImageId=ami_by_name("trawsers-scylla"),
                KeyName="kostja",
                MinCount=3,
                MaxCount=3,
                InstanceType="i3.8xlarge",
                TagSpecifications=[{'ResourceType': 'instance', 'Tags': [tag]}])
            pprint(instances)
        else:
            client = boto3.client("ec2")
            instances = client.start_instances(InstanceIds=instances)
            pprint(instances)


@register("halt", "Shutdown AMI instances")
class ShutdownInstances(Action):

    def func(self, args):
        instances = instances_by_tag("scylla")
        ec2 = boto3.resource("ec2")
        response = ec2.instances.filter(InstanceIds=instances).stop()
        pprint(response)

@register("keys", "Show existing key pairs")
class ShutdownInstances(Action):

    def func(self, args):
        client = boto3.client("ec2")
        response = client.describe_key_pairs()
        pprint(response)
