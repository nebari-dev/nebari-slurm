# Frequently Asked Questions

## Why on-prem hpc instead of kubernetes?

We have eventual plans for supporting existing on-prem kubernetes
deployments in [issue
#216](https://github.com/Quansight/qhub/issues/216). HPC still has
many advantages over kubernetes:
 - simplicity as it following a more traditional linux and systemd
   making it easier to diagnose errors
 - can deployed to take advantage of pre-provisioned existing
   infrastructure
 - **TODO** still possible to support containerized workflows
 - can fully take advantage of HPC infrastructure in on-prem
   datacenter

