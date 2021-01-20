provider "digitalocean" {

}

resource "digitalocean_ssh_key" "main" {
  name       = "${var.name}-ssh-key"
  public_key = file(var.ssh-public-key)
}

resource "digitalocean_vpc" "main" {
  name   = "${var.name}-network"
  region = var.region
}

resource "digitalocean_droplet" "master-node" {
  name   = "${var.name}-master"
  image  = var.master-image
  size   = var.worker-instance
  region = var.region
  vpc_uuid = digitalocean_vpc.main.id

  ssh_keys = [digitalocean_ssh_key.main.fingerprint]

  tags = concat([
    "qhub-hpc", "master"
  ], var.tags)
}

resource "digitalocean_droplet" "worker-nodes" {
  count = 3

  name   = "${var.name}-worker-${count.index}"
  image  = var.worker-image
  size   = var.worker-instance
  region = var.region
  vpc_uuid = digitalocean_vpc.main.id

  ssh_keys = [digitalocean_ssh_key.main.fingerprint]

  tags = concat([
    "qhub-hpc", "worker"
  ], var.tags)
}
