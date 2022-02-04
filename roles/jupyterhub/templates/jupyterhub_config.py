##
## This file is maintained by Ansible - ALL MODIFICATIONS WILL BE REVERTED
## https://jupyterhub.readthedocs.io/en/stable/getting-started/config-basics.html
##
import subprocess
import json
import os

from jupyterhub_traefik_proxy import TraefikTomlProxy
from batchspawner import SlurmSpawner
from traitlets import Unicode, Callable

# Find all conda environments that have dask jupyterlab, batchspawner, and jupyterhub installed
jupyterlab_packages = ['jupyterlab', 'batchspawner', 'jupyterhub']
def conda_envs_w_packages(packages, names_only=False):
    _environments = []
    output = subprocess.check_output(['conda', 'env', 'list', '--json'])
    environments = json.loads(output)['envs']
    for environment in environments:
        output = subprocess.check_output(['conda', 'list', '-p', environment, '--json'])
        if set(packages)  <= {_['name'] for _ in json.loads(output)}:
            _environments.append((os.path.basename(environment), environment))
    if names_only:
        return [env_name for env_name, path in _environments]
    return _environments


# Allow gathering of jupyterhub prometheus metrics
c.JupyterHub.authenticate_prometheus = False

# JupyterHub base url
c.JupyterHub.base_url = '{{ jupyterhub_base_url }}'

# Don't kill servers when JupyterHub restarts
c.JupyterHub.cleanup_servers = False

# Turn sessions off - we don't use them, since we pass through to slurm
c.PAMAuthenticator.open_sessions = False

# Listen on all interfaces, since hub should be reachable from spawned nodes
c.JupyterHub.hub_ip = '0.0.0.0'


# -------------------- Base Authenticator ----------------
from oauthenticator.generic import GenericOAuthenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator
c.OAuthenticator.client_id = "{{ jupyterhub_client_id }}"
c.OAuthenticator.client_secret = "{{ jupyterhub_client_secret }}"
c.GenericOAuthenticator.oauth_callback_url = "https://{{ traefik_domain | default(hostvars[groups['hpc-master'][0]].ansible_host) }}/hub/oauth_callback"
c.GenericOAuthenticator.scope = "profile"
c.GenericOAuthenticator.tls_verify = False
c.GenericOAuthenticator.authorize_url = "https://{{ traefik_domain | default(hostvars[groups['hpc-master'][0]].ansible_host) }}/auth/realms/{{ keycloak_realm }}/protocol/openid-connect/auth"
c.GenericOAuthenticator.token_url = "https://{{ traefik_domain | default(hostvars[groups['hpc-master'][0]].ansible_host) }}/auth/realms/{{ keycloak_realm }}/protocol/openid-connect/token"
c.GenericOAuthenticator.userdata_url = "https://{{ traefik_domain | default(hostvars[groups['hpc-master'][0]].ansible_host) }}/auth/realms/{{ keycloak_realm }}/protocol/openid-connect/userinfo"
c.GenericOAuthenticator.username_key = "preferred_username"
c.GenericOAuthenticator.claim_groups_key = "roles"
c.GenericOAuthenticator.allowed_groups = ['jupyterhub_admin', 'jupyterhub_developer']
c.GenericOAuthenticator.admin_groups = ['jupyterhub_admin']

# -------------------- Base Spawner --------------------

class QHubHPCSpawnerBase(SlurmSpawner):

  req_conda_environment_prefix = Unicode('',
        help="Conda environment prefix to launch jupyterlab"
    ).tag(config=True)

  # data from form submission is {key: [value]}
  # we need to convert the formdata to a key value dict
  def options_from_form(self, data):
      return {key: value[0] for key, value in data.items()}

  main_options_form = f'''
<div class="form-group row">
  <label for="memory" class="col-2 col-form-label">JupyterLab Memory (GB)</label>
  <div class="col-10">
    <input class="form-control" type="number" value="1" id="memory" name="memory">
  </div>
</div>
<div class="form-group row">
  <label for="nprocs" class="col-2 col-form-label">JupyterLab CPUs</label>
  <div class="col-10">
    <input class="form-control" type="number" value="1" id="nprocs" name="nprocs">
  </div>
</div>
<div class="form-group row">
  <label for="partition" class="col-2 col-form-label">Slurm Partition</label>
  <div class="col-10">
     <select class="form-select" aria-label="Slurm Queue" id="partition" name="partition">
       <option value="general">general</option>
{% for item in groups %}
{% if item.startswith('partition-')%}
       <option value="{{ item[10:] }}">{{ item[10:] }}</option>
{% endif %}
{% endfor %}
     </select>
  </div>
</div>
'''

  conda_options_form = f'''
{% raw %}
<div class="form-group row">
  <label for="conda_environment_prefix" class="col-2 col-form-label">Conda Environment</label>
  <div class="col-10">
     <select class="form-select" aria-label="Conda Environment" id="conda_environment_prefix" name="conda_environment_prefix">
{''.join([f'<option value="{_[1]}">{_[0]}</option>' for _ in conda_envs_w_packages(jupyterlab_packages)])}
     </select>
  </div>
</div>
{% endraw %}
'''

  def options_form(self, spawner):

    ## Not currently working - idea is to omit conda env from spawner form
    ## for dashboards, since already selected a conda env
    #if spawner.orm_spawner.user_options and 'presentation_type' in spawner.orm_spawner.user_options:
    #  self.log.info("In options_form")
    #  if spawner.user_options['presentation_type']:
    #    return self.main_options_form # Omit the conda env dropdown since that is chosen per dashboard

    # Display full form including conda env dropdown
    return ''.join([self.main_options_form, self.conda_options_form])


{% if cdsdashboards_enabled %}
# -------------------- Specify Dashboard Instance Size --------------------
from cdsdashboards.app import CDS_TEMPLATE_PATHS
from cdsdashboards.hubextension import cds_extra_handlers

from cdsdashboards.hubextension.spawners.variablemixin import VariableMixin, MetaVariableMixin

dashboard_packages = ['cdsdashboards-singleuser']

class QHubHPCSpawner(QHubHPCSpawnerBase, VariableMixin, metaclass=MetaVariableMixin):
  pass

c.VariableMixin.default_presentation_cmd = ['jhsingle-native-proxy']

c.JupyterHub.allow_named_servers = True

c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.processbuilder.ProcessBuilder'

c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
c.JupyterHub.extra_handlers = cds_extra_handlers

c.CDSDashboardsConfig.conda_envs = conda_envs_w_packages(jupyterlab_packages + dashboard_packages, names_only=True)

# Force dashboard creator to select an instance size
c.CDSDashboardsConfig.spawn_default_options = False

c.JupyterHub.default_url = '/hub/home'

{% else %}

# Assign Qhub Spawner
class QHubHPCSpawner(QHubHPCSpawnerBase):
    pass

c.JupyterHub.template_paths = []
c.JupyterHub.extra_handlers = []

{% endif %}

c.JupyterHub.spawner_class = QHubHPCSpawner

c.SlurmSpawner.start_timeout = {{ jupyterhub_config.spawner.start_timeout }}
c.QHubHPCSpawner.default_url = '/lab'

# default values for batch spawner
c.QHubHPCSpawner.req_memory = '1' # GB
c.QHubHPCSpawner.req_nprocs = '1'
c.QHubHPCSpawner.req_conda_environment_prefix = '{{ miniforge_home }}/envs/{{ jupyterhub_lab_environment | basename | splitext | first }}'
c.QHubHPCSpawner.req_prologue = '''
# ensure user has link to shared directory
if [ ! -L "$HOME/share" ]; then
  ln -s /home/share "$HOME/share"
fi

# ensure ipyparallel configuration profiles
cp -r /etc/jupyter/profile_default $HOME/.ipython/

export PATH={{ miniforge_home }}/condabin:$PATH
'''


c.QHubHPCSpawner.batch_script = """#!/bin/bash
{% raw %}
#SBATCH --output={{homedir}}/.jupyterhub_slurmspawner_%j.log
#SBATCH --error={{homedir}}/.jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --chdir={{homedir}}
#SBATCH --export={{keepvars}}
#SBATCH --get-user-env=L
{% if partition  %}#SBATCH --partition={{partition}}
{% endif %}{% if runtime    %}#SBATCH --time={{runtime}}
{% endif %}{% if memory     %}#SBATCH --mem={{memory}}G
{% endif %}{% if gres       %}#SBATCH --gres={{gres}}
{% endif %}{% if nprocs     %}#SBATCH --cpus-per-task={{nprocs}}
{% endif %}{% if reservation%}#SBATCH --reservation={{reservation}}
{% endif %}{% if options    %}#SBATCH {{options}}{% endif %}
set -euo pipefail
trap 'echo SIGTERM received' TERM
{{prologue}}
{% endraw %}

{% if cdsdashboards_enabled %}
# Overwrite conda_environment_prefix when using cdsdashboards
if [ -n '{{ '{{ conda_env }}' }}' ]; then
    export PATH={{miniforge_home}}/envs/{{ '{{ conda_env }}' }}/bin:$PATH
else
    export PATH={{ '{{ conda_environment_prefix }}' }}/bin:$PATH
fi
{% else %}
export PATH={{ '{{ conda_environment_prefix }}' }}/bin:$PATH
{% endif %}

{% raw %}
which jupyterhub-singleuser
echo "running command {{cmd}}"
{% if srun %}{{srun}} {% endif %}{{cmd}}
echo "jupyterhub-singleuser ended gracefully"
{{epilogue}}
"""
{% endraw %}


# ===== adding api tokens for external services =======
c.JupyterHub.services = [
{% for service_name in jupyterhub_services %}
   {
      'name': "{{ service_name }}",
      'api_token': "{{ jupyterhub_services[service_name] }}",
      'admin': True
   },
{% endfor %}
]

#==================== THEMING =====================#

import tornado.web
import qhub_jupyterhub_theme

c.JupyterHub.extra_handlers = [
    (r'/custom/(.*)', tornado.web.StaticFileHandler, {"path": qhub_jupyterhub_theme.STATIC_PATH}),
] + c.JupyterHub.extra_handlers

c.JupyterHub.template_paths = [
    qhub_jupyterhub_theme.TEMPLATE_PATH
] + c.JupyterHub.template_paths

c.JupyterHub.template_vars = {
{% for key, value in jupyterhub_theme.template_vars.items() %}
    '{{ key }}': '{{ value }}',
{% endfor %}
{% if cdsdashboards_enabled %}'cdsdashboards_enabled': True{% endif %}
}

# ======================= CUSTOM ==================
jupyterhub_custom = json.loads('{{ jupyterhub_custom | tojson }}')
for classname, attributes in jupyterhub_custom.items():
    for attribute, value in attributes.items():
        setattr(getattr(c, classname), attribute, value)
