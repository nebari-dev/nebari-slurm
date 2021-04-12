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

resource "aws_vpc" "vpc_network" {
  cidr_block = var.ip_range

  tags = {
    Name = "${var.name}-network"
  }
}
