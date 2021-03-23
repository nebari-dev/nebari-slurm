provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name = "${var.name}-resource-group"
  location = var.resource-location
}

resource "azurerm_availability_set" "as" {
  name = "${var.name}-availablity-set"
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_virtual_network" "vnet" {
  name = "${var.name}-vnet"
  address_space = [ var.vnet-address-space ]
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags = {
    environment = var.environment
  }
}

resource "azurerm_network_security_group" "network-sg-1" {
   name                = "${var.name}-worker-network-sg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags = {
    environment = var.environment
  }
}

resource "azurerm_network_security_group" "network-sg-2" {
  name                = "${var.name}-master-network-sg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  tags = {
    environment = var.environment
  }
}

resource "azurerm_network_security_rule" "sg-rule-1" {
  count                       = "${length(var.whitelist_port)}"
  name                        = "sg-rule-${count.index}"
  priority                    = (100 + (count.index))
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "${element(var.whitelist_port, count.index)}"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.network-sg-2.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "${var.name}-subnet-1"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefix       = var.subnet-1-address-prefix
}

resource "azurerm_network_interface" "ni" {
  count = var.worker-count
  name                = "${var.name}-worker-network-interface-${count.index}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal-worker-${count.index}"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
  }
  tags = {
    environment = var.environment
  }
}

resource "azurerm_network_interface_security_group_association" "nsg-association" {
  count = var.worker-count
  network_interface_id      = element(azurerm_network_interface.ni.*.id, count.index)
  network_security_group_id = azurerm_network_security_group.network-sg-1.id
}

resource "azurerm_public_ip" "public-ip" {
  name                = "${var.name}-public-ip"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  allocation_method   = "Static"

  tags = {
    environment = var.environment
  }
}

resource "azurerm_network_interface" "ni-2" {
  name                = "${var.name}-master-network-interface"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal-master"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public-ip.id
  }
  tags = {
    environment = var.environment
  }
}

resource "azurerm_network_interface_security_group_association" "nsg-association-2" {
  network_interface_id      = azurerm_network_interface.ni-2.id
  network_security_group_id = azurerm_network_security_group.network-sg-2.id
}

resource "azurerm_linux_virtual_machine" "worker-nodes" {
  count = var.worker-count
  name                = "${var.name}-worker-node-${count.index}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = var.node-machine-size
  admin_username      = var.node-machine-username
  network_interface_ids = [
    element(azurerm_network_interface.ni.*.id, count.index)
  ]

  admin_ssh_key {
    username   = var.node-machine-username
    public_key = file(var.pub-file-path)
  }
  source_image_reference {
    publisher = var.source-image-reference[0]
    offer     = var.source-image-reference[1]
    sku       = var.source-image-reference[2]
    version   = var.source-image-reference[3]
  }
  os_disk {
    caching              = var.os-disk-cache
    storage_account_type = var.os_disk_storage_account_type
    disk_size_gb         = var.os-disk-size
  }

  tags = {
    environment = var.environment
  }
}

resource "azurerm_linux_virtual_machine" "master-node" {

  name                = "${var.name}-master-node"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = var.master-machine-size
  admin_username      = var.master-machine-username
  network_interface_ids = [
    azurerm_network_interface.ni-2.id,
  ]


  admin_ssh_key {
    username   = var.master-machine-username
    public_key = file(var.pub-file-path)
  }
  source_image_reference {
    publisher = var.source-image-reference[0]
    offer     = var.source-image-reference[1]
    sku       = var.source-image-reference[2]
    version   = var.source-image-reference[3]
  }
  os_disk {
    caching              = var.os-disk-cache
    storage_account_type = var.os_disk_storage_account_type
    disk_size_gb         = var.os-disk-size
  }

  tags = {
    environment = var.environment
  }
}

resource "local_file" "ansible_inventory" {
  content = <<-EOT
  # autogenerated by terraform
  all:
    hosts:
      ${azurerm_linux_virtual_machine.master-node.name}:
        ansible_host: ${azurerm_linux_virtual_machine.master-node.public_ip_address} 
        ansible_user: ubuntu
        ansible_ssh_private_key_file: ${var.ssh-private-key}
      ${join("\n    ", formatlist("%s:\n      ansible_host: %s\n      ansible_user: ubuntu\n      ansible_ssh_private_key_file: ${var.ssh-private-key}\n      ansible_ssh_common_args: '-o ProxyCommand=\"ssh -i id_rsa -W %%h:%%p -q ubuntu@${azurerm_linux_virtual_machine.master-node.public_ip_address}\"'", azurerm_linux_virtual_machine.worker-nodes.*.name, azurerm_linux_virtual_machine.worker-nodes.*.private_ip_address))}
    children:
      hpc-master:
        hosts:
          ${azurerm_linux_virtual_machine.master-node.name}:
      hpc-worker:
        hosts:
          ${join("\n        ", formatlist("%s:", azurerm_linux_virtual_machine.worker-nodes.*.name))}
  EOT

  filename = "inventory"
}
