from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class DnsforwardStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        cidr = "20.0.0.0/16"
        
        # vpc = ec2.Vpc(self, "VPC",
        #     cidr=cidr,
        #     max_azs=1
        #     # subnet_configuration=[ec2.SubnetConfiguration(
        #     #     cidr_mask=24,
        #     #     name="Application",
        #     #     subnet_type=ec2.SubnetType.PUBLIC
        #     #     ),
        #     #     ec2.SubnetConfiguration(
        #     #     cidr_mask=24,
        #     #     name="Application2",
        #     #     subnet_type=ec2.SubnetType.PUBLIC
        #     #     )
        #     # ]
        # )
        
        cfVpc = ec2.CfnVPC(
            self,
            "VPC",
            cidr_block = "20.0.0.0/16",
            tags = [core.Tag(key="Name",value="CDKVPC")]
        )
    
        
        subnet_2a = ec2.CfnSubnet(
            self,
            id="subnet_2a",
            availability_zone="ap-northeast-2a",
            cidr_block="20.0.1.0/24",
            map_public_ip_on_launch = True,
            vpc_id=cfVpc.ref,
            tags = [core.Tag(key="Name",value="subnet-2a")]
        )
        
        subnet_2c = ec2.CfnSubnet(
            self,
            id="subnet_2c",
            availability_zone="ap-northeast-2c",
            cidr_block="20.0.2.0/24",
            map_public_ip_on_launch = True,
            vpc_id=cfVpc.ref,
            tags = [core.Tag(key="Name",value="subnet-2c")]
        )
        
        # subnet_2c = ec2.Subnet(
        #     self,
        #     id="subnet_2c",
        #     availability_zone="ap-northeast-2c",
        #     cidr_block="20.0.2.0/24",
        #     vpc_id=vpc.vpc_id
        # )


    
        
        sg = ec2.CfnSecurityGroup(self,
                                 id="sg-ssh",
                                 vpc_id=cfVpc.ref,
                                 group_description="Default Group",
                                 tags = [core.Tag(key="Name",value="DNS_SG")])
                                 #security_group_ingress=[ingress_ssh])
                                 #security_group_egress=[egress_all])
                                 
        ingress_ssh = ec2.CfnSecurityGroupIngress(self,"SSH",ip_protocol="tcp",group_id=sg.ref,
                                              from_port=22,
                                              to_port=22,
                                              cidr_ip="0.0.0.0/0")

        egress_all = ec2.CfnSecurityGroupEgress(self,id="OUTBOUND",group_id=sg.ref,
                                                     ip_protocol="-1",
                                                     #from_port=0,
                                                     #to_port=65535,
                                                     cidr_ip="0.0.0.0/0")
        # security_group = ec2.SecurityGroup(
        #     self,
        #     id='test-security-group',
        #     vpc=(ec2.Vpc)(cfVpc),
        #     security_group_name='test-security-group'
        # )
        
        # security_group.add_ingress_rule(
        #     peer=ec2.Peer.ipv4(cidr),
        #     connection=ec2.Port.tcp(22),
        # )
        
        dns_server = ec2.MachineImage.generic_linux({
            "ap-northeast-2" : "ami-00d293396a942208d"
        })
        
        ec2.CfnInstance(
            self,
            id="dns_master",
            image_id = dns_server.get_image(self).image_id,
            instance_type = "t2.small",
            key_name = "SeoulRegion",
            security_group_ids = [sg.ref],
            subnet_id = subnet_2a.ref,
            tags = [{
                "key":"dns",
                "value":"master"
            }]
        )
        
        ec2.CfnInstance(
            self,
            id="dns_slave",
            image_id = dns_server.get_image(self).image_id,
            instance_type = "t2.small",
            key_name = "SeoulRegion",
            security_group_ids = [sg.ref],
            subnet_id = subnet_2c.ref,
            tags = [{
                "key":"dns",
                "value":"slave"
            }]
        )