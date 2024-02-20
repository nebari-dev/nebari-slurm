# Benchmarking

There are many factors that go into HPC performance. Aside from the
obvious cpu performance network and storage are equally important in a
distributed context.

## Storage

[fio](https://fio.readthedocs.io/en/latest/fio_doc.html) is a powerful
tool for benchmarking filesystems. Measuring maximum performance
especially on extremely high performance filesystems can be tricky to
measure and will require research on how to effectively use the
tool. Often times measuring maximum performance on high performance
distributed filesystems will require multiple nodes and threads for
reading/writing. However it should provide a good ballpark of
performance.

Substitute `<directory>` with the filesystem that you want to
test. `df -h` can be a great way to see where each drive is
mounted. `fio` will need the ability to read/write in the given
directory.

IOPs (input/output operations per second)

### Maximum Write Throughput

```shell
fio --ioengine=sync --direct=0 \
  --fsync_on_close=1 --randrepeat=0 --nrfiles=1  --name=seqwrite --rw=write \
  --bs=1m --size=20G --end_fsync=1 --fallocate=none  --overwrite=0 --numjobs=1 \
  --directory=<directory> --loops=10
```

### Maximum Write IOPs

```shell
fio --ioengine=sync --direct=0 \
  --fsync_on_close=1 --randrepeat=0 --nrfiles=1  --name=randwrite --rw=randwrite \
  --bs=4K --size=1G --end_fsync=1 --fallocate=none  --overwrite=0 --numjobs=80 \
  --sync=1 --directory=<directory> --loops=10
```

### Maximum Read Throughput

```shell
fio --ioengine=sync --direct=0 \
  --fsync_on_close=1 --randrepeat=0 --nrfiles=1  --name=seqread --rw=read \
  --bs=1m --size=240G --end_fsync=1 --fallocate=none  --overwrite=0 --numjobs=1 \
  --directory=<directory> --invalidate=1 --loops=10
```

### Maximum Read IOPs

```shell
fio --ioengine=sync --direct=0 \
  --fsync_on_close=1 --randrepeat=0 --nrfiles=1  --name=randread --rw=randread \
  --bs=4K --size=1G --end_fsync=1 --fallocate=none  --overwrite=0 --numjobs=20 \
  --sync=1 --invalidate=1 --directory=<directory> --loops=10
```

## Network

To test network latency and bandwidth there needs to be a source and
destination that you wish to test. It will expose a given port by
default `5201` with iperf.

### Bandwidth

Start a server on a given `<dest>`

```shell
iperf3 -s
```

No on the `<src>` machine run

```shell
iperf3 -c <ip address>
```

This will measure the bandwidth of the link between the nodes from
`<src>` to `<dest>`. This means that if you are using a provider where
your Internet have very different upload vs. download speeds you will
see very different results in the direction. Add a `-R` flag to the
client to test the other direction.

### Latency

[ping](https://linux.die.net/man/8/ping) is a great way to watch the
latency between `<src>` and `<dest>`.

From the src machine run

```shell
ping -4 <dest> -c 10
```

Keep in mind that ping is the bi-directional (round trip) time. So
dividing by 2 is roughly the latency.

