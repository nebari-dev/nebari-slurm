c.JupyterHubSSH.hub_url = 'http://{{ groups['hpc-master'][0] }}:{{ jupyterhub_port }}'
c.JupyterHubSSH.host_key_path = '/etc/ssh/ssh_host_rsa_key'
c.JupyterHubSSH.port = {{ jupyterhub_ssh_port }}
