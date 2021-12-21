# Copying Arbitrary Files onto Nodes
Arbitrary files and folders can be copied from the ansible control node onto the managed nodes as part of the ansible playbook deployment by setting the following ansible variables to copy files onto all nodes, all nodes in a particular group or only onto a particular node respectively.
    - `copy_files_all`
    - `copy_files_[ansible_group_name]`
    - `copy_files_[ansible_host_name]`

Copying a file onto the hpc02-test node could be done by setting the following ansible variable e.g. in the host_vars/hpc02-test.yaml file.
```yaml
...
copy_files_hpc02-test:
    - src: /path/to/file/on/control/node
      dest: /path/to/file/on/manged/node
      owner: root
      group: users
      mode: 'u=rw,g=r,o=r' # or alternatively '644'
      directory_mode: '644'
```

The owner, group, and mode fields are optional.  See https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html#id2 for more detail about each field.
