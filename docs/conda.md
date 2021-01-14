# Conda

Refer to the [main documentation](https://docs.conda.io/en/latest/)

## Adding Conda Environments

To add a new conda environment add the `environment.yaml` to
`files/environments/<environment-name>.yaml` where
`<environment-name>` is the name of the environment specified in the
yaml file. An example would be 

```yaml
name: example
channels:
 - conda-forge
dependencies:
 - python
```

Where we would add a file `files/environment/example.yaml`.

You must then specify the environment in `group_vars/hpc-master.yaml`
in the list of `miniforge.environments`. E.g.

```
miniforge:
  environments:
     ...
     - example
     ...
```

When you rerun the `ansible-playbook -i <inventory> playbook.yaml` the
environment will be created for all nodes.

## Updating a conda environment

To update a conda environment simply modify the
`files/environments/<environment-name>.yaml` and rerun the
ansible-playbook.
