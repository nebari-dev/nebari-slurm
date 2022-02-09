# Overview

QHub HPC is a deployment of HPC with
[jupyterhub](https://jupyterhub.readthedocs.io/en/stable/) here we
talk about the services that run and how they are connected. The
architecture is based off of the typical hpc setup of a master/login
node with `N` worker nodes. The worker nodes are designed to have
minimal dependencies which most of the setup involves configuring the
master node. At a high level there are several services: monitoring,
the job scheduler ([slurm](https://slurm.schedmd.com/overview.html)),
and jupyterhub and related python services.

Important urls:
 - `https://<master node ip>/` jupyterhub server
 - `https://<master node ip>/monitoring/` grafana server
 - `https://<master node ip>/auth/` keycloak server
 - `https://<master node ip>/gateway/` dask-gateway server for remote connection
 - `ssh <master node ip> -p 8022` to ssh into jupyterlab session for user (requires jupyterhub token)

## All Nodes

### Services

 - [node_exporter](https://github.com/prometheus/node_exporter) node metrics (default port 9100)

## Master Node

### Services

Authentication
 - [keycloak](https://www.keycloak.org/) for enterprise grade open source authentication

Reverse Proxy
 - [traefik](https://traefik.io/) open source network proxy

Monitoring
 - [grafana](https://grafana.com/) :: central place to view monitoring information (default port 3000)
 - [prometheus](https://prometheus.io/docs/introduction/overview/) :: metrics scraper (default port 9090)
 - [slurm_exporter](https://github.com/vpenso/prometheus-slurm-exporter) :: slurm metrics (default port 9341)
 - [Traefik exported metrics](https://doc.traefik.io/traefik/observability/metrics/overview/)
 - [JupyterHub exported metrics](https://jupyterhub.readthedocs.io/en/stable/reference/metrics.html)

Slurm
 - [slurmctld](https://slurm.schedmd.com/slurmctld.html) :: slurm central management daemon
 - [slurmdbd](https://slurm.schedmd.com/slurmdbd.html) :: slurm accounting 
 - [mysql](https://www.mysql.com/) :: database for slurm accounting

Python Ecosystem
 - [jupyterhub](https://jupyter.org/hub) :: scalable interactive compute (default port 8000)
 - [dask-gateway](https://gateway.dask.org/) :: scalable distributed computing
 - [nfs server](https://en.wikipedia.org/wiki/Network_File_System) for
   sharing conda environments and home directories between all users
 - [conda-store](https://conda-store.readthedocs.io/en/latest/) for
   managing conda environments within nodes

## Worker Nodes

### Services

Slurm
 - [slurmd](https://slurm.schedmd.com/slurmd.html) :: slurm agent that runs on all worker nodes
