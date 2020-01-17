#!/usr/bin/env python3
import boto3
from abc import abstractmethod

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

