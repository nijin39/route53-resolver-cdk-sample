from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class DnsforwardStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc_ip: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        if vpc_ip:
            print("VPC_IP " + vpc_ip)
            cidr = vpc_ip
        else:
            cidr = "10.0.0.0/16"

        # 01. VPC 생성
        cfVpc = ec2.CfnVPC(
            self,
            "VPC",
            cidr_block = cidr,
            tags = [core.Tag(key="Name",value="CDKVPC")]
        )
        
        # 02. Subnet 생성
        subnet_2a = ec2.CfnSubnet(
            self,
            id="subnet_2a",
            availability_zone="ap-northeast-2a",
            cidr_block="100.0.1.0/24",
            map_public_ip_on_launch = True,
            vpc_id=cfVpc.ref,
            tags = [core.Tag(key="Name",value="subnet-2a")]
        )
        
        subnet_2c = ec2.CfnSubnet(
            self,
            id="subnet_2c",
            availability_zone="ap-northeast-2c",
            cidr_block="100.0.2.0/24",
            map_public_ip_on_launch = True,
            vpc_id=cfVpc.ref,
            tags = [core.Tag(key="Name",value="subnet-2c")]
        )
        
        # 03. SG 생성
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

        # 04. EC2 생성
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
                "key":"Name",
                "value":"dns_master"
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
                "key":"Name",
                "value":"dns_slave"
            }]
        )