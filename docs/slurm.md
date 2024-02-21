# Slurm

For detailed slurm information please refer to the
[documentation](https://slurm.schedmd.com/overview.html).

## Checking Health of Slurm Cluster

[sinfo](https://slurm.schedmd.com/sinfo.html) is your bread and butter
and should be used to quickly check the health of the cluster.

```shell
sinfo
```

```shell
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
general*     up   infinite      1    mix hpc02-test
general*     up   infinite      2   idle hpc03-test,hpc04-test
```

## Get current job queue including running jobs

```shell
squeue
```

## Getting information about a job

```shell
scontrol show job <job-id>
```

```shell
JobId=37 JobName=spawner-jupyterhub
   UserId=vagrant(1000) GroupId=vagrant(1000) MCS_label=N/A
   Priority=4294901724 Nice=0 Account=(null) QOS=normal
   JobState=RUNNING Reason=None Dependency=(null)
   Requeue=1 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0
   RunTime=00:01:16 TimeLimit=UNLIMITED TimeMin=N/A
   SubmitTime=2021-01-19T14:27:24 EligibleTime=2021-01-19T14:27:24
   AccrueTime=2021-01-19T14:27:24
   StartTime=2021-01-19T14:27:24 EndTime=Unknown Deadline=N/A
   SuspendTime=None SecsPreSuspend=0 LastSchedEval=2021-01-19T14:27:24
   Partition=general AllocNode:Sid=localhost:135266
   ReqNodeList=(null) ExcNodeList=(null)
   NodeList=hpc02-test
   BatchHost=hpc02-test
   NumNodes=1 NumCPUs=1 NumTasks=1 CPUs/Task=1 ReqB:S:C:T=0:0:*:*
   TRES=cpu=1,mem=1G,node=1,billing=1
   Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
   MinCPUsNode=1 MinMemoryNode=1G MinTmpDiskNode=0
   Features=(null) DelayBoot=00:00:00
   OverSubscribe=OK Contiguous=0 Licenses=(null) Network=(null)
   Command=(null)
   WorkDir=/home/vagrant
   StdErr=/home/vagrant/.jupyterhub_slurmspawner_37.log
   StdIn=/dev/null
   StdOut=/home/vagrant/.jupyterhub_slurmspawner_37.log
   Power=
```

## Configuring and adding node information

For each node create a `host_vars/<node-name>.yaml` and omit any
fields if you want to use the default value. Suppose the following
configuration for `host_vars/hpc02-test.yaml`.

```yaml
slurm_memory: 7976         # RealMemory (default 1024)
slurm_cpus: 4              # CPUs (default 1)
slurm_boards: 1            # Boards (default 1)
slurm_sockets_per_board: 4 # SocketsPerBoard (default 1)
slurm_cores_per_socket: 1  # CoresPerSocket (default 1)
slurm_threads_per_core: 1  # ThreadsPerCore (default 1)
```

Would result in the following slurm node configuration

```init
# Nodes
NodeName=hpc02-test RealMemory=7976 CPUs=4 Boards=1 SocketsPerBoard=4 CoresPerSocket=1 ThreadsPerCore=1 State=UNKNOWN
```

You can get the detailed node specs via slurmd and can be used to
easily set the node configuration. The more accurately that you set
the node information for slurm the more accurately users can target
their programs on the hardware.

```shell
slurmd -C
```

```shell
NodeName=hpc02-test CPUs=4 Boards=1 SocketsPerBoard=4 CoresPerSocket=1 ThreadsPerCore=1 RealMemory=7976
UpTime=0-01:46:52
```

If you have set an incorrect configuration, the nodes may enter a
DRAIN state with low cores*sockets*threads and memory error. You will
then need to modify the node state to IDLE once it is properly
configured.

## Modifying Node State

There are several common cases where one would need to manually change
the node state. All slurm managment is done via the `sacct` and
`scontrol` command. In this case we need to use `scontrol` command.

```shell
scontrol update nodename=<node-name> state=IDLE
```

This is useful if you want to resume a node for operation.

## Node States

The full list of [node
states](https://slurm.schedmd.com/sinfo.html#lbAG). Here we outline
some of the common ones.

- ALLOCATED :: node is completely consumed
- MIXED :: node is partially consumed
- IDLE :: node is idle and has no running jobs
- DRAIN :: node is unable to schedule new jobs but running jobs will finish

## Adding Slurm Partitions

Partitions in slurm can easily be created via ansible groups. Any
group start starts with `partition-`. For example

```ini
[hpc_master]
hpc01-test

[hpc_worker]
hpc02-test
hpc03-test
hpc04-test

[partition_example]
hpc02-test
hpc04-test
```

Will create the following slurm partitions

```ini
# Partitions
PartitionName=general Nodes=hpc02-test,hpc03-test,hpc04-test Default=YES MaxTime=INFINITE State=UP
PartitionName=example Nodes=hpc02-test,hpc04-test Default=NO MaxTime=INFINITE State=UP
```
