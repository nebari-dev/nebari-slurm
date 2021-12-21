# ContainDS Dashboards

ContainDS Dashboards is a dashboard publishing solution that has been
integrated with Qhub-HPC. Refer to the [main
documentation](https:// cdsdashboards.readthedocs.io/en/stable/) for
additional info.

## Necessary Steps to use ContainDS Dashboards with Qhub-HPC
- Add `cdsdashboards` to your jupyterhub environment
- Add `cdsdashboards-singleuser` as well as the desired supported
  visualization libraries (panel, bokeh, voila, streamlit, plotlydash,
  rshiny, etc.) to one of your user environments.  Note, each user
  environment also requires `jupyterlab`, `jupyterhub`, and
  `batchspawner` to function properly on qhub-hpc.
- Set `cdsdashboards.enabled` to true in `group_vars/all.yaml`
- Rerun ansible-playbook after adding the new environment.

## Restarting a Stopped Dashboard

If you stop your dashboard from the Home tab of Jupyterhub, and wish
to restart it then click the dashboard name, scroll to the bottom of
the form, and push Save to retart. Do **not** click on the start
button on the Home tab of Jupyterhub.  This option does **not** work
currently.  ![Click Green Highlighted Region to Restart
Dashboard](_static/images/qhub-dashboards-bug.png)
