# Qhub and QHub-HPC Comparison

At a high level QHub is focused on a Kubernetes and container based
deployment of all of its components. Many of the advantages of a
container based deployment allow for better security, scalability of
components and compute nodes.

QHub-HPC is focused on bringing many of the same features but within a
bare metal installation allowing users to fully take advantage of
their hardware for performance. Additionally these installations tend
to be easier to manage and debug when issues arise (traditional linux
sys-admin experience works well here). Due to this approach QHub-HPC
lacks containers but achieves workflows and scheduling of compute via
[Slurm](https://slurm.schedmd.com/documentation.html) and keeping
[services
available](https://www.freedesktop.org/wiki/Software/systemd/).

Questions to help determine which solution may be best for you:

1. Are you deploying to the cloud e.g. AWS, GCP, Azure, or Digital Ocean?

QHub is likely your best option. The auto-scalability of QHub compute
allows for cost effective usage of the cloud while taking advantage of
a managed Kubernetes.

2. Are you deploying to a bare metal cluster?

QHub-HPC may be your best option since deployment does not require the
complexity of managing a kubernetes cluster. If you do have a devops
or IT team to help manage kubernetes on bare metal QHub could be a
great option. But be advised that managing Kubenetes comes with quite
a lot of complexity which the cloud providers handle for us.

3. Are you concerned about absolute best performance?

QHub-HPC is likely your best option. But note when we say absolute
performance we mean your software is able to fully take advantage of
your networks Infiniband hardware, uses MPI, and SIMD
instructions. Few users fall into this camp and should rarely be a
reason to chose QHub-HPC (unless you know why you are making this
choice).

# Feature Matrix

| Core                                             | QHub                                | QHub-HPC          |
|--------------------------------------------------|-------------------------------------|-------------------|
| Scheduler                                        | Kubernetes                          | SystemD and Slurm |
| User Isolation                                   | Containers (cgroups and namespaces) | Slurm (cgroups)   |
| Auto-scaling compute nodes                       | X                                   |                   |
| Cost efficient compute support (Spot/Premptible) | X                                   |                   |
| Static compute nodes                             |                                     | X                 |

| User Services                      | QHub | QHub-HPC |
|------------------------------------|------|----------|
| Dask Gateway                       | X    | X        |
| JupyterHub                         | X    | X        |
| JupyterHub-ssh                     | X    | X        |
| CDSDashboards                      | X    | X        |
| Conda-Store environment management | X    | X        |
| ipyparallel                        |      | X        |
| Native MPI support                 |      | X        |

| Core Services                                                 | QHub | QHub-HPC |
|---------------------------------------------------------------|------|----------|
| Monitoring via Grafana and Prometheus                         | X    | X        |
| Auth integration (OAuth2, OpenID, ldap, kerberos)             | X    | X        |
| Role based authorization on JupyterHub, Grafana, Dask-Gateway | X    | X        |
| Configurable user groups                                      | X    | X        |
| Shared folders for each user's group                          | X    | X        |
| Traefik proxy                                                 | X    | X        |
| Automated Let's Encrypt and manual TLS certificates           | X    | X        |
| Forward authentication ensuring all endpoints authenticated   | X    |          |
| Backups via Restic                                            |      | X        |

| Integrations | QHub | QHub-HPC |
|--------------|------|----------|
| ClearML      | X    |          |
| Prefect      | X    |          |
| Bodo         |      | X        |
