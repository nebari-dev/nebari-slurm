output "public-master-node-ip" {
  description = "ip address of master node"
  value       = digitalocean_droplet.master-node.ipv4_address
}

output "private-master-node-ip" {
  description = "ip address of master node"
  value       = digitalocean_droplet.master-node.ipv4_address_private
}

output "public-worker-node-ip" {
  description = "ip addresses of worker nodes"
  value       = digitalocean_droplet.worker-nodes.*.ipv4_address
}

output "private-worker-node-ip" {
  description = "ip addresses of worker nodes"
  value       = digitalocean_droplet.worker-nodes.*.ipv4_address_private
}

output "ssh-key" {
  description = "ssh private key location"
  value       = var.ssh-private-key-name
}
