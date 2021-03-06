/** \file AlignableParameterBuilder.cc
 *
 *  $Date: 2010/10/26 20:01:52 $
 *  $Revision: 1.19 $

*/

// This class's header should be first:
#include "Alignment/CommonAlignmentAlgorithm/interface/AlignmentParameterBuilder.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "Alignment/CommonAlignment/interface/Alignable.h"
#include "Alignment/CommonAlignment/interface/AlignmentParameters.h"

#include "Alignment/CommonAlignmentParametrization/interface/AlignmentParametersFactory.h"

#include "Alignment/CommonAlignmentAlgorithm/interface/AlignmentParameterSelector.h"
#include "Alignment/CommonAlignmentAlgorithm/interface/SelectionUserVariables.h"

#include <algorithm>

using namespace AlignmentParametersFactory;

//__________________________________________________________________________________________________
AlignmentParameterBuilder::AlignmentParameterBuilder(AlignableTracker* alignableTracker,
						     AlignableExtras* alignableExtras) :
  theAlignables(),
  theAlignableTracker(alignableTracker),
  theAlignableMuon(0),
  theAlignableExtras(alignableExtras)
{
}

//__________________________________________________________________________________________________
AlignmentParameterBuilder::AlignmentParameterBuilder(AlignableTracker* alignableTracker, 
                                                     AlignableMuon* alignableMuon,
						     AlignableExtras* alignableExtras) :
  theAlignables(), 
  theAlignableTracker(alignableTracker),
  theAlignableMuon(alignableMuon),
  theAlignableExtras(alignableExtras)
{
}


//__________________________________________________________________________________________________
AlignmentParameterBuilder::AlignmentParameterBuilder(AlignableTracker* alignableTracker,
						     AlignableExtras* alignableExtras,
                                                     const edm::ParameterSet &pSet) :
  theAlignables(), 
  theAlignableTracker(alignableTracker),
  theAlignableMuon(0),
  theAlignableExtras(alignableExtras)
{
  this->addAllSelections(pSet);
}

//__________________________________________________________________________________________________
AlignmentParameterBuilder::AlignmentParameterBuilder(AlignableTracker* alignableTracker,
                                                     AlignableMuon* alignableMuon,
						     AlignableExtras* alignableExtras,
                                                     const edm::ParameterSet &pSet) :
  theAlignables(), 
  theAlignableTracker(alignableTracker),
  theAlignableMuon(alignableMuon),
  theAlignableExtras(alignableExtras)
{
  // std::cout << "Made it to AlignmentParameterBuilder::AlignmentParameterBuilder" << std::endl;
  this->addAllSelections(pSet);
  // std::cout << "Made it past addAllSelections(pSet)" << std::endl;

}

const AlignableTracker* AlignmentParameterBuilder::alignableTracker() const
{
  return theAlignableTracker;
}

//__________________________________________________________________________________________________
void AlignmentParameterBuilder::addAllSelections(const edm::ParameterSet &pSet)
{

  // std::cout << "addAllSelections: 1 " << std::endl;
  AlignmentParameterSelector selector(0);
  std::vector<std::string> selsTypes(pSet.getParameter<std::vector<std::string> >("parameterTypes"));

  // std::cout << "addAllSelections: 2 " << std::endl;
  
  for (unsigned int i = 0; i < selsTypes.size(); ++i) {
    // std::cout << "addAllSelections: 3, i: " << i << std::endl;

    std::vector<std::string> selSetType(selector.decompose(selsTypes[i], ','));
    if (selSetType.size() != 2) {
      // std::cout << "addAllSelections: 4 " << std::endl;
      throw cms::Exception("BadConfig") << "AlignmentParameterBuilder"
					<< "parameterTypes should contain 2 comma separated strings"
					<< ", but found '" << selsTypes[i] << "'.";
    }
    // std::cout << "addAllSelections: 5 " << std::endl;
    // std::cout << "selSetType[0]: " << selSetType[0] << std::endl;
    // std::cout << "selSetType[1]: " << selSetType[1] << std::endl;

    this->addSelections(pSet.getParameter<edm::ParameterSet>(selSetType[0]),
			AlignmentParametersFactory::parametersType(selSetType[1]));
  }
  // std::cout << "addAllSelections: 6 " << std::endl;

}

//__________________________________________________________________________________________________
unsigned int AlignmentParameterBuilder::addSelections(const edm::ParameterSet &pSet,
						      ParametersType parType)
{

  // std::cout << "made it to AlignmentParameterBuilder::addSelections" << std::endl;
  const unsigned int oldAliSize = theAlignables.size();

  // std::cout << "made it to AlignmentParameterBuilder::addSelections 1" << std::endl;

  AlignmentParameterSelector selector( theAlignableTracker, theAlignableMuon, theAlignableExtras );
  // std::cout << "made it to AlignmentParameterBuilder::addSelections 1a" << std::endl;

  const unsigned int addedSets = selector.addSelections(pSet);

  // std::cout << "made it to AlignmentParameterBuilder::addSelections 2" << std::endl;

  const align::Alignables &alignables = selector.selectedAlignables();
  const std::vector<std::vector<char> > &paramSels = selector.selectedParameters();

  // std::cout << "made it to AlignmentParameterBuilder::addSelections 3" << std::endl;

  align::Alignables::const_iterator iAli = alignables.begin();
  std::vector<std::vector<char> >::const_iterator iParamSel = paramSels.begin();
  unsigned int nHigherLevel = 0;

  // std::cout << "made it to AlignmentParameterBuilder::addSelections 4" << std::endl;

  while (iAli != alignables.end() && iParamSel != paramSels.end()) {
    std::vector<bool> boolParSel;
    std::vector<char> parSel(*iParamSel); // copy, since decodeParamSel may manipulate
    bool charSelIsGeneral = this->decodeParamSel(parSel, boolParSel);
    if (this->add(*iAli, parType, boolParSel)) ++nHigherLevel;
    if (charSelIsGeneral) this->addFullParamSel((*iAli)->alignmentParameters(), parSel);

    ++iAli;
    ++iParamSel;
  }

  // std::cout << "made it to AlignmentParameterBuilder::addSelections 5" << std::endl;

  edm::LogInfo("Alignment") << "@SUB=AlignmentParameterBuilder::addSelections"
                            << " Added " << addedSets << " set(s) of alignables with "
                            << theAlignables.size() - oldAliSize << " alignables in total,"
                            << " of which " << nHigherLevel << " are higher level "
			    << "(using " << parametersTypeName(parType) << "AlignmentParameters).";
   
  // std::cout << "made it to AlignmentParameterBuilder::addSelections 6" << std::endl;

  return addedSets;
}

//__________________________________________________________________________________________________
bool AlignmentParameterBuilder::add(Alignable *alignable,
				    ParametersType parType,
				    const std::vector<bool> &sel)
{ 
  AlignmentParameters *paras = AlignmentParametersFactory::createParameters(alignable, parType, sel);
  alignable->setAlignmentParameters(paras);
  theAlignables.push_back(alignable);

  const int aliTypeId = alignable->alignableObjectId();
  const bool isHigherLevel = (aliTypeId != align::AlignableDet
			      && aliTypeId != align::AlignableDetUnit);
  return isHigherLevel;
}


//__________________________________________________________________________________________________
unsigned int AlignmentParameterBuilder::add(const align::Alignables &alignables,
					    ParametersType parType, const std::vector<bool> &sel)
{

  unsigned int nHigherLevel = 0;

  for (align::Alignables::const_iterator iAli = alignables.begin();
       iAli != alignables.end(); ++iAli) {
    if (this->add(*iAli, parType, sel)) ++nHigherLevel;
  }

  return nHigherLevel;
}


//__________________________________________________________________________________________________
void AlignmentParameterBuilder::fixAlignables(int n)
{

  if (n<1 || n>3) {
    edm::LogError("BadArgument") << " n = " << n << " is not in [1,3]";
    return;
  }

  align::Alignables theNewAlignables;
  int i=0;
  int imax = theAlignables.size();
  for ( align::Alignables::const_iterator ia=theAlignables.begin();
        ia!=theAlignables.end();  ia++ ) 
	{
	  i++;
	  if ( n==1 && i>1 ) 
		theNewAlignables.push_back(*ia);
	  else if ( n==2 && i>1 && i<imax ) 
		theNewAlignables.push_back(*ia);
	  else if ( n==3 && i>2 && i<imax) 
		theNewAlignables.push_back(*ia);
	}

  theAlignables = theNewAlignables;

  edm::LogInfo("Alignment") << "@SUB=AlignmentParameterBuilder::fixAlignables"
                            << "removing " << n << " alignables, so that " 
                            << theAlignables.size() << " alignables left";
}

//__________________________________________________________________________________________________
bool AlignmentParameterBuilder::decodeParamSel(std::vector<char> &paramSelChar,
                                               std::vector<bool> &result) const
{
  result.clear();
  // remove all spaces from paramSelChar - useful to group the parameters if they are many
  paramSelChar.erase(std::remove(paramSelChar.begin(), paramSelChar.end(), ' '),
		     paramSelChar.end());

  bool anyNon01 = false;

  for (unsigned int pos = 0; pos < paramSelChar.size(); ++pos) {

    switch (paramSelChar[pos]) {
    default:
      anyNon01 = true;
      // no break;
    case '1':
      result.push_back(true);
      break;
    case '0':
      result.push_back(false);
      break;
    }
  }

  return anyNon01;
}

//__________________________________________________________________________________________________
bool AlignmentParameterBuilder::addFullParamSel(AlignmentParameters *aliParams,
                                                const std::vector<char> &fullSel) const
{
  if (!aliParams) return false;

  aliParams->setUserVariables(new SelectionUserVariables(fullSel));

  return true;
}
