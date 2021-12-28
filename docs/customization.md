# Custom TLS Certificate

By default, traefik will create and use a self signed TLS certificate for user communication.  If desired, a custom TLS Certificate can be copied from the ansible controller node to the appropriate location for use by traefik.  To do so, set the following settings in the all.yaml file.

```yaml
traefik:
  ... # other variables defined
  tls:
    certificate: /path/to/MyCertificate.crt
    key: /path/to/MyKey.key
```