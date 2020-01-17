#!/usr/bin/env python3
from abc import abstractmethod
import boto3
import subprocess

registry = {}

def register(name, description):
    """Register the action in the action registry with the given name"""
    def decorator(Cls):
        Cls.name = name
        Cls.description = description
        registry[name] = Cls
        return Cls
    return decorator


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
        pass
