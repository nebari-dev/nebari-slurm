# Backup

Backups are performed in QHub HPC via [restic](https://restic.net/)
an open source backup tool. It is extremely flexible on where backups
are performed as well as supporting encrypted, incremental backups.

## Configuration

The following shows a daily backup on S3 for QHub.

```yaml
backup:
  enabled: false
  on_calendar: "daily"
  randomized_delay: "3600"
  environment:
    RESTIC_REPOSITORY: "s3:s3.amazonaws.com/bucket_name"
    RESTIC_PASSWORD: "thisismyencryptionkey"
    AWS_ACCESS_KEY_ID: accesskey
    AWS_SECRET_ACCESS_KEY: mylongsecretaccesskey
```

 - enabled :: determines whether backups are enabled
 - on_calendar :: determines the frequency to perform backups. Consult [systemd timer](https://www.freedesktop.org/software/systemd/man/systemd.timer.html) documentation for syntax
 - randomized_delay :: is the random delay in seconds to apply to backups. Usefull to prevent backups from all being performed at an exact time each day
  - environment :: are all the key value pairs used to configure restic. RESTIC_REPOSITORY and RESTIC_PASSWORD are required. The rest are environment variables for the specific [backup repository](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html).

## Manual Backup

At any time you can trigger a manual backup. SSH into the master node.

```shell
sudo systemctl start restic-backup.service
```
