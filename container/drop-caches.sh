#!/bin/bash
sync
sudo sh -c "echo 1 > /proc/sys/vm/drop_caches"
sync
sudo sh -c "echo 2 > /proc/sys/vm/drop_caches"
sync
sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"
