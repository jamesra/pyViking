#!/bin/bash

/opt/nvidia/nvidia_entrypoint.sh
sudo service ssh start
python3 -m segmentation_grpc
python3 -m segmentation_server
exec "$@"