# Dependencies

 - Terraform v0.14.4
   - [Download link](https://releases.hashicorp.com/terraform/0.14.4/)
   - [Instruction to install link](https://learn.hashicorp.com/tutorials/terraform/install-cli)

# Testing

## Create ssh key for azure vm

Create ssh key for azure vm and ensure that public and
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

## Get the subscription_id and tenant_id

To get [subscription_id and tenant_id](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure_cli)

```shell
export ARM_SUBSCRIPTION_ID=...
export ARM_TENANT_ID=...
```

## Create azure resources

```shell
terraform init
terraform apply
```

After `terraform apply` and `inventory` file will be created

## Ansible playbook application

Adjust the following terraform variables:
  - `resource-location` 
  - `vnet-address-space`
  - `subnet-1-address-prefix`
  - `master-machine-size`
  - `node-machine-size`
  - `node-machine-size`
  - `worker-count`
  - `os-disk-size`

You might want to change the these variables according to your requirements
## Destroying the resources

```shell
terraform destroy
```
