variable "name" {
  description = "Prefix name to assign to digital ocean resources"
  type        = string
  default     = "qhub-hpc-test"
}

variable "ssh-public-key" {
  description = "Path to ssh public key for access to machines"
  type        = string
  default    = "./id_rsa.pub"
}

variable "tags" {
  description = "Additional tags to apply to resources"
  type        = list(string)
  default     = ["test"]
}

variable "region" {
  description = "Region to deploy digital ocean resources"
  type        = string
  default     = "nyc1"
}

variable "ip_range" {
  description = "Range of ip addresses to assign to compute nodes"
  type        = string
  default     = "10.10.10.0/24"
}

variable "master-image" {
  description = "Image to use for digital ocean deployment for hpc master"
  type        = string
  default     = "ubuntu-20-04-x64"
}

variable "master-instance" {
  description = "Compute instance to use for digital ocean deployment for hpc master"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "worker-image" {
  description = "Image to use for digital ocean deployment for hpc workers"
  type        = string
  default     = "ubuntu-20-04-x64"
}

variable "worker-instance" {
  description = "Compute instance to use for digital ocean deployment for hpc workers"
  type        = string
  default     = "s-4vcpu-8gb"
}

variable "worker-count" {
  description = "Number of worker nodes to spawn"
  type        = string
  default     = 2
}
