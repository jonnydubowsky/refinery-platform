#!/bin/sh
# aws.sh

set -x

# This script is intended to be executed on AWS instance after
# the bootstraph.sh script. The bootstrap.sh script is common
# to both Vagrant and AWS. Both bootstrap.sh and aws-docker.sh (this
# script) are supplied via cloudinit userdata.
