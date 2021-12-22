# Accessing Qhub HPC from a Domain

By default, a qhub-hpc deployment must be accesssed using the ip address of the hpc-master node.  However, if a domain name has been set up to point to the hpc-master node, then Qhub HPC's router, [Traefik](https://doc.traefik.io/traefik/), can be configured to work with the domain by setting the **traefik.domain** ansible variable.

For example, if you had the example.com domain set up to point to the hpc-master node, then you could add the following to the all.yaml file and redeploy, after which navigating to https://example.com in a web browser would bring up your Qhub HPC deployment sign in page.

```yaml
traefik:
  ... # other variables defined here
  domain: example.com
```

