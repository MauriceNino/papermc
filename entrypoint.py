import os

import requests
from packaging.version import parse as parse_version

DEFAULT_FLAGS = '-Dcom.mojang.eula.agree=true'

# https://krusic22.com/2020/03/25/higher-performance-crafting-using-jdk11-and-zgc/
KRUSIC_FLAGS = '-XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:-UseParallelGC -XX:-UseParallelOldGC '
'-XX:-UseG1GC -XX:+UseZGC'

# https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/
AIKARS_FLAGS = '-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions '
'-XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M '
'-XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 '
'-XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem '
'-XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true'

# Initialize passed env variables
MC_PAPER_VERSION = os.getenv('MC_PAPER_VERSION') or 'latest'
MC_PAPER_BUILD = os.getenv('MC_PAPER_BUILD') or 'latest'
MC_RAM_MIN = os.getenv('MC_RAM_MIN') or os.getenv('MC_RAM')
MC_RAM_MAX = os.getenv('MC_RAM_MAX') or os.getenv('MC_RAM')
MC_JAVA_OPTS = os.getenv('MC_JAVA_OPTS') or KRUSIC_FLAGS if os.getenv('MC_USE_KRUSIC_FLAGS') == 'true' else AIKARS_FLAGS
MC_EXTRA_JAVA_OPTS = os.getenv('MC_EXTRA_JAVA_OPTS') or ''
MC_PAPER_ARGS = os.getenv('MC_PAPER_ARGS') or ''

USER_ID = int(os.getenv('PUID') or 2000)
GROUP_ID = int(os.getenv('PGID') or 2000)

if MC_RAM_MIN is not None:
  MC_JAVA_OPTS = f'{MC_JAVA_OPTS} -Xms{MC_RAM_MIN}'

if MC_RAM_MAX is not None:
  MC_JAVA_OPTS = f'{MC_JAVA_OPTS} -Xmx{MC_RAM_MAX}'
  
MC_JAVA_OPTS = f'{MC_JAVA_OPTS} {MC_EXTRA_JAVA_OPTS} {DEFAULT_FLAGS}'

# Determine correct version and build
paperUrl = 'https://papermc.io/api/v2/projects/paper'

if MC_PAPER_VERSION == 'latest':
  MC_PAPER_VERSION = requests.get(paperUrl).json()['versions'][-1]

if MC_PAPER_BUILD == 'latest':
  MC_PAPER_BUILD = requests.get(f'{paperUrl}/versions/{MC_PAPER_VERSION}').json()['builds'][-1]

# Download correct paper version & setup local env
paperJarFolder = f'/paper/{MC_PAPER_VERSION}'

if not os.path.exists(paperJarFolder):
  os.makedirs(paperJarFolder)
  
paperJar = f'paper-{MC_PAPER_VERSION}-{MC_PAPER_BUILD}.jar'
paperJarUrl = f'{paperUrl}/versions/{MC_PAPER_VERSION}/builds/{MC_PAPER_BUILD}/downloads/{paperJar}'
paperJarFile = os.path.join(paperJarFolder, f'{MC_PAPER_VERSION}-{MC_PAPER_BUILD}.jar')

if not os.path.isfile(paperJarFile):
  open(paperJarFile, 'wb').write(requests.get(paperJarUrl).content)

# Handle file permissions & change user
os.system(f'addgroup -g {GROUP_ID} paper')
os.system(f'adduser -u {USER_ID} -G paper -H -D paper')

os.system(f'chown {USER_ID}:{GROUP_ID} /data')
os.chdir('/data')
os.setgid(GROUP_ID)
os.setuid(USER_ID)

# Determine correct Java Version
javaExec = '/usr/lib/jvm/java-17-openjdk/bin/java'

paperMajor = parse_version(MC_PAPER_VERSION)
if paperMajor < parse_version("1.17"):
  javaExec = '/usr/lib/jvm/java-11-openjdk/bin/java'
if paperMajor < parse_version("1.14"):
  javaExec = '/usr/lib/jvm/java-8-openjdk/bin/java'

# Start the server
startCommand = f'{javaExec} -server {MC_JAVA_OPTS} -jar {paperJarFile} {MC_PAPER_ARGS} nogui'
print(' '.join(startCommand.split()))
os.execvp(javaExec, startCommand.split())

# not reached
os._exit(127)