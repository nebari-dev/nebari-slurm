##
## This file is maintained by Ansible - ALL MODIFICATIONS WILL BE REVERTED
## https://jupyterhub.readthedocs.io/en/stable/getting-started/config-basics.html
##
import subprocess
import json
import os
import sys
import glob

from batchspawner import SlurmSpawner, format_template
from traitlets import Unicode, default, Union
import keycloak
from textwrap import dedent

from jupyterhub.utils import maybe_future
from jupyterhub.traitlets import Callable
from tornado import gen

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

# Configure jupyterhub to work with external proxy
c.JupyterHub.cleanup_servers = False
c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.auth_token = "{{ jupyterhub_proxy_auth_token }}"
c.ConfigurableHTTPProxy.api_url = 'http://localhost:{{ jupyterhub_proxy_api_port }}'

# Turn sessions off - we don't use them, since we pass through to slurm
c.PAMAuthenticator.open_sessions = False

# Listen on all interfaces, since hub should be reachable from spawned nodes
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = {{ jupyterhub_port }}


# -------------------- Base Authenticator ----------------
from oauthenticator.generic import GenericOAuthenticator

c.OAuthenticator.client_id = "{{ jupyterhub_client_id }}"
c.OAuthenticator.client_secret = "{{ jupyterhub_client_secret }}"
c.GenericOAuthenticator.oauth_callback_url = "https://{{ traefik_domain | default(hostvars[groups['hpc_master'][0]].ansible_ssh_host) }}/hub/oauth_callback"
c.GenericOAuthenticator.scope = "profile"
c.GenericOAuthenticator.tls_verify = False
c.GenericOAuthAuthentication.http_request_kwargs = {'validate_cert': False}
c.GenericOAuthenticator.authorize_url = "https://{{ traefik_domain | default(hostvars[groups['hpc_master'][0]].ansible_ssh_host) }}/auth/realms/{{ keycloak_realm }}/protocol/openid-connect/auth"
c.GenericOAuthenticator.token_url = "https://{{ traefik_domain | default(hostvars[groups['hpc_master'][0]].ansible_ssh_host) }}/auth/realms/{{ keycloak_realm }}/protocol/openid-connect/token"
c.GenericOAuthenticator.userdata_url = "https://{{ traefik_domain | default(hostvars[groups['hpc_master'][0]].ansible_ssh_host) }}/auth/realms/{{ keycloak_realm }}/protocol/openid-connect/userinfo"
c.GenericOAuthenticator.username_key = "preferred_username"
c.GenericOAuthenticator.claim_groups_key = "roles"
c.GenericOAuthenticator.allowed_groups = ['jupyterhub_admin', 'jupyterhub_developer']
c.GenericOAuthenticator.admin_groups = ['jupyterhub_admin']


def sync_users(username, min_uid=1_000_000, max_uid=1_000_000_000):
    current_uids = set()
    keycloak_admin = keycloak.KeycloakAdmin(
        server_url="https://{{ traefik_domain | default(hostvars[groups['hpc_master'][0]].ansible_ssh_host) }}/auth/",
        username="{{ keycloak_admin_username }}",
        password="{{ keycloak_admin_password }}",
        realm_name="{{ keycloak_realm }}",
        user_realm_name="master",
        verify=False)

    # quick check to see if user_sync has run on user
    # function only runs on new user registration
    username_uid = keycloak_admin.get_user_id(username)
    user = keycloak_admin.get_user(username_uid)
    if 'jupyterhubCheck' in user['attributes']:
        return

    users = keycloak_admin.get_users()
    for user in users:
        uid = user.get('attributes', {}).get('uidNumber')
        if uid:
            current_uids.add(int(uid[0]))

    for user in users:
        if 'jupyterhubCheck' in user['attributes']:
            continue

        payload = user
        payload['attributes']['jupyterhubCheck'] = 'true'
        payload['attributes']['homeDirectory'] = f"/home/{user['username']}"

        initial_uid = (hash(user['username']) % (max_uid - min_uid)) + min_uid
        while initial_uid in current_uids:
            initial_uid = ((initial_uid + 1 - min_uid) % (max_uid - min_uid)) + min_uid
        payload['attributes']['uidNumber'] = str(initial_uid)
        current_uids.add(initial_uid)

        keycloak_admin.update_user(user['id'], payload)


class QHubAuthenticator(GenericOAuthenticator):
    async def authenticate(self, handler, data):
        user = await super().authenticate(handler, data)
        if user is None:
            return user
        sync_users(user['name'])
        return user


c.JupyterHub.authenticator_class = QHubAuthenticator

# -------------------- Base Spawner --------------------

class QHubHPCSpawnerBase(SlurmSpawner):
    req_conda_environment_prefix = Unicode('',
        help="Conda environment prefix to launch jupyterlab"
    ).tag(config=True)

    batch_script = Union(
        trait_types=[Unicode(), Callable(),],
        help="Script to be run by the batch system to start the single-user server",
        config=True
    )

    # This already exists in batchspawner, but we need to override
    async def _get_batch_script(self, **subvars):
        """Format batch script from vars"""

        if callable(self.batch_script):
            self.batch_script = await maybe_future(self.batch_script(self))

        # Could be overridden by subclasses, but mainly useful for testing
        return format_template(self.batch_script, **subvars)

# Assign Qhub Spawner
class QHubHPCSpawner(QHubHPCSpawnerBase):
    pass

c.JupyterHub.allow_named_servers = True
c.JupyterHub.default_url = '/hub/home'

c.JupyterHub.template_paths = []
c.JupyterHub.extra_handlers = []

c.JupyterHub.spawner_class = 'wrapspawner.ProfilesSpawner'

c.SlurmSpawner.start_timeout = {{ jupyterhub_config.spawner.start_timeout }}
c.QHubHPCSpawner.default_url = '/lab'

# default values for batch spawner
c.QHubHPCSpawner.req_memory = '1' # GB
c.QHubHPCSpawner.req_nprocs = '1'
c.QHubHPCSpawner.req_partition = 'general'
c.QHubHPCSpawner.req_conda_environment_prefix = '{{ miniforge_home }}/envs/{{ jupyterhub_lab_environment | basename | splitext | first }}'
c.QHubHPCSpawner.req_prologue = '''
# ensure user has link to the shared directory, if it exists
if [ -d "/shared" ] && [ ! -L "$HOME/share" ]; then
  ln -s /shared "$HOME/share"
fi

echo "Ensure home directory $HOME is private"
# This will remove read, write, execute permissions from the group and other users.
# It will not change permissions for the user that owns the file.
chmod go-rwx $HOME

# ensure ipyparallel configuration profiles
cp -r /etc/jupyter/profile_default $HOME/.ipython/

export PATH={{ miniforge_home }}/condabin:$PATH
'''

def populate_condarc(username):
    """Generate condarc configuration string for the given username."""
    condarc = json.dumps({
        "envs_dirs": [
            f"/opt/conda-store/conda-store/{dir_name}/envs" for dir_name in [username, "filesystem"]
        ]
    })
    return f"printf '{condarc}' > /home/{username}/.condarc\n"

@gen.coroutine
def generate_batch_script(spawner):
    """Generate a batch script for SLURM and JupyterHub based on spawner settings."""
    username = spawner.user.name

    auth_state = yield spawner.user.get_auth_state()
    if auth_state:
        print(f"auth_state: {auth_state}")
        print("#######################")

    print(f"Generating batch script for {username}")

    sbatch_headers = dedent("""\
        #!/bin/bash
        {% raw %}
        #SBATCH --output={{homedir}}/.jupyterhub_slurmspawner_%j.log
        #SBATCH --error={{homedir}}/.jupyterhub_slurmspawner_%j.log
        #SBATCH --job-name=spawner-jupyterhub
        #SBATCH --chdir={{homedir}}
        #SBATCH --export={{keepvars}}
        #SBATCH --get-user-env=L
        {% if partition %}#SBATCH --partition={{partition}}
        {% endif %}{% if runtime %}#SBATCH --time={{runtime}}
        {% endif %}{% if memory %}#SBATCH --mem={{memory}}G
        {% endif %}{% if gres %}#SBATCH --gres={{gres}}
        {% endif %}{% if nprocs %}#SBATCH --cpus-per-task={{nprocs}}
        {% endif %}{% if reservation%}#SBATCH --reservation={{reservation}}
        {% endif %}{% if options %}#SBATCH {{options}}{% endif %}
        set -euo pipefail
        trap 'echo SIGTERM received' TERM
        {{prologue}}
        {% endraw %}
    """)

    conda_store_headers = dedent("""\
        {% if conda_store_enabled %}
        # Setting Conda-Store configuration
        mkdir -p "$HOME/.jupyter/lab/user-settings/@mamba-org/gator-lab/"
        echo '{"condaStoreUrl": "/conda-store"}' > $HOME/.jupyter/lab/user-settings/@mamba-org/gator-lab/plugin.jupyterlab-settings

        # Setting nb_conda_kernels settings
        echo '{"CondaKernelSpecManager": {"name_format": "{environment}"}}' > $HOME/.jupyter/jupyter_config.json
        {% endif %}

        export PATH={{ '{{ conda_environment_prefix }}' }}/bin:$PATH
    """)

    srun_jupyterhub_single_user = dedent("""\
        {% raw %}
        which jupyterhub-singleuser
        echo "running command {{cmd}}"
        {% if srun %}{{srun}} {% endif %}{{cmd}}
        echo "jupyterhub-singleuser ended gracefully"
        {{epilogue}}
        {% endraw %}
    """)

    return "".join([
        sbatch_headers,
        populate_condarc(username),
        conda_store_headers,
        srun_jupyterhub_single_user
    ])

c.QHubHPCSpawner.batch_script = generate_batch_script

USER_PROFILES = {{ jupyterhub_profiles | tojson }}

def set_profiles(user_profiles: list):
    """Set the profiles for the ProfilesSpawner."""
    profiles = []
    for profile_dict in user_profiles:
        profile_name, profile_data = next(iter(profile_dict.items()))
        profiles.append((
            profile_data['display_name'],
            profile_name,
            QHubHPCSpawner,
            dict(**profile_data['options'])
        ))
    return profiles


# User profiles
c.ProfilesSpawner.profiles = set_profiles(USER_PROFILES)

# ===== adding api tokens for external services =======
c.JupyterHub.services = [
{% if idle_culler.enabled %}
   {
        'name': 'idle-culler',
        'admin': True,
        'command': [
            sys.executable,
            '-m', 'jupyterhub_idle_culler',
            '--timeout={{ idle_culler.timeout }}',
            '--cull-every={{ idle_culler.cull_every }}',
            '--remove-named-servers',
        ],
    },
{% endif %}
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
import nebari_jupyterhub_theme

c.JupyterHub.extra_handlers = [
    (r'/custom/(.*)', tornado.web.StaticFileHandler, {"path": nebari_jupyterhub_theme.STATIC_PATH}),
] + c.JupyterHub.extra_handlers

c.JupyterHub.template_paths = [
    nebari_jupyterhub_theme.TEMPLATE_PATH
] + c.JupyterHub.template_paths

c.JupyterHub.template_vars = {
{% for key, value in jupyterhub_theme.template_vars.items() %}
    '{{ key }}': '{{ value }}',
{% endfor %}
}

# ======================= CUSTOM ==================
jupyterhub_custom = json.loads('{{ jupyterhub_custom | tojson }}')
for classname, attributes in jupyterhub_custom.items():
    for attribute, value in attributes.items():
        setattr(getattr(c, classname), attribute, value)

# =================== ADDITIONAL FILES ====================
# https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/main/jupyterhub/files/hub/jupyterhub_config.py#L459
# load /etc/jupyterhub/additional config files
config_dir = "/etc/jupyterhub/additional/"
if os.path.isdir(config_dir):
    for file_path in sorted(glob.glob(f"{config_dir}/*.py")):
        file_name = os.path.basename(file_path)
        print(f"Loading {config_dir} config: {file_name}")
        with open(file_path) as f:
            file_content = f.read()
        # compiling makes debugging easier: https://stackoverflow.com/a/437857
        exec(compile(source=file_content, filename=file_name, mode="exec"))
