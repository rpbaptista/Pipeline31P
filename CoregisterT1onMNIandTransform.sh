#!/usr/bin/env bash

list_of_id=$(cat $1)
echo ${list_of_id} # your subject list

for f in ${list_of_id}; do

	echo $f
# This script performs coregistration of the MNI template on individual T1 first
antsRegistrationSyN.sh -f YourMNITemplate.nii -m YourIndividualT1.nii -o MNIxT1 -t s

# and now do the transformation of your masks of MNI space in individual T1 space

antsApplyTransforms -d 3 -i yourMasks.nii  -r YourIndividualT1.nii -o MasksInNewSpace.nii -n MultiLabel -t [MNIxT10GenericAffine.mat,1]

done
