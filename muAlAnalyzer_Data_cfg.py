import FWCore.ParameterSet.Config as cms
import os
ijob = int(os.environ["IJOB"])
input_files = os.environ["INPUTFILES"].split(" ")

process = cms.Process("MUAL")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(*input_files))
#import FWCore.PythonUtilities.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = '2018_UL_IOV1.txt').getVLuminosityBlockRange()

process.muAlAnalyzer = cms.EDAnalyzer('MuAlAnalyzer',
  debugLevel      = cms.int32(1),
  recoMuons       = cms.InputTag("muAlMuons"),
  recoBeamSpot    = cms.InputTag("offlineBeamSpot"),
  fillRecoMuons   = cms.bool(True),
  fillRecoDimuons = cms.bool(True),
  fillGenMuons    = cms.bool(False),
)

process.p = cms.Path(process.muAlAnalyzer)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string("out_%03d.root" % ijob)
)
