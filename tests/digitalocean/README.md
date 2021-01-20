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
