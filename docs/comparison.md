# Qhub and QHub-HPC Comparison

At a high level QHub is focused on a Kubernetes and container based
deployment of all of its components. Many of the advantages of a
container based deployment allow for better scalability of components
and compute nodes.

QHub-HPC is focused on bringing many of the same features but within a
bare metal installation allowing users to fully take advantage of
their hardware. Due to this approach QHub-HPC lacks containers but
achieves workflows and scheduling of compute via
[Slurm](https://slurm.schedmd.com/documentation.html) and keeping
[services available](https://www.freedesktop.org/wiki/Software/systemd/).

# Feature Matrix

| Core                                             | QHub       | QHub-HPC              |
|--------------------------------------------------|------------|-----------------------|
| Scheduler                                        | Kubernetes | SystemD and Slurm     |
| User Isolation                                   | Containers | Slurm managed cgroups |
| Auto-scaling compute nodes                       | X          |                       |
| Cost efficient compute support (Spot/Premptible) | X          |                       |
| Static compute nodes                             |            | X                     |

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
