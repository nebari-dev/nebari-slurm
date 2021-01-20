output "internal-master-ip" {
 value = google_compute_instance.master-node.network_interface.0.access_config.0.nat_ip
}

output "internal-worker-ip" {
 value = google_compute_instance.worker-nodes.*.network_interface.0.access_config.0.nat_ip
}
