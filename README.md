**EXPERIMENTAL** Note that QHub-hpc is currently experimental

# qhub-hpc

QHub HPC is an opinionated open source deployment of
[jupyterhub](https://jupyterhub.readthedocs.io/en/stable/) on on-prem
resources. QHub-hpc is a "distribution" of these
packages much like [Debian](https://www.debian.org/) and
[Ubuntu](https://ubuntu.com/) are distributions of
[Linux](https://en.wikipedia.org/wiki/Linux). The high level goal of
this distribution is to form a cohesive set of tools that enable:
 - environment management via [conda](https://docs.conda.io/en/latest/) and [conda-store](https://github.com/Quansight/conda-store)
 - monitoring of compute infrastructure and services
 - scalable and efficient compute via
   [jupyterlab](https://jupyterlab.readthedocs.io/en/stable/) and
   [dask](https://dask.org/)
 - deployment of jupyterhub on prem without requiring deep devops
   knowledge of the hpc and jupyter ecosystem

# Dependencies

 - [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
 - [vagrant](https://www.vagrantup.com/docs/installation) for testing

Install ansible dependencies

```shell
ansible-galaxy collection install -r requirements.yaml
```

# Testing

Vagrant is a tool responsible for creating and provisioning vms. It
has convenient integration with ansible which allows for easy
effective control over configuration. Currently the `Vagrantfile` only
has support for `libvirt`.

```shell
cd tests
vagrant up --provider=<provider-name>
```

Notebook for testing functionality
 - `tests/assets/notebook/test-dask-gateway.ipynb`

# Services

Current testing environment spins up four nodes:
 - all nodes :: node_exporter for node metrics
 - master node :: slurm scheduler, munge, mysql, jupyterhub, grafana, prometheus
 - worker node :: slurm daemon, munge
 
## Jupyterhub

Jupyterhub is accessible via `<master node ip>:8000`

## Grafana

Grafana is accessible via `<master node ip>:3000`

# License

[QHub-hpc is BSD3 licensed](LICENSE).


# Contributing

Contributions are welcome!
