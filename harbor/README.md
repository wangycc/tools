## harbor api
----

### Building and running

#### Build

```shell
make install
```

#### Running

```shell
./main.py <flags>
```


#### docker

```shell
make docker
```

### USAGE

```shell

usage: main.py [-h] [-d DAY] [--last LAST] [-g GROUP [GROUP ...]] [-l]
               [-u USER] [-p PASSWORD] [--host HOST]

cleanup Harbor registry

optional arguments:
  -h, --help            show this help message and exit
  -d DAY, --day DAY     Only delete tags created before given date.
  --last LAST           Keep last N tags(default: 20)
  -g GROUP [GROUP ...], --group GROUP [GROUP ...]
                        Delete only the repositories of the specified project
                        group
  -l, --list            list all project group
  -u USER, --user USER  harbor user
  -p PASSWORD, --password PASSWORD
                        harbor password
  --host HOST           harbor host
  
 ```

