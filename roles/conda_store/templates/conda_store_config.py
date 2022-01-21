import logging

from conda_store_server.storage import S3Storage
from conda_store_server.server.auth import GenericOAuthAuthentication

# ==================================
#      conda-store settings
# ==================================
c.CondaStore.storage_class = S3Storage
c.CondaStore.store_directory = "/opt/conda-store/conda-store/"
c.CondaStore.environment_directory = "/opt/conda-store/envs/"
c.CondaStore.conda_command = "conda"
c.CondaStore.database_url = "mysql+pymysql://{{ mysql_users[1].username }}:{{ mysql_users[1].password }}@localhost/{{ mysql_databases[1] }}"
c.CondaStore.default_uid = 1000
c.CondaStore.default_gid = 100
c.CondaStore.default_permissions = "775"

c.S3Storage.internal_endpoint = "localhost:{{ minio_port }}"
c.S3Storage.external_endpoint = "{{ lookup('vars', 'ansible_' + internal_interface, 'ipv4', 'address') }}:{{ minio_port }}"
c.S3Storage.access_key = "{{ minio_username }}"
c.S3Storage.secret_key = "{{ minio_password }}"
c.S3Storage.region = "us-east-1"  # minio region default
c.S3Storage.bucket_name = "conda-store"
c.S3Storage.secure = False

# ==================================
#        server settings
# ==================================
c.CondaStoreServer.log_level = logging.INFO
c.CondaStoreServer.enable_ui = True
c.CondaStoreServer.enable_api = True
c.CondaStoreServer.enable_registry = True
c.CondaStoreServer.enable_metrics = True
c.CondaStoreServer.address = "0.0.0.0"
c.CondaStoreServer.port = {{ conda_store_port }}
c.CondaStoreServer.url_prefix = "{{ conda_store_prefix }}"


# ==================================
#         auth settings
# ==================================
c.GenericOAuthAuthentication.access_token_url = "https://{{ traefik_domain | default(hostvars[groups['hpc-master'][0]].ansible_host) }}/auth/realms/{{ keycloak_realm }}/protocol/openid-connect/token"
c.GenericOAuthAuthentication.authorize_url = "https://{{ traefik_domain | default(hostvars[groups['hpc-master'][0]].ansible_host) }}/auth/realms/{{ keycloak_realm }}/protocol/openid-connect/auth"
c.GenericOAuthAuthentication.user_data_url = "https://{{ traefik_domain | default(hostvars[groups['hpc-master'][0]].ansible_host) }}/auth/realms/{{ keycloak_realm }}/protocol/openid-connect/userinfo"
c.GenericOAuthAuthentication.oauth_callback_url = "https://{{ traefik_domain | default(hostvars[groups['hpc-master'][0]].ansible_host) }}/conda-store/oauth_callback"
c.GenericOAuthAuthentication.client_id = "{{ conda_store_client_id }}"
c.GenericOAuthAuthentication.client_secret = "{{ conda_store_client_secret }}"
c.GenericOAuthAuthentication.access_scope = "profile"
c.GenericOAuthAuthentication.user_data_key = "preferred_username"
c.GenericOAuthAuthentication.tls_verify = False

import requests
from conda_store_server import schema, api, orm
from conda_store_server.server.utils import get_conda_store

class KeyCloakAuthentication(GenericOAuthAuthentication):
    def authenticate(self, request):
        # 1. using the callback_url code and state in request
        oauth_access_token = self._get_oauth_token(request)
        if oauth_access_token is None:
            return None  # authentication failed

        response = requests.get(
            self.user_data_url,
            headers={"Authorization": f"Bearer {oauth_access_token}"},
            verify=self.tls_verify,
        )
        response.raise_for_status()
        user_data = response.json()

        role_mappings = {
            'conda_store_admin': 'admin',
            'conda_store_developer': 'developer',
            'conda_store_viewer': 'viewer',
        }
        roles = {role_mappings[role] for role in user_data.get('roles', []) if role in role_mappings}
        username = user_data['preferred_username']
        namespaces = {username, 'default', 'filesystem'}
        role_bindings = {
            f'{username}/*': {'admin'},
            f'filesystem/*': {'reader'},
            f'default/*': roles,
        }

        for group in user_data.get('groups', []):
            namespaces.add(group)
            role_bindings[f'{group}/*'] = roles

        conda_store = get_conda_store()
        for namespace in namespaces:
            _namespace = api.get_namespace(conda_store.db, name=namespace)
            if _namespace is None:
                conda_store.db.add(orm.Namespace(name=namespace))
                conda_store.db.commit()

        return schema.AuthenticationToken(
            primary_namespace=username,
            role_bindings=role_bindings,
        )

c.CondaStoreServer.authentication_class = KeyCloakAuthentication

# ==================================
#         worker settings
# ==================================
c.CondaStoreWorker.log_level = logging.INFO
c.CondaStoreWorker.watch_paths = ["/opt/environments"]
