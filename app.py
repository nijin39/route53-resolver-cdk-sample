#!/usr/bin/env python3

from aws_cdk import core

from dnsforward.dnsforward_stack import DnsforwardStack


app = core.App()
DnsforwardStack(app, "dnsforward", env={'region': 'ap-northeast-2'})

app.synth()
