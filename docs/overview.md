# Overview

QHub HPC is a High-Performance Computing (HPC) deployment using [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/). In this document, we will discuss the services that run within this architecture and how they are interconnected. The setup follows a standard HPC configuration with a master/login node and 'N' worker nodes.

The master node serves as the central control and coordination hub for the entire cluster. It plays a pivotal role in managing and optimizing cluster resources and ensuring secure, efficient, and reliable operations. In contrast, worker nodes primarily focus on executing computational tasks and rely on instructions from the master node for job execution.

At a high level, the architecture comprises several key services: monitoring, the job scheduler ([Slurm](https://slurm.schedmd.com/overview.html)), and JupyterHub along with related Python services.

Important URLs:

- `https://<master node ip>/`: JupyterHub server
- `https://<master node ip>/monitoring/`: Grafana server
- `https://<master node ip>/auth/`: Keycloak server
- `https://<master node ip>/gateway/`: Dask-Gateway server for remote connections
- `ssh <master node ip> -p 8022`: SSH into a JupyterLab session for users (requires a JupyterHub token)

## Services (All Nodes)

- [node_exporter](https://github.com/prometheus/node_exporter): Collects node metrics (default port 9100)

## Master Node

### Services

#### Authentication

- [Keycloak](https://www.keycloak.org/): Provides enterprise-grade open-source authentication

#### Control and Coordination

- [Slurm](https://slurm.schedmd.com/overview.html): Manages job scheduling, resource allocation, and cluster control
- [slurmctld](https://slurm.schedmd.com/slurmctld.html): Manages the Slurm central management daemon
- [slurmdbd](https://slurm.schedmd.com/slurmdbd.html): Handles Slurm accounting
- [MySQL](https://www.mysql.com/): Acts as the database for Slurm accounting

#### Reverse Proxy and Routing

- [Traefik](https://traefik.io/): Serves as an open-source network proxy, routing network traffic efficiently

#### Monitoring and Metrics

- [Grafana](https://grafana.com/): Acts as a central place to view monitoring information (default port 3000)
- [Prometheus](https://prometheus.io/docs/introduction/overview/): Scrapes metrics (default port 9090)
- [slurm_exporter](https://github.com/vpenso/prometheus-slurm-exporter): Provides Slurm metrics (default port 9341)
- [Traefik exported metrics](https://doc.traefik.io/traefik/observability/metrics/overview/)
- [JupyterHub exported metrics](https://jupyterhub.readthedocs.io/en/stable/reference/metrics.html)

#### Python Ecosystem

- [JupyterHub](https://jupyter.org/hub): Provides scalable interactive computing (default port 8000)
- [Dask-Gateway](https://gateway.dask.org/): Enables scalable distributed computing
- [NFS server](https://en.wikipedia.org/wiki/Network_File_System): Facilitates sharing Conda environments and home directories among all users
- [conda-store](https://conda-store.readthedocs.io/en/latest/): Manages Conda environments within nodes

## Worker Nodes

Worker nodes primarily focus on executing computational tasks and have minimal dependencies, making them efficient for running parallel workloads. They rely on instructions from the master node for job execution and do not have the same level of control and coordination responsibilities as the master node. The master node's role is pivotal in orchestrating the overall cluster's functionality and ensuring efficient and secure operations.
