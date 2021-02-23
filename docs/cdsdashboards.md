# ContainDS Dashboards

ContainDS Dashboards is a dashboard publishing colution that has been integrated with Qhub-onprem. Refer to the [main documentation](https:// cdsdashboards.readthedocs.io/en/stable/) for additional info.

## Necessary Steps to use ContainDS Dashboards with Qhub-onprem
- Add `cdsdashboards` to your jupyterhub environment
- Add `cdsdashboards-singleuser` as well as the desired supported visualization libraries (panel, bokeh, voila, streamlit, plotlydash, rshiny, etc.) to one of your user environments.
- Set `cdsdashboards.enabled` to true in `group_vars/all.yaml`
