# Development Guide

Welcome to the QHub HPC development guide! This guide will help you set up your development environment and tools for working with QHub HPC using Vagrant to orchestrated the virtual machines (VMs) and Ansible to provision the necessary infrastructure.

## Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

- Vagrant: Vagrant is a tool for building and managing virtual machine environments. Install the latest version for your operating system.

- Virtualization Provider: Depending on your preference, choose either Libvirt or VirtualBox as your virtualization provider.

- Git: Git is a version control system. You'll need it to clone the QHub HPC repository.

Let's get started!

## Additional Development Tasks

It is recommended to use a personal environment for development. This will allow you to install additional packages and tools without affecting your system's global environment. We recommend using Conda to create a personal environment but you could use pipenv or virtualenv as well. Keep in mind that Ansible cannot run on a Windows host natively, though it can run under the Windows Subsystem for Linux (WSL).

### Installing Ansible

We recommend installing Ansible via Conda for a seamless development experience. First, you need to install Conda:

```bash
conda create -n qhub-hpc -c conda-forge ansible
conda activate qhub-hpc
```

This creates a Conda environment named qhub-hpc and installs Ansible within it. You can activate this environment whenever you need to use Ansible for QHub HPC development tasks.

If you prefer not to use Conda and want to install Ansible using other methods, please follow the official Ansible installation instructions for your specific platform.

## Choose a Virtualization Provider

QHub HPC supports two virtualization providers: Libvirt and QEMU. You can choose the one that suits your needs. If you're unsure, we recommend using Libvirt.

### Providers

Vagrant is a versatile tool that can manage different types of machines through various providers. While Vagrant ships with support for VirtualBox, Hyper-V, and Docker, it can work with other providers as well. Choosing the right provider can offer features that align with your specific use case.

Alternate providers may offer advantages such as better stability and performance. For example, if you intend to use Vagrant for significant workloads, VMware providers are often recommended due to their robust support and reliability, surpassing VirtualBox in many scenarios.

Before you can use a different provider, you must install it using the Vagrant plugin system. Once installed, using the provider is straightforward and aligns with Vagrant's user-friendly approach.

For QHub HPC development, we provide instructions for two providers: Libvirt and virtualbox. Follow the relevant subsection for your chosen provider to set up your development environment.

### Libvirt

Libvirt is a toolkit for managing virtualization platforms. It provides a common API for different virtualization technologies, including QEMU, KVM, Xen, LXC, and VirtualBox. Libvirt is a popular choice for Linux-based systems and is the default provider for Vagrant on Linux.

If you're using a Linux-based system, we recommend using Libvirt as your provider. It offers better performance and stability than VirtualBox and is the default provider for Vagrant on Linux. For installation documentation, please refer to the [Libvirt provider documentation](https://ubuntu.com/server/docs/virtualization-libvirt).

Libvirt will also require you to install a an extension for Vagrant called `vagrant-libvirt`. You can install this extension by running the following command:

```bash
vagrant plugin install vagrant-libvirt
```

Note: For more information you can refer to this opensource article on [Libvirt](https://opensource.com/article/21/10/vagrant-libvirt).

### VirtualBox

VirtualBox is a popular virtualization platform that supports a wide range of operating systems. It is a cross-platform solution that is available for Windows, macOS, and Linux. VirtualBox is the default provider for Vagrant on Windows and macOS.

If you're using Windows or macOS, we recommend using VirtualBox as your provider. It is the default provider for Vagrant on these platforms and offers a stable and reliable experience. For installation documentation, please refer to the [VirtualBox community documentation](https://help.ubuntu.com/community/VirtualBox/Installation).

## Create and Provision VMs

Select one of the available test Vagrant files already present in this repository under the `/tests` directory. For example, if you want to test the `ubuntu1804` Vagrant file, run the following command:

```bash
cd tests/ubuntu1804
vagrant up --provider=<provider>
```

Before creating and provisioning the virtual machines (VMs), please be aware of potential naming conflicts if someone else has already used the same machine. To avoid conflicts, consider one of the following options:

1. Choose a Different Ubuntu Version:
   - Instead of `ubuntu1804`, try using `ubuntu2004` if it's available.

2. Add Your Own Prefix:
  You can add a unique prefix to the VM names to avoid conflicts. Set an environment variable `HPC_VM_PREFIX` with your chosen prefix before running any Vagrant commands. For example:

   ```bash
   export HPC_VM_PREFIX='-<my initials>'
    ```

  This will prefix all VM names with the string you provide. For example, if you set `HPC_VM_PREFIX='-abc'`, the VM names will be `abc-ubuntu1804-master`, `abc-ubuntu1804-worker-1`, and so on.

This should spin up the VMs and provision them using Ansible. If you encounter any errors, please refer to the [Troubleshooting] section.

Now that your VMs are up and running, lets populate then with the QHub infrastrcture. To do so, copy the contents of `templates.inventory/*` over into the newly created `.vagrant/provisioners/ansible/inventory/` directory. For example considering that you are in the `tests/ubuntu1804` directory, run the following command:

```bash
cp -r ../../templates.inventory/* .vagrant/provisioners/ansible/inventory/
```

you should now be able to see two new folders being added `host_vars` and `group_vars` under the `.vagrant/provisioners/ansible/inventory/` directory. These folders contain the variables that are used by Ansible to provision the VMs. For more information on the variables, please refer to the [configuration](./configuration.md) page in this documentation.

In the example above, the directory structure should be as follows:

```bash
tests/ubuntu2004/.vagrant/provisioners/ansible/inventory/
├── group_vars
│   ├── all.yaml
│   ├── hpc_master.yaml
│   └── hpc_worker.yaml
├── host_vars
│   └── hpc01-test.yaml
└── vagrant_ansible_inventory
```

Now to make the new changes to propagate, run the following command:

```bash
vagrant provision
```

This should now populate the VMs with the QHub infrastructure. You can now access the JupyterHub instance by visiting `https://<master node ip>/` where `<master node ip>` is the ip address of your specific deployment. You will be prompted by the jupyterhub landing page.

If you would like to set a DNS record for the master node, you can do so by adding the following line to your `/etc/hosts` file:

```bash
<master node ip> <your domain name>
```

and make sure to replace `<master node ip>` with the ip address of your master node and `<your domain name>` with the domain name you would like to use. If using a serivce such as CloudFlare to manage your DNS records, you can also set up an A record to point to the master node ip address and the above step will not be required.

Though, do update the contents of `group_vars/all.yaml` to include the extra field (at the end of the file):

```yaml
traefik_domain: <your domain name>
```

This will ensure that the traefik reverse proxy is configured to use the domain name you have set.

## Checking services

For debugging purposes, you can inspect service status, logs or restart an individual service while connected to the master node. Bellow we give an example of how to do this for the JupyterHub and Slurm services.

```bash
# Restart JupyterHub:
systemctl restart jupyterhub

# Inspect logs:
journalctl -u jupyterhub -e
```

`SlurmSpawner` logs are stored in the worker nodes in the home folder of the user running JupyterLab, e.g., `/home/example-user/.jupyterhub_slurmspawner_9.log`

## Troubleshooting
