terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "vpc" {
  cidr_block        = var.cidr_block
  tags = {
    Name = "${var.name}_vpc"
  }
}

resource "aws_subnet" "subnet" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.subnet
  map_public_ip_on_launch = "true"
tags = {
    Name = "${var.name}_subnet"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    name = "${var.name}_gateway"
  }  
}

resource "aws_security_group" "ingress-all-test" {
name = "allow-all-sg"
vpc_id = aws_vpc.vpc.id
ingress {
    cidr_blocks = [
      "0.0.0.0/0"
    ]
from_port = 22
    to_port = 22
    protocol = "tcp"
  }
// Terraform removes the default rule
  egress {
   from_port = 0
   to_port = 0
   protocol = "-1"
   cidr_blocks = ["0.0.0.0/0"]
 }
}

resource "aws_default_route_table" "route_table" {
  default_route_table_id = aws_vpc.vpc.default_route_table_id
route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
}
  tags = {
    name = "${var.name}_route_table"
  }
}


resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDBxkRO5ArcW11LdLmdoDtVe0C+yll+SFmMgeswJ7UAnMEwvK3CU/4y6xuDUjC/xnLO85J6/z2gqoN5SMM5KPymV6UEn9nW3SZxYTS7yrmI6bGZbZFaKvQq8T5LMr3Le9y2Sw6B4CjyyFfcN29BWeubJBHnn2AxrM3JaieXFzBhoQcGNa4wz+5b+fqOZxbUrNjekv3vu/xsZMH0rBgVFkTXg39mSLfZnyj/XDyqC3cwnJjckQov4n7BzueOxbFciewZ8N256vItsWIxpg7wLdsSmY7S7THZ+eMEspPnOod1zSzg+tcKhS7iyEy0mSZGAHnK6LijRDyC50jHOHQ4FI+ct0NcNLeiX2LY8U29+Sp745msry7z/JruyCpWxA0apPBTAsQGrWa0StzzAm/VNXGBFF102gNuYDRbfdjHPu2PKGoJLPxOptRDZ9D3cTmi6KzTQlipoYn9N2KDSci4uCn3Wm9W7SEdeWJDiuTXlamldPjYpAQXE6VY9bwSOUIL+Dk= tyler@speider"
}


resource "aws_instance" "master-node" {
  tags = {
    name   = "${var.name}-master"
  }
  ami           = "ami-0a62a78cfedc09d76" # us-west-2 ubuntu 20.04 LTS
  instance_type = var.master-instance
  subnet_id     = aws_subnet.subnet.id
  key_name      = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.ingress-all-test.id]
}

resource "aws_instance" "worker-node" {
  count = var.worker-count
  tags = {
    name   = "${var.name}-worker-${count.index}"
  }
  ami           = "ami-0a62a78cfedc09d76" # us-west-2 ubuntu 20.04 LTS
  instance_type = var.worker-instance
  subnet_id     = aws_subnet.subnet.id
  key_name      = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.ingress-all-test.id]  
}


# resource "aws_eip" "master" {
#   instance = aws_instance.master-node.id
# }

# resource "aws_eip" "worker" {
#   count    = var.worker-count
#   instance = aws_instance.worker-node[count.index].id
# }
