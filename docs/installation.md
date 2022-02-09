# Requirements

QHub-HPC currently requires ubuntu bare metal machines. There are
plans to support additional OSs such as RHEL. We actively test on the
latest stable Ubuntu release. We require:
 - 1 main node with at least 4 cpus and 16 GB of RAM
 - 0-N worker nodes (main node can be a worker node but is not
   recommended) with no significant requirements on resources

Must be able to ssh into each node from the node you are running the
ansible commands and connect via root (not recommended) or user and
sudo with or without a password.

# Dependencies

We recommend installing ansible via conda. First you must [install
conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

```shell
conda create -n qhub-hpc -c conda-forge ansible
conda activate qhub-hpc
```

If you do not want to use conda follow the [Ansible installation
instructions](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).

# Installation

Prior to the `0.4` release each QHub-HPC deployment required
maintaining a fork and rebasing all the changes to QHub-HPC within the
`main` branch. Now we strive to maintain the variables within the
QHub-HPC roles.

## Copy the template

In this example we create our own deployment `my-deployment` and
create a managed git repository for our deployment. You will want to
substitute this name.

```shell
git clone https://github.com/Quansight/qhub-hpc /tmp/qhub-hpc

mkdir my-deployment
cd my-deployment
git init

cp -r /tmp/qhub-hpc/inventory.template/* .
```

This will initialize the directory with:
 - `inventory` which is an [ansible inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)
 - `host_vars` is a collection of host specific variables within the hosts
 - `group_vars` is a collection of group specific variables within the hosts

Over time you may add additional directories and files to the
repository.

## Modify the ansible inventory

Below is an example ansible inventory file used for
`ansible-playbook`. There are [great docs on modifying the ansible
inventory
file](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html). The important keys to set:
  - `ansible_host` which is the DNS accessible name
  - `ansible_port` default is `22`
  - `ansible_user` which is the username to login into node by default is the user that the `ansible-playbook` command is run as
  - `ansible_ssh_private_key_file` is the path to the ssh key to login to node

Next you must configure the groups. In this case the `hpc-master` and
`hpc-worker` groups. There must only be one node in the `hpc-master`
group. `N` nodes can be in the `hpc-worker` section (including the
hpc-master node which is not recommended).

```
hpc02-test ansible_host=192.168.121.124 ansible_port=22 ansible_user='vagrant' ansible_ssh_private_key_file='/home/costrouc/.vagrant.d/insecure_private_key'
hpc03-test ansible_host=192.168.121.176 ansible_port=22 ansible_user='vagrant' ansible_ssh_private_key_file='/home/costrouc/.vagrant.d/insecure_private_key'
hpc04-test ansible_host=192.168.121.133 ansible_port=22 ansible_user='vagrant' ansible_ssh_private_key_file='/home/costrouc/.vagrant.d/insecure_private_key'
hpc01-test ansible_host=192.168.121.35 ansible_port=22 ansible_user='vagrant' ansible_ssh_private_key_file='/home/costrouc/.vagrant.d/insecure_private_key'

[hpc-master]
hpc01-test

[hpc-worker]
hpc02-test
hpc03-test
hpc04-test

[partition-example]
hpc02-test
hpc04-test
```

Arbitrary additional groups with name `partition-<name>` may be added
to create additional slurm partition groups of name `<name>`. This can
be useful if you want a Slurm partition for on the gpu or high memory
nodes.

# host_vars

If you would like to set specific variables for a given host you must
create a file in `host_vars/<host-name>.yaml`. Currently we only
recommend a few variables be set on the host_vars. This is the slurm
resources for each node. E.g. the following.

```yaml
slurm_memory: 16000
slurm_cpus: 4
slurm_sockets_per_board: 4
```

This however is difficult to correctly set see the section
"Configuring and adding node information" in [slurm.md](./slurm.md). A
hosts file should be created for each node in the `hpc-worker`
group. In the inventory example above the following files would exist:

 - `host_vars/hpc02-test.md`
 - `host_vars/hpc03-test.md`
 - `host_vars/hpc04-test.md`

It is okay to get the memory and cpus wrong. This can later be
corrected on a re-deployment.

# group_vars

Most if not all configuration will be done in the `group_vars`
directory. Within that directory there are three groups:
 - `all.yaml` which are variables set for all nodes
 - `hpc-master.yaml` which are variables set for the hpc master node
 - `hpc-worker.yaml` which are variables set for the hpc worker nodes

Detailed information on customizing the configuration should see the
[configuration](./configuration.md).

# Deployment

After any modifications to the `host_vars/*`, `group_vars/*`, or
`inventory` an Ansible deployment should be performed. QHub-HPC has
intentionally followed a normal Ansible deployment pattern to allow
for reusing the amazing tutorials and documentation currently in place
around Ansible.

```shell
cd my-deployment
ansible-playbook -i inventory /tmp/qhub-hpc/playbook.yaml
```

# Checking the status of the deployment

Upon successful deployment you should be able to visit the
`https://<hpc-master>/` where `<hpc-master>` is the ip address or dns
name of your specific deployment. You will be prompted by the
jupyterhub landing page.
