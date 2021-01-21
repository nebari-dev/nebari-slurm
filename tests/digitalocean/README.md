# Dependencies

 - [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
 - [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

# Testing

## Create ssh key for droplets

Create ssh key for digital ocean droplets and ensure that public and
private key are in current directory.

```shell
$ ssh-keygen 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/<username>/.ssh/id_rsa): ./id_rsa
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in ./id_rsa
Your public key has been saved in ./id_rsa.pub
...
```

Ensure that `id_rsa` and `id_rsa.pub` are properly permissioned
`600`. If not use `chmod`

```shell
chmod 600 id_rsa
chmod 600 id_rsa.pub
```

## Create digitalocean environment variable

Create a [DigitalOcean api key](https://www.digitalocean.com/community/tutorials/how-to-create-a-digitalocean-space-and-api-key)

```shell
export DIGITALOCEAN_TOKEN=...
```

## Create digital ocean resources

```shell
terraform init
terraform apply
```

After `terraform apply` and `inventory` file will be created

## Ansible playbook application

Adjust the following terraform variables:
  - `group_vars/all.yaml` `internal_interface` -> `eth1`
  - `group_vars/all.yaml` `firewall.internal_ip_range` -> `10.10.10.0/24`
  - `group_vars/hpc-worker.yaml` `nfs_client.mounts.*.host` -> `qhub-onprem-test-master`
  
You may have a different internal_ip address range is you changed
`var.ip_range` in terraform.


```shell
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory ../../playbook.yaml
```

You should then be able to access the grafana and jupyterhub service.

## Destroying the resources

```shell
terraform destroy
```
