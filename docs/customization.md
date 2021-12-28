<<<<<<< HEAD
# Copying Arbitrary Files onto Nodes
Arbitrary files and folders can be copied from the ansible control node onto the managed nodes as part of the ansible playbook deployment by setting the following ansible variables to copy files onto all nodes, all nodes in a particular group or only onto a particular node respectively.
    - `copy_files_all`
    - `copy_files_[ansible_group_name]`
    - `copy_files_[ansible_host_name]`

Copying two files/folders onto the hpc02-test node could be done by setting the following ansible variable e.g. in the host_vars/hpc02-test.yaml file.
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

The owner, group, and mode fields are optional.  See https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html#id2 for more detail about each field.  

Files copied in this way will not overwrite existing files.  Also, remember that the home directory of users is a network file system so it would only be necessary to copy files in the user directories into a single node.
=======
# Accessing Qhub HPC from a Domain

By default, a qhub-hpc deployment must be accesssed using the ip address of the hpc-master node.  However, if a domain name has been set up to point to the hpc-master node, then Qhub HPC's router, [Traefik](https://doc.traefik.io/traefik/), can be configured to work with the domain by setting the **traefik.domain** ansible variable.

For example, if you had the example.com domain set up to point to the hpc-master node, then you could add the following to the all.yaml file and redeploy, after which navigating to https://example.com in a web browser would bring up your Qhub HPC deployment sign in page.

```yaml
traefik:
  ... # other variables defined here
  domain: example.com
```

>>>>>>> rename_set_domain
