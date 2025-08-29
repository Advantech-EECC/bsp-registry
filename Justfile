# loads .env file from the current working dir
#
# minimal .env contents could be 
#
# KAS_WORKDIR=$PWD
# KAS_CONTAINER_ENGINE=docker
# KAS_CONTAINER_IMAGE=<docker-image-tag>
# GITCONFIG_FILE=<user-home-dir>/.gitconfig
# DL_DIR=<user-home-dir>/cache/downloads/
# SSTATE_DIR=<user-home-dir>/cache/sstate/ 
#
set dotenv-load

repo_root := absolute_path(justfile_directory())
repo_name := file_name(repo_root)

dotenv := repo_root / ".env"

kas_build_args := "--provenance=true"

# Print available commands
help:
    just --list --unsorted

# Populate .env file 
[group('docker')]
env distro="debian:12":
    echo " \
    # generated automatically, to adjust change env rule in the Justfile \n \
    KAS_WORKDIR=$PWD\n \
    KAS_CONTAINER_ENGINE=docker\n \
    KAS_CONTAINER_IMAGE=advantech/bsp-registry/{{distro}}\n \
    GITCONFIG_FILE=${HOME}/.gitconfig\n \
    DL_DIR=${HOME}/data/cache/downloads/\n \
    SSTATE_DIR=${HOME}/data/cache/sstate/\n \
    " > .env

# Build official KAS Docker image based on Debian Linux
[group('docker')]
docker-debian distro="debian:12": (env distro)
    docker build -f Dockerfile.debian -t advantech/bsp-registry/{{distro}} .

# Build KAS Docker image based on Ubuntu Linux
[group('docker')]
docker-ubuntu distro="ubuntu:20.04" kas="4.7": (env distro)
    docker build -f Dockerfile.ubuntu -t advantech/bsp-registry/{{distro}} --build-arg DISTRO="{{distro}}" --build-arg KAS_VERSION="{{kas}}" .

# Build a Yocto BSP for a specified machine
[group('yocto')]
yocto action="build" bsp="mbsp" machine="rsb3720" version="walnascar" docker="ubuntu:22.04" kas="5.0" args="": (docker-ubuntu docker kas)
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-{{bsp}}-{{version}}-{{machine}}" kas-container {{action}} {{args}} adv-{{bsp}}-oenxp-{{version}}-{{machine}}.yaml    

# Build Yocto Walnascar BSP for a specified machine
[group('yocto')]
walnascar bsp="mbsp" machine="rsb3720": (docker-ubuntu 'ubuntu:22.04' '5.0')
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-{{bsp}}-walnascar-{{machine}}" kas-container build {{kas_build_args}} adv-{{bsp}}-oenxp-walnascar-{{machine}}.yaml    

#Build Yocto Styhead BSP for a specified machine
[group('yocto')]
styhead bsp="mbsp" machine="rsb3720": (docker-ubuntu 'ubuntu:22.04' '5.0')
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-{{bsp}}-styhead-{{machine}}" kas-container build {{kas_build_args}} adv-{{bsp}}-oenxp-styhead-{{machine}}.yaml    

#Build Yocto Scarthgap BSP for a specified machine
[group('yocto')]
scarthgap bsp="mbsp" machine="rsb3720": (docker-ubuntu 'ubuntu:22.04' '5.0')
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-{{bsp}}-scarthgap-{{machine}}" kas-container build {{kas_build_args}} adv-{{bsp}}-oenxp-scarthgap-{{machine}}.yaml    

#Build Yocto Mickledore BSP for a specified machine
[group('yocto')]
mickledore bsp="bsp" machine="rsb3730": (docker-ubuntu 'ubuntu:20.04' '4.7')
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-{{bsp}}-mickledore-{{machine}}" kas-container build {{kas_build_args}} adv-{{bsp}}-oenxp-mickledore-{{machine}}.yaml    

#Build Yocto Kirkstone BSP for a specified machine
[group('yocto')]
kirkstone bsp="bsp" machine="rsb3720": (docker-ubuntu 'ubuntu:20.04' '4.7')
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-{{bsp}}-kirkstone-{{machine}}" kas-container build {{kas_build_args}} adv-{{bsp}}-oenxp-kirkstone-{{machine}}.yaml    

[group('qemu')]
qemu arch="arm64" yocto="walnascar" docker="ubuntu:22.04" kas="5.0": (docker-ubuntu docker kas)
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-{{yocto}}-qemu{{arch}}" kas-container build yocto/{{yocto}}.yml:compilers/clang/{{yocto}}.yml:yocto/qemu/qemu{{arch}}.yaml    

[group('qemu')]
qemu-shell arch="arm64" yocto="walnascar" docker="ubuntu:22.04" kas="5.0":(docker-ubuntu docker kas)
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-{{yocto}}-qemu{{arch}}" kas-container shell yocto/{{yocto}}.yml:compilers/clang/{{yocto}}.yml:yocto/qemu/qemu{{arch}}.yaml    

#Build BSP for a specified machine
[group('bsp')]
bsp machine="rsb3720" yocto="scarthgap" docker="ubuntu:22.04" kas="5.0": (docker-ubuntu docker kas)
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-bsp-{{yocto}}-{{machine}}" kas-container build {{kas_build_args}} adv-bsp-oenxp-{{yocto}}-{{machine}}.yaml

# Enter a BSP build environment shell for a machine 
[group('bsp')]
bsp-shell machine="rsb3720" yocto="scarthgap" docker="ubuntu:22.04" kas="5.0": (docker-ubuntu docker kas)
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-bsp-{{yocto}}-{{machine}}" kas-container shell adv-bsp-oenxp-{{yocto}}-{{machine}}.yaml

# Build Modular BSP for a specified machine
[group('mbsp')]
mbsp machine="rsb3720" yocto="walnascar": docker-debian
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-mbsp-{{yocto}}-{{machine}}" kas-container build {{kas_build_args}} adv-mbsp-oenxp-{{yocto}}-{{machine}}.yaml

# Enter a "Modular BSP" build environment shell for a machine 
[group('mbsp')]
mbsp-shell machine="rsb3720" yocto="walnascar": docker-debian
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-mbsp-{{yocto}}-{{machine}}" kas-container shell adv-mbsp-oenxp-{{yocto}}-{{machine}}.yaml

# Build Modular BSP with OTA support for a specified machine
[group('ota')]
ota-mbsp machine="rsb3720" ota="rauc" yocto="walnascar": docker-debian
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-ota-{{ota}}-mbsp-{{yocto}}-{{machine}}" kas-container build {{kas_build_args}} adv-mbsp-oenxp-{{yocto}}-{{machine}}.yaml:features/ota/{{ota}}/adv-ota-{{yocto}}.yml

# Enter a "Modular BSP" build environment shell with OTA support for a machine 
[group('ota')]
ota-shell machine="rsb3720" ota="rauc" yocto="walnascar": docker-debian
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-ota-{{ota}}-mbsp-{{yocto}}-{{machine}}" kas-container shell adv-mbsp-oenxp-{{yocto}}-{{machine}}.yaml:features/ota/{{ota}}/adv-ota-{{yocto}}.yml

# Enter a "Modular BSP" build environment shell for a machine 
[group('ros')]
ros-mbsp machine="rsb3720" ros="humble" yocto="walnascar": docker-debian
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-ros-{{ros}}-mbsp-{{yocto}}-{{machine}}" kas-container build {{kas_build_args}} adv-mbsp-oenxp-{{yocto}}-{{machine}}.yaml:features/ros2/{{ros}}.yml

# Enter a "Modular BSP" build environment shell with ROS support for a machine 
[group('ros')]
ros-shell machine="rsb3720" ros="humble" yocto="walnascar": docker-debian
    @. "{{ dotenv }}" && \
    KAS_BUILD_DIR="$PWD/build-ros-{{ros}}-mbsp-{{yocto}}-{{machine}}" kas-container shell adv-mbsp-oenxp-{{yocto}}-{{machine}}.yaml:features/ros2/{{ros}}.yml

mtk-bsp machine yocto:
    @KAS_BUILD_DIR="$PWD/build-mtk-mbsp-{{yocto}}-{{machine}}" kas-container build bsp-oemtk-{{yocto}}-{{machine}}.yaml
