# PaperMC

This a Linux based Docker image, which provides a [PaperMC](https://papermc.io/) Minecraft server.
It is compatible with ARM and x64, supports all valid PaperMC versions (`1.8.8` - `1.19`), and will be maintained in the future.

<!--
The following versions were tested and determined to work:
`1.19`, `1.18`, `1.17.1`, `1.16.1`, `1.15`, `1.14`, `1.13`, `1.12.2`, `1.11.2`, `1.10.2`, `1.9.4`, `1.8.8`
--->

## Usage

You need to have a working docker install on your system. If you are unsure how to do that, please consult the [official docs](https://docs.docker.com/get-docker/).
Running this docker image means that you must adhere to the TOS of [Mojang/Minecraft](https://www.minecraft.net/en-us/terms) and that you agree to the [Minecraft EULA](https://www.minecraft.net/en-us/eula).

### Docker

```sh
docker container run -it \
  -v minecraft:data \
  -p 25565:25565 \
  -e MC_RAM "2G" \
  --restart unless-stopped \
  mauricenino/papermc
```

> The config variable `-e MC_RAM "2G"` is just an example. Please use your own config and have a look at the [Options](#options) for additional configuration options.

### Docker-Compose

```yml
version: "3.5"

services:
  minecraft:
    image: mauricenino/papermc
    restart: unless-stopped
    ports:
      - 25565:25565
    volumes:
      - minecraft:data
    environment:
      MC_RAM: "2G"
```

> The config variable `MC_RAM: "2G"` is just an example. Please use your own config and have a look at the [Options](#options) for additional configuration options.

## Options

| Variable            | Default                                                                                                | Option                                                                                                                                                                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MC_PAPER_VERSION    | `latest`                                                                                               | Any valid Minecraft version, that has a [PaperMC version](https://papermc.io/api/v2/projects/paper) released                                                                                                                                       |
| MC_PAPER_BUILD      | `latest`                                                                                               | Any valid PaperMC Build for the given version                                                                                                                                                                                                      |
| MC_RAM              |                                                                                                        | The amount of Memory you want to assign to your minecraft server (e.g. `2G`)                                                                                                                                                                       |
| MC_RAM_MIN          |                                                                                                        | Specify min-max values for the assigned Memory (not recommended)                                                                                                                                                                                   |
| MC_RAM_MAX          |                                                                                                        | Specify min-max values for the assigned Memory (not recommended)                                                                                                                                                                                   |
| MC_JAVA_OPTS        | [Aikars Flags](https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/) | Override the flags that are being passed to the JVM                                                                                                                                                                                                |
| MC_EXTRA_JAVA_OPTS  |                                                                                                        | Append to the flags that are being passed to the JVM                                                                                                                                                                                               |
| MC_USE_KRUSIC_FLAGS | `false`                                                                                                | Set to `true` if you want to replace `MC_JAVA_OPTS` with [Krusics Flags](https://krusic22.com/2020/03/25/higher-performance-crafting-using-jdk11-and-zgc/), which are said to be more performant for servers with a lot of RAM available (> 20 GB) |
| MC_PAPER_ARGS       |                                                                                                        | Can be any valid startup argument for your PaperMC server ([list](https://www.spigotmc.org/wiki/start-up-parameters/))                                                                                                                             |
| PUID                | `2000`                                                                                                 | A custom user id - mostly used for file permissions                                                                                                                                                                                                |
| PGID                | `2000`                                                                                                 | A custom group id - mostly used for file permissions                                                                                                                                                                                               |
| TZ                  |                                                                                                        | A custom timezone (e.g. `Europe/Vienna`) - to make the timestamps appear in the correct timezone                                                                                                                                                   |
