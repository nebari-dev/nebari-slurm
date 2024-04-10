# User Guide

## Conda

### Adding and updating Conda environments

#### What is `conda-store`?

[`conda-store`][conda-store-docs] is a Python package that serves _identical_
`conda` environments by controlling the environment lifecycle.
It ensures that the management, building, and serving of environments is as
identical as possible and seamless for the end users.

All environments in Nebari are served through `conda-store`.

Using `conda-store`, Nebari admins can track specific files or directories for
changes in environment specifications. They can manage environments using the
web interface, REST API, or the command-line utility (CLI).

#### Exploring the conda-store Interface

Access conda-store through your domain `<nebari-slurm-domain/conda-store>`, log
in to authenticate, and navigate the dashboard to view account details and permissions.

- Key sections include User, Namespaces, and Permissions, which dictate access
  levels and capabilities.

![conda-store default main page, before authentication, login button highlighted](https://conda.store/assets/images/login-1346a06ed408f74937da23b0a1c6fda3.png)

#### Creating a New Environment

Environments are created in conda-store using a YAML file. Post-creation, the
environment can be managed through the conda-store UI, allowing for edits and
build status monitoring.

More details on creating environments can be found in the [conda-store documentation](https://conda.store/conda-store-ui/tutorials/create-envs).

Package installation should be done via the conda-store web interface to avoid
inconsistencies and limitations associated with command line installations.

#### **Note on Shared Namespaces**

Access to shared namespaces in conda-store depends on user assignment to groups
in Keycloak and the corresponding permissions within those groups.

By default, NebarSlurm is deployed with the following groups: `admin`, `developer`,
and `analyst` (in roughly descending order of permissions and scope). Note that
such group names will differ on a per-instance basis. Check
[Conda-store authorization model](https://conda-store.readthedocs.io/en/latest/contributing.html#authorization-model)
for more details on conda-store authorization.

## ContainDS Dashboards

ContainDS Dashboards is a dashboard publishing solution that has been
integrated with Qhub-HPC. Refer to the [main
documentation](https:// cdsdashboards.readthedocs.io/en/stable/) for
additional info.

### Necessary Steps to use ContainDS Dashboards with Qhub-HPC

- Add `cdsdashboards` to your jupyterhub environment
- Add `cdsdashboards-singleuser` as well as the desired supported
  visualization libraries (panel, bokeh, voila, streamlit, plotlydash,
  rshiny, etc.) to one of your user environments.  Note, each user
  environment also requires `jupyterlab`, `jupyterhub`, and
  `batchspawner` to function properly on qhub-hpc.
- Set `cdsdashboards.enabled` to true in `group_vars/all.yaml`
- Rerun ansible-playbook after adding the new environment.

### Restarting a Stopped Dashboard

If you stop your dashboard from the Home tab of Jupyterhub, and wish
to restart it then click the dashboard name, scroll to the bottom of
the form, and push Save to retart. Do **not** click on the start
button on the Home tab of Jupyterhub.  This option does **not** work
currently.  ![Click Green Highlighted Region to Restart
Dashboard](_static/images/qhub-dashboards-bug.png)

## Dask

Dask support is based on:

- [dask distributed](https://distributed.dask.org/en/latest/)
- [dask gateway](https://gateway.dask.org/)

[conda-store-docs]: https://conda-store.readthedocs.io/
