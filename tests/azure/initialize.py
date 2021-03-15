import subprocess
    
def get_host_dict(host_line):
    single_host = host_line.split(' ')[1:]
    host_dict = {_.split('=')[0]: _.split('=')[1] for _ in single_host}
    return host_dict

def get_cpus(host_dict):
    """
    Gets the number of CPUs on the master and worker nodes
    """
    result = subprocess.run(
        ["ssh", "-i", 
         f"{host_dict['ansible_ssh_private_key_file']}", 
         f"{host_dict['ansible_user']}@{host_dict['ansible_host']}", 
         "lscpu"], stdout=subprocess.PIPE
            )
    num_cpus_text = [_ for _ in result.stdout.decode("utf-8").split('\n') if "CPU(s):" in _][0]
    num_cpus = int(''.join([_ for _ in num_cpus_text if _.isnumeric()]))
    
    return num_cpus


def get_mem(host_dict):
    """
    Gets the number of desired MB on the worker nodes. Assumes master and worker are same instance type
    """
    result = subprocess.run(
        ["ssh", "-i", 
         f"{host_dict['ansible_ssh_private_key_file']}", 
         f"{host_dict['ansible_user']}@{host_dict['ansible_host']}", 
         "grep",
         "MemTotal",
         "/proc/meminfo"], stdout=subprocess.PIPE
    )

    mem_KB = int(''.join([_ for _ in result.stdout.decode("utf-8") if _.isnumeric()]))
    slurm_MBs = int(mem_KB / 1000 * .95)
    
    return slurm_MBs


with open("inventory", "r") as f:
    text = f.read()
    
def main():
    host_lines = [_ for _ in text.split('\n') if 'ansible_host' in _]
    host_dict = get_host_dict(host_lines[0])
    num_cpus_int = get_cpus(host_dict)
    slurm_MBs = get_mem(host_dict)

    worker_names = [_ for _ in text.split('[hpc-worker]')[1].split('\n') if _ != '']

    for worker in worker_names:
        with open(f"../../host_vars/{worker}.yaml", "w") as f:
            f.write(
f"""slurm_cpus: {num_cpus_int}
slurm_sockets_per_board: 1
slurm_memory: {slurm_MBs}
""")

if __name__ == "__main__":
    main()
