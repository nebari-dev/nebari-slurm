# Configuration

## User and group management

### Adding new user

In order to add new users to QHub-HPC add to the `enabled_users`
variable. The format for each user is:

```yaml
enabled_users:
 ...
 - username: <username>
   uid: <user id to assign to user>
   fullname: <fullname of user>
   email: <email of user>
   primary_group: <name of primary group user is member of [optional]>
   groups: [<list of group names user is member of [optional]>
 ...
```

### Adding new groups

In order to add new groups to QHub-HPC add to the `enabled_groups`
variable. The format for each group is:

```yaml
enabled_groups:
  ...
  - name: <group name>
    gid: <group id for group name>
  ...
```

### Ensuring groups or users that do not exist

Adding any username or group name to `disabled_users` or
`disabled_groups`.

```yaml
disabled_groups:
  ...
  - <group-name>
  ...

disalbed_users:
  ...
  - <username>
  ...
```

## Adding additional packages to nodes

Setting the variable `installed_packages` will ensure that the given
Ubuntu packages are installed on the given node.

```yaml
installed_packages:
 ...
 - git
 ...
```

## NFS client mounts

You may mount arbitrary nfs mounts via `nfs_client_mounts`
variable. The format for `nfs_client_mounts` is as follows:

```yaml
nfs_client_mounts:
  ...
  - host: <host name for nfs mount>
    path: <path to mount given nfs export>
  ...
```

## Samba/CIFS client mounts


You may mount arbitrary cifs/samba or windows file shares with
`samba_client_mounts`. The `username`, `password`, `options`, and
`domain` fields are optional. 

```yaml
samba_client_mounts:
  ...
  - name: <name of samba share>
    host: <dns host name for samba or windows file share>
    path: <path name for where to mount samba share>
    options: <linux mount options to set>
    username: <username to use for login>
    password: <password to use for login>
    domain: <domain to use for login>
  ...
```

## JupyterHub 

### Setting arbitrary traitlets in JupyterHub

Setting a key, key, value in `jupyterhub_custom` is equivalent to
setting the traitlet `c.<classname>.<attribute> = <value>`. For
example to set the traitlet `c.Spawner.start_timeout = 60`.

```yaml
jupyterhub_custom:
  Spawner:
    start_timeout: 60
```

### Arbitrary additional files as configuration

You may add additional files that are run at the end of JupyterHub's
configuration via Traitlets. 

```yaml
jupyterhub_additional_config:
  ...
  01-myconfig: "{{ inventory_dir }}/<path-to-file>.py
  ...
```

The variable `inventory_dir` is a convenient variable that allows you
to reference files created within your inventory directory.

### JupyterHub idle culler

Adjusting the `idle_culler` settings or disabling the culler is
configurable.

```yaml
idle_culler:
  enabled: true
  timeout: 86400   # 1 day
  cull_every: 3600 # 1 hour
```

 - `timeout` is the time that a user is inactive 
 - `cull_every` is the interval to delete inactive jupyterlab instances

### Set default UI to classic jupyter notebooks

As of JupyterHub 2.0, the default user interface is Jupyterlab.  If the classic Jupyter notebook UI is preferred, this can be configured as shown below.
```yaml
jupyterhub_custom:
  QHubHPCSpawner:
    default_url: '/tree'
  Spawner:
    environment:
      JUPYTERHUB_SINGLEUSER_APP: notebook.notebookapp.NotebookApp
```

### Services

Additional services can be added to the `jupyterhub_services`
variable. Currently this is only `<service-name>:
<service-apikey>`. You must keep the `dask_gatway` section.

```yaml
jupyterhub_services:
  ...
  <service-name>: <service-apikey>
  ...
```

### Theme

The theme variables are using
[qhub-jupyterhub-theme](https://github.com/Quansight/qhub-jupyterhub-theme). All
variables are configurable. `logo` is a special variable where you
supply a url that the users web browser can access.

```yaml
jupyterhub_theme:
  template_vars:
    hub_title: "This is QHub HPC"
    hub_subtitle: "your scalable open source data science laboratory."
    welcome: "have fun."
    logo: "/hub/custom/images/jupyter_qhub_logo.svg"
    primary_color: '#4f4173'
    secondary_color: '#957da6'
    accent_color: '#32C574'
    text_color: "#111111"
    h1_color: "#652e8e"
    h2_color: "#652e8e"
```

## Copying Arbitrary Files onto Nodes

Arbitrary files and folders can be copied from the ansible control
node onto the managed nodes as part of the ansible playbook deployment
by setting the following ansible variables to copy files onto all
nodes, all nodes in a particular group or only onto a particular node
respectively.

    - `copy_files_all`
    - `copy_files_[ansible_group_name]`
    - `copy_files_[ansible_host_name]`

Copying two files/folders onto the hpc02-test node could be done by
setting the following ansible variable e.g. in the
host_vars/hpc02-test.yaml file.

```yaml
...
copy_files_hpc02-test:
  - src: /path/to/file/on/control/node
    dest: /path/to/file/on/manged/node
    owner: root
    group: root
    mode: 'u=rw,g=r,o=r'
    directory_mode: '644'
  - src: /path/to/other/file/on/control/node
    dest: /path/to/other/file/on/manged/node
    owner: vagrant
    group: users
    mode: '666'
    directory_mode: 'ugo+rwx'
```

The owner, group, and mode fields are optional. See
https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html#id2
for more detail about each field.

Files copied in this way will not overwrite existing files.  Also,
remember that the home directory of users is a network file system so
it would only be necessary to copy files in the user directories into
a single node.

## Slurm

Slurm configuration. Only a few slurm variables should be
configured. Sadly with how ansible works all variables must be copied
from the default. These two configuration settings allow additional
ini section and keys to be set.

```yaml
slurm_config:
  ...

slurmdbd_config:
  ...
```

## Traefik

### Accessing Qhub HPC from a Domain

By default, a qhub-hpc deployment must be accesssed using the ip
address of the hpc-master node.  However, if a domain name has been
set up to point to the hpc-master node, then Qhub HPC's router,
[Traefik](https://doc.traefik.io/traefik/), can be configured to work
with the domain by setting the `traefik_domain` ansible variable.

For example, if you had the example.com domain set up to point to the
hpc-master node, then you could add the following to the all.yaml file
and redeploy, after which navigating to https://example.com in a web
browser would bring up your Qhub HPC deployment sign in page.

```yaml
traefik_domain: example.com
```

### Automated Lets-Encrypt Certificate

Traefik can provision a tls certificate from Let's Encrypt assuming
that your master node ip is publicly accessible. Additionally the
`traefik_domain` and `traefik_letsencrypt_email` must be set.

```yaml
traefik_tls_type: letsencrypt
traefik_letsencrypt_email: myemail@example.com
```

### Custom TLS Certificate

By default, traefik will create and use a self signed TLS certificate
for user communication.  If desired, a custom TLS Certificate can be
copied from ansible to the appropriate location for use by Traefik.
To do so, set the following settings in the all.yaml file.

```yaml
traefik_tls_type: certificate
traefik_tls_certificate: /path/to/MyCertificate.crt
traefik_tls_key: /path/to/MyKey.key
```

For testing out this optional it is easy to generate your own
self-signed certificate. Substitute all of the values for values that
fit your use case.

```shell
export QHUB_HPC_DOMAIN=example.com
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 \
  -subj "/C=US/ST=Oregon/L=Portland/O=Quansight/OU=Org/CN=$QHUB_HPC_DOMAIN" \
  -nodes
```

## Backups

Backups are performed in QHub HPC via [restic](https://restic.net/)
an open source backup tool. It is extremely flexible on where backups
are performed as well as supporting encrypted, incremental backups.

### Variables

The following shows a daily backup on S3 for QHub.

```yaml
backup_enabled: true
backup_on_calendar: "daily"
backup_randomized_delay: "3600"
backup_environment:
  RESTIC_REPOSITORY: "s3:s3.amazonaws.com/bucket_name"
  RESTIC_PASSWORD: "thisismyencryptionkey"
  AWS_ACCESS_KEY_ID: accesskey
  AWS_SECRET_ACCESS_KEY: mylongsecretaccesskey
```
 - `backup_enabled` :: determines whether backups are enabled
 - `backup_on_calendar` :: determines the frequency to perform backups. Consult [systemd timer](https://www.freedesktop.org/software/systemd/man/systemd.timer.html) documentation for syntax
 - `backup_randomized_delay` :: is the random delay in seconds to apply to backups. Usefull to prevent backups from all being performed at an exact time each day
  - `backup_environment` :: are all the key value pairs used to configure restic. RESTIC_REPOSITORY and RESTIC_PASSWORD are required. The rest are environment variables for the specific [backup repository](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html).

### Manual backup

At any time you can trigger a manual backup. SSH into the master node.

```shell
sudo systemctl start restic-backup.service
```

