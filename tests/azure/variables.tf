variable "name" {
  description = "Prefix name to assign to azure cloud resources"
  type        = string
  default     = "qhub-hpc-test"
}
variable "resource-location" {
  description = "azure location to deploy the resources"
  type        = string
  default     = "centralus"
}
variable "environment" {
  type        = string
  default     = "dev"
}
variable "vnet-address-space" {
  description = "Virtual network address space"
  type        = string
  default     = "10.0.0.0/16"
}
variable "subnet-1-address-prefix" {
  description = "Subnet address space"
  type    = string
  default = "10.0.0.0/24"
}
variable "whitelist_port" {
  description = "Port to whitelist for the master node"
  type        = list
  default     = ["22","8080"]
}
variable "master-machine-size" {
  description = "master node configuration"
  type    = string
  default = "Standard_F1"
}
variable "master-machine-username" {
  description = "master node admin username"
  type    = string
  default = "ubuntu"
}
variable "pub-file-path" {
  description = "Public key path for the azure vms"
  type    = string
  default = "./id_rsa.pub"
}
variable "ssh-private-key" {
  description = "Path to ssh private key for access to machines"
  type        = string
  default     = "./id_rsa"
}
variable "source-image-reference" {
  description = "OS related configuration"
  type        = list
  default     = ["Canonical","0001-com-ubuntu-server-focal","20_04-lts","latest"]
}
variable "os-disk-cache" {
  description = "The Type of Caching which should be used for the Internal OS Disk. Possible values are None, ReadOnly and ReadWrite"
  type        = string
  default     = "ReadWrite"
}
variable "os_disk_storage_account_type" {
  description = "Storage Account which should back this the Internal OS Disk. Possible values are Standard_LRS, StandardSSD_LRS and Premium_LRS"
  type        = string
  default     = "Standard_LRS"
}
variable "node-machine-size" {
  description = "worker node configuration"
  type        = string
  default     = "Standard_F1"
}
variable "node-machine-username" {
  description = "master node admin username"
  type        = string
  default     = "ubuntu"
}
variable "worker-count" {
  description = "Number of worker nodes to spawn"
  type        = string
  default     = 2
}
variable "os-disk-size" {
  description = "os disk size"
  type    = string
  default = "40"
}
