# Frequently Asked Questions

Q1: Can a user access another user's home directory in JupyterLab?

No. Every user's home directory is private to themselves and they cannot access contents
of any other user's home directory. Example below shows the permissions of user directories
in `/home`.

```bash
$ ls -ltrh /home

total 36K
drwx------  9 john-doe       example-user 4.0K Apr  1 19:22 john-doe
drwx------  9 alice-doe      example-user 4.0K Apr  1 19:34 alice-doe
```

```bash
john-doe@worker-01:~$ pwd
/home/john-doe

# The user john-doe unable to access contents of user alice-doe's home directory:
john-doer@worker-01:~$ ls /home/alice-doe/
ls: cannot open directory '/home/alice-doe/': Permission denied
```
