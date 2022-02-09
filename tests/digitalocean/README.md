# Dependencies

 - [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
 - [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

# Testing

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

After `terraform apply` an `inventory` and ssh private/public key file
will be created.

## QHub-HPC installation

Follow the installation

## Destroying the resources

```shell
terraform destroy
```
