## Remote Development

Running and developing on a remote Linux machine running `libvirt`.

In this example, using a Mac laptop.

### Set up SSH on local machine

In ~/.ssh/config add:

```
Host gpu
  HostName gpu.quansight.dev
  User dlester
  IdentityFile ~/.ssh/id_rsa
  Port 2222
#  LocalForward 8443 192.168.121.171:443
```

Connect to that machine:

```
ssh gpu
```

### Clone repo and setup Nix shell

Inside the remote:

```
git clone https://github.com/Quansight/qhub-hpc
cd qhub-hpc
nix develop

# Install some ansible addons
ansible-galaxy collection install -r requirements.yaml
```

The nix-shell command installs packages mentioned in `flake.nix` and launches a shell.

### Configure traefik to expect traffic from localhost
Modify the all.yaml file to define the traefik.domain ansible variable as below.

```yaml
traefik:
  ... # other variables defined here
  domain: localhost
```

### Create and provision VMs

Inside the remote still:

```
cd tests/ubuntu1804
# OR  cd tests/ubuntu2004
vagrant up --provider=libvirt
```

Note that if someone else has already done this on the same machine, there may be a naming conflict. Either try 
ubuntu2004 instead, or add your own prefix to avoid a conflict.

For tests/ubuntu1804, this can be achieved by setting `export HPC_VM_PREFIX='-<my initials>'` before running any vagrant commands.

### Connect to hpc01-test VM

On the remote:

```
vagrant ssh
```

This should ssh into the hpc01-test VM.

To obtain the IP on the remote network:

```
ip addr
```

This could be 192.168.121.171 for example.

To be able to connect all the way through, back on the host Mac add/update to ~/.ssh/config:

```
Host gpu
  HostName gpu.quansight.dev
  User dlester
  IdentityFile ~/.ssh/id_rsa
  Port 2222
  LocalForward 8443 192.168.121.171:443

Host vm
  HostName 192.168.121.171
  user vagrant
  Port 22
  ProxyJump gpu 
```

Note the IP address we obtained for the VM appears twice - once in the (now uncommented LocalForward in gpu), and 
again in the second section (vm).

You should now be able to:

1. Connect direct to the master node (hpc01-test) from your Mac using `ssh vm`
2. Visit https://localhost:8443/ to view JupyterHub on the master node through the port forward

## Development in VSCode

In VSCode on your Mac, you can install the [Remote SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension.

Cmd+Shift+P to load command palette, select `Remote - SSH: Connect to Host` and `gpu` should show up. You can browse the remote file system and open the qhub-hpc folder.

During development, if you make changes then you may need to re-provision using:

```
ssh gpu

# On remote:
cd qhub-hpc
nix develop

cd tests/ubuntu1804
vagrant provision
```

Or it may be easier just to edit/copy the jupyterhub_config.py file to /etc/jupyterhub directly.
Similarly with source files, or it should also be possible to only run the relevant ansible steps.

To run ansible directly only on tasks tagged 'conda' and 'jupyterhub' on the master node, run this within the nix shell on the gpu machine:

```
ansible-playbook -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --private-key=~/.vagrant.d/insecure_private_key -u vagrant -l hpc_master --tags="conda,jupyterhub" ../../playbook.yaml
```

For debugging:

```
# Restart JupyterHub to read latest config changes:
systemctl restart jupyterhub
# Inspect logs
journalctl -u jupyterhub -e
```

SlurmSpawner logs are stored in the worker nodes in the home folder of the user running JupyterLab, eg. /home/example-user/.jupyterhub_slurmspawner_9.log

Conda troubles:
To completely remove and reinstall:
```
sudo rm -rf /opt/conda/envs/jupyterhub
sudo /opt/conda/bin/conda env update -f /opt/conda-environments/jupyterhub.yaml --prefix /opt/conda/envs/jupyterhub
```

## KVM and libvirt

If you find vagrant is in an inconsistent state and cannot access the VMs, you can destroy manually:

virsh list --all
# get the machine name

virsh destroy <THE_MACHINE>
virsh undefine <THE_MACHINE>

# get the volume name
virsh vol-list default

virsh vol-delete --pool default <THE_VOLUME>

## SQLite

To inspect the database, `ssh vm` then:

```
sudo apt install sqlite3
sqlite3 /var/lib/jupyterhub/jupyterhub.sqlite
```
