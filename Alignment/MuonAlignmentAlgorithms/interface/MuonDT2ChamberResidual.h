#ifndef Alignment_MuonAlignmentAlgorithms_MuonDT2ChamberResidual_H
#define Alignment_MuonAlignmentAlgorithms_MuonDT2ChamberResidual_H

/** \class MuonDT2ChamberResidual
 * 
 * Implementation of muon chamber residuals for transverse DT layers
 * 
 * $Id: $
 */

#include "Alignment/MuonAlignmentAlgorithms/interface/MuonHitsChamberResidual.h"

class MuonDT2ChamberResidual: public MuonHitsChamberResidual 
{
public:
  MuonDT2ChamberResidual(edm::ESHandle<GlobalTrackingGeometry> globalGeometry, AlignableNavigator *navigator,
                         DetId chamberId, const AlignableDetOrUnitPtr& chamberAlignable);
  
  // for DT2, the residual is chamber local y
  // for DT2, the resslope is dresy/dz, or tan(phi_x)
  /* virtual void addResidual(const TrajectoryStateOnSurface *tsos, const TransientTrackingRecHit *hit); */
  virtual void addResidual(edm::ESHandle<Propagator> prop, const TrajectoryStateOnSurface *tsos, const TrackingRecHit *hit);


  // dummy method
  virtual void setSegmentResidual(const reco::MuonChamberMatch *, const reco::MuonSegmentMatch *) {}
};

#endif // Alignment_MuonAlignmentAlgorithms_MuonDT2ChamberResidual_H
