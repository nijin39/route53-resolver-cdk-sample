import json
import pytest

from aws_cdk import core
from dnsforward.dnsforward_stack import DnsforwardStack


def get_template():
    app = core.App()
    DnsforwardStack(app, "dnsforward")
    return json.dumps(app.synth().get_stack("dnsforward").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
