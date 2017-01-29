#!/bin/sh
#
# Time-stamp: <2017-01-29 13:54:13 alex>
# 
# script to reduce an img file from the raw copy of the PI flash disk
# in order to copy quiclky on a new SD card of the same size
#
# v1
#
# --------------------------------------------------------------------
# PiProbe
# Copyright (C) 2016-2017  Alexandre Chauvin Hameau <ach@meta-x.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later 
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

if [ "$1x" == "x" ]
then
  echo "usage: $0 [file.img]"
  exit
fi

file=$1

function end {
    if [ "${lo}x" != "x" ]; then
	echo "INFO: suppress ${lo} loopback"
	losetup -d ${lo}
    fi

    rm -f /tmp/fsck.$$

    echo "exiting..."
    exit
}

# get start of the ext4 partition, the first one is a FAT
ext4_num=`parted -m $file unit B print | awk -F: '/ext4/ { print $1 }'`

# get start of the ext4 partition, the first one is a FAT
ext4_start=`parted -m $file unit B print | awk -F: '/ext4/ { print $2 }' | tr -d 'B'`
echo $ext4_start

if [ ${ext4_start} -lt 25000000 ]; then
    echo "ERROR : parted error : cannot find the ext4 partition"
    parted $file print
    exit
fi

echo "INFO: found start of the ext4 partition at $ext4_start"

# mount the ext4 partition
lo=`losetup -f --show -o ${ext4_start} ${file}`

losetup -l | fgrep ${lo} > /dev/null
if [ $? != 0 ]; then
    echo "ERROR: cannot mount the ext4 partition in a loopback"
    exit
fi

echo "INFO: loop used is ${lo}"

echo "* check FS"

fsck.ext4 -p -v -f ${lo} > /tmp/fsck.$$ 2>&1

if [ $? != 0 ]; then
    echo "ERROR: fsck reported error"
    cat /tmp/fsck.$$
    end
fi

echo "* estimate best new size for partition"

# get block size
block_size=`tune2fs -l ${lo} | awk -F: '/Block size/ {gsub(/[[:space:]]*/,"",$2); print $2 }'`
if [ ${block_size} -lt 512 ]; then
    echo "ERROR: bad block size"
    end
fi

echo "INFO: block size = ${block_size}"

best_size=`resize2fs -P ${lo} 2>&1 | awk -F: '{if ($0 !~ /resize2fs/) {gsub(/[[:space:]]*/,"",$2); print $2}}'`
echo "INFO: best size reported for FS : ${best_size} blocks"

# opt_size=`expr 2 \* ${best_size}`
opt_size=`expr 1024 \* 32 + ${best_size}`
echo "INFO: new size for ext4 estimated to ${opt_size} blocks"

echo "* resize the FS"

resize2fs -p ${lo} ${opt_size}

ext4_end=`expr ${ext4_start} + ${block_size} \* ${opt_size}`
echo "INFO: end of new ext4 partition : ${ext4_end}"

echo "* disconnect partition"
losetup -d ${lo}
lo=""

echo "* resize file"

echo "  - suppress partition ${ext4_num}"
parted ${file} rm ${ext4_num}

echo "  - recreate partition"
parted -s ${file} unit B mkpart primary ext4 ${ext4_start} ${ext4_end}

shrink_size=`expr ${ext4_end} + 1024 \* ${block_size}`
echo "  - shrink file at ${shrink_size}"

truncate -s ${shrink_size} ${file}

lo=`losetup -f --show -o ${ext4_start} ${file}`
fsck.ext4 -n -f ${lo}
losetup -d ${lo}
lo=""

end
