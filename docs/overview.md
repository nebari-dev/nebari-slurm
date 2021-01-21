# Overview

QHub OnPrem is a deployment of HPC with
[jupyterhub](https://jupyterhub.readthedocs.io/en/stable/) here we
talk about the services that run and how they are connected. The
architecture is based off of the typical hpc setup of a master/login
node with `N` worker nodes. The worker nodes are designed to have
minimal dependencies which most of the setup involves configuring the
master node. At a high level there are several services: monitoring,
the job scheduler ([slurm](https://slurm.schedmd.com/overview.html)),
and jupyterhub and related python services.

Important urls:
 - `<master node ip>:8000` jupyterhub server
 - `<master node ip>:3000` grafana server with username `admin` and password `admin`

## All Nodes

### Services

 - [node_exporter](https://github.com/prometheus/node_exporter) node metrics (default port 9100)

## Master Node

### Services

Monitoring
 - [grafana](https://grafana.com/) :: central place to view monitoring information (default port 3000)
 - [prometheus](https://prometheus.io/docs/introduction/overview/) :: metrics scraper (default port 9090)
 - [slurm_exporter](https://github.com/vpenso/prometheus-slurm-exporter) :: slurm metrics (default port 9341)

Slurm
 - [slurmctld](https://slurm.schedmd.com/slurmctld.html) :: slurm central management daemon
 - [slurmdbd](https://slurm.schedmd.com/slurmdbd.html) :: slurm accounting 
 - [mysql](https://www.mysql.com/) :: database for slurm accounting

Python Ecosystem
 - [jupyterhub](https://jupyter.org/hub) :: scalable interactive compute (default port 8000)
 - [nfs server](https://en.wikipedia.org/wiki/Network_File_System) for
   sharing conda environments and home directories between all users

## Worker Nodes

### Services

Slurm
 - [slurmd](https://slurm.schedmd.com/slurmd.html) :: slurm agent that runs on all worker nodes
