output "master-node-ip" {
  value = azurerm_linux_virtual_machine.master-node.public_ip_address
}

output "worker-node-ip" {
  value = azurerm_linux_virtual_machine.worker-nodes.*.private_ip_address
}
