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

variable "zone" {
  description = "Region to deploy digital ocean resources"
  type        = string
  default     = "us-central1"
}

variable "ip_range" {
  description = "Range of ip addresses to assign to compute nodes"
  type        = string
  default     = "10.10.10.0/24"
}

variable "master-image" {
  description = "Image to use for digital ocean deployment for hpc master"
  type        = string
  default     = "ubuntu-2004-lts"
}

variable "master-instance" {
  description = "Compute instance to use for digital ocean deployment for hpc master"
  type        = string
  default     = "c2-standard-4"
}

variable "worker-image" {
  description = "Image to use for digital ocean deployment for hpc workers"
  type        = string
  default     = "ubuntu-2004-lts"
}

variable "worker-instance" {
  description = "Compute instance to use for digital ocean deployment for hpc workers"
  type        = string
  default     = "c2-standard-4"
}

variable "worker-count" {
  description = "Number of worker nodes to spawn"
  type        = string
  default     = 2
}
