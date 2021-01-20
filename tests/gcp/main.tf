provider "google" {
}

resource "google_compute_network" "vpc_network" {
  name                    = "${var.name}-network"
  auto_create_subnetworks = "true"
}

resource "google_compute_firewall" "ssh-rule" {
  name = "${var.name}-ssh-port-22"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports = ["22"]
  }
  target_tags = [google_compute_instance.master-node.name]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_address" "vm_static_ip" {
  name = "${var.name}-static-ip"
}

resource "google_compute_instance" "master-node" {
  name   = "${var.name}-master"
  machine_type   = var.master-instance

  boot_disk {
    initialize_params {
      image = var.master-image
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.self_link
    access_config {
           nat_ip = google_compute_address.vm_static_ip.address
    }
  }
  
  metadata = {
    ssh-keys = "ubuntu:${file(var.ssh-public-key)}"
  }
  
  tags = concat([
    "qhub-onprem", "master"
  ], var.tags)
}

resource "google_compute_instance" "worker-nodes" {
  count = var.worker-count

  name   = "${var.name}-worker-${count.index}"
  machine_type   = var.worker-instance
  
  boot_disk {
    initialize_params {
      image = var.worker-image
    }
  }
  
  network_interface {
    network = google_compute_network.vpc_network.self_link
    access_config {
    }
  }

  metadata = {
    ssh-keys = "ubuntu:${file(var.ssh-public-key)}"
  }

  tags = concat([
    "qhub-onprem", "worker"
  ], var.tags)
}
