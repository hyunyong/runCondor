#!/bin/bash

#Folder="/eos/cms/store/data/Run2017B/SingleMuon/RAW-RECO/ZMu-25Jul2019_UL2017-v1/"
#Folder="/eos/cms/store/data/Run2017C/SingleMuon/RAW-RECO/ZMu-25Jul2019_UL2017-v1/"
#Folder="/eos/cms/store/data/Run2017E/SingleMuon/RAW-RECO/ZMu-25Jul2019_UL2017-v1/"
Folder="/eos/cms/store/group/alca_muonalign/adthomps/refit_2018ReRecoIOV1_vs_2018UL_data_withTracker/SingleMuon/crab_MuAlRefit_UL2018data_2018A-rereco-geom/190810_201210/"
fileTXT="2018_IOV1.py"

listfile=`eos find $Folder | grep root | grep -v failed`
echo 'fileNames = [' > $fileTXT

for item in $listfile
do
lenght=${#item}
item_fix=${item:8:$lenght} 
Mystring="       '$item_fix',"
echo $Mystring >> $fileTXT
done

echo ']' >> $fileTXT
