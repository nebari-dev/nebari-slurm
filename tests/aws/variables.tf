variable "name" {
  description = "Prefix name to assign to aws resources"
  type        = string
  default     = "qhub-hpc-test"
}

variable "ssh-public-key" {
  description = "Path to ssh public key for access to machines"
  type        = string
  default    = "./id_rsa.pub"
}

variable "ssh-private-key" {
  description = "Path to ssh private key for access to machines"
  type        = string
  default    = "./id_rsa"
}

variable "tags" {
  description = "Additional tags to apply to resources"
  type        = list(string)
  default     = ["test"]
}

variable "zone" {
  description = "Region to deploy aws resources"
  type        = string
  default     = "us-west-2"
}

variable "availability-zone" {
  description = "Availability zone to deploy aws resources"
  type        = string
  default     = "us-west-2a"
}

variable "subnet" {
  description = "Range of ip addresses to assign to compute nodes"
  type        = string
  default     = "192.168.0.0/24"
}

variable "cidr_block" {
  default = "192.168.0.0/16"
}

variable "master-image" {
  description = "Image to use for aws deployment for hpc master"
  type        = string
  default     = "ubuntu-2004-lts"
}

variable "master-instance" {
  description = "Compute instance to use for aws deployment for hpc master"
  type        = string
  default     = "c5.18xlarge"
}

variable "worker-image" {
  description = "Image to use for aws deployment for hpc workers"
  type        = string
  default     = "ubuntu-2004-lts"
}

variable "worker-instance" {
  description = "Compute instance to use for aws deployment for hpc workers"
  type        = string
  default     = "c5.18xlarge"
}

variable "disk-size" {
  description = "Size of boot drive instance uses"
  type        = string
  default     = 100
}

variable "disk-type" {
  description = "Disk type compute instance uses"
  type        = string
  default     = "pd-ssd"
}

variable "worker-count" {
  description = "Number of worker nodes to spawn"
  type        = string
  default     = 16
}
