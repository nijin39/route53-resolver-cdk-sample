from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class DnsforwardStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        vpc = ec2.Vpc(self, "VPC",
            cidr="10.0.0.0/21",
            max_azs=3,
            subnet_configuration=[ec2.SubnetConfiguration(
                cidr_mask=24,
                name="Application",
                subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                cidr_mask=24,
                name="Application2",
                subnet_type=ec2.SubnetType.PUBLIC
                )
            ]
        )

        security_group = ec2.SecurityGroup(
            self,
            id='test-security-group',
            vpc=vpc,
            security_group_name='test-security-group'
        )
        
        security_group = ec2.SecurityGroup(
            self,
            id='test-security-group',
            vpc=vpc,
            security_group_name='test-security-group'
        )