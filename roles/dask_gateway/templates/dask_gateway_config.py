import subprocess
import json
import os

from dask_gateway_server.options import Options, Integer, Float, Select

c.DaskGateway.backend_class = (
    "dask_gateway_server.backends.jobqueue.slurm.SlurmBackend"
)

c.JobQueueBackend.dask_gateway_jobqueue_launcher = "{{ miniforge_home }}/envs/{{ dask_gateway_environment | basename | splitext | first }}/bin/dask-gateway-jobqueue-launcher"

c.Proxy.address = ':{{ dask_gateway_api_port }}'
c.Proxy.tcp_address = ':{{ dask_gateway_scheduler_internal_port }}'

# Authentication
c.DaskGateway.authenticator_class = "dask_gateway_server.auth.JupyterHubAuthenticator"
c.JupyterHubAuthenticator.jupyterhub_api_token = "{{ jupyterhub_services.dask_gateway }}"
c.JupyterHubAuthenticator.jupyterhub_api_url = "http://localhost:{{ jupyterhub_proxy_port }}/hub/api"


# Find all conda environments that have dask distributed installed
def dask_distributed_environments():
    dask_environments = []
    output = subprocess.check_output(['conda', 'env', 'list', '--json'])
    environments = json.loads(output)['envs']
    for environment in environments:
        output = subprocess.check_output(['conda', 'list', '-p', environment, '--json'])
        if 'distributed' in {_['name'] for _ in json.loads(output)}:
            dask_environments.append((os.path.basename(environment), environment))
    return dask_environments


# ================= Dask Gateway Options ===============
def options_handler(options):
    return {
        "worker_cores": options.worker_cores,
        "worker_memory": int(options.worker_memory * 2 ** 30),
        "scheduler_cores": options.scheduler_cores,
        "scheduler_memory": int(options.scheduler_memory * 2 ** 30),
        "scheduler_cmd": f'{options.environment}/bin/dask-scheduler',
        "worker_cmd": f'{options.environment}/bin/dask-worker',
        "partition": options.partition
    }

c.Backend.cluster_options = Options(
    Integer("worker_cores", default=1, min=1, max=4, label="Worker Cores"),
    Float("worker_memory", default=1, min=1, max=8, label="Worker Memory (GiB)"),
    Integer("scheduler_cores", default=1, min=1, max=2, label="Scheduler Cores"),
    Float("scheduler_memory", default=1, min=1, max=4, label="Scheduler Memory (GiB)"),
    Select("environment", dask_distributed_environments(), default="{{ jupyterhub_lab_environment | basename | splitext | first }}", label="Dask Conda Environment"),
    Select("partition", ['general',
{%- for item in groups -%}
{%- if item.startswith('partition-')-%}'{{ item[10:] }}', {% endif -%}
{%- endfor -%}], default="general", label="Slurm Partition"),
    handler=options_handler,
)
