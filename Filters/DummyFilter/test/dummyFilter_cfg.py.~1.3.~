import FWCore.ParameterSet.Config as cms

process = cms.Process("DUMMYFILTER")

process.source = cms.Source("PoolSource",
     fileNames = cms.untracked.vstring(
        '/store/caf/user/pakhotin/singleMuonGun_RECO_v4/singleMuonGun_RECO_v4/e72a66c48f67453e57ae7abb7c7b6a5b/singleMuonGun_RECO_3064_1_yCu.root',
       '/store/caf/user/pakhotin/singleMuonGun_RECO_v4/singleMuonGun_RECO_v4/e72a66c48f67453e57ae7abb7c7b6a5b/singleMuonGun_RECO_3065_1_jqT.root'
    )
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
  fileName = cms.untracked.string("singleMuonGun_RECO_Consolidated.root"),
  SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("Path"))
)

process.EndPath = cms.EndPath(process.output)
