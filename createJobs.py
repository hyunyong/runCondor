import os, sys, optparse, math

cTmp = """executable              = {sh}
universe                = vanilla
requirements            = (OpSysAndVer =?= "CentOS7")
request_cpus            = {nCPU}
max_transfer_output_mb  = {memory}
+JobFlavour             = "tomorrow"
output                  = {shN}.out
error                   = {shN}.err
log                     = {shN}.log
transfer_input_files    = {tarBall}, {cfgFile}, {lumi}
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_output_files   = {outN}
queue

"""

sTmp="""#!/bin/sh

echo $SHELL
export CAFDIR=`pwd`
tar xf {tarBall}
cd {cmsPath}
scram build ProjectRename
eval `scramv1 run -sh`
export IJOB={jobID}
export INPUTFILES='{fileList}'
cd $CAFDIR
cmsRun muAlAnalyzer_Data_cfg.py
tar cf {outFile} *.root
"""

file_list = sys.argv[1]   # MuAlRefit_Run2016E_RAWreco_DT3DOF_CSC3DOF_02_list.py
njobs = int(sys.argv[2])  # 700

print "file_list =", file_list
print "njobs =", njobs

execfile(file_list)

for i in range(njobs):
    inputNames = " ".join(fileNames[len(fileNames)*i/njobs:len(fileNames)*(i+1)/njobs])
    analyzer = "analyzer%03d.sh"%i
    outFile = "out%03d.tar"%i
    sh = open(analyzer,'w')
    tmpShV = {'tarBall':'2017UL1060.tar' , 'cmsPath':'2017UL1060/src', 'jobID':i, 'fileList':inputNames, 'outFile':outFile}
    sh.write(sTmp.format(**tmpShV))
    os.system("chmod +x %s" % analyzer)
    sub = open(analyzer.replace(".sh",".sub"),'w')
    tmpSubV = {'sh':analyzer, 'nCPU':4, 'memory':'4000','shN':'analyzer%03d'%i, 'tarBall':'2017UL1060.tar', 'cfgFile':'muAlAnalyzer_Data_cfg.py', 'outN':outFile, 'lumi':'2018_UL_IOV1.txt'}
    sub.write(cTmp.format(**tmpSubV))
    os.system("chmod +x %s" % analyzer.replace(".sh",".sub"))
cList = [x for x in os.listdir(".") if x.startswith("analyzer") and x.endswith(".sub")]
cList.sort()
for i, x in enumerate(cList):
  print "condor submit {}/{}".format(i+1,len(cList))
  try: os.system("condor_submit -batch-name MuAlAnalyzer_"+file_list.replace(".py"," ")+x)
  except: os.system("condor_submit -batch-name MuAlAnalyzer_"+file_list.replace(".py"," ")+x)
