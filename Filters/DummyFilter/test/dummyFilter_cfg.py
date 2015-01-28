import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.Utilities.FileUtils as FileUtils

process = cms.Process("DUMMYFILTER")

options = VarParsing.VarParsing ('analysis')

#done: 100,200,300,400,500,600,700

mylist = FileUtils.loadListFromFile ('filelist/split_filelist_800.txt')

#print mylist

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring (mylist),                        
  
)
    

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring("cout"),
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string("INFO")))

process.DummyFilter = cms.EDFilter("DummyFilter",
  filterAll      = cms.bool(True)
)

process.Path = cms.Path(process.DummyFilter)

process.output = cms.OutputModule("PoolOutputModule",
  fileName = cms.untracked.string("singleMuonGun_RECO_Consolidated_800.root"),
  SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("Path"))
)

process.EndPath = cms.EndPath(process.output)
