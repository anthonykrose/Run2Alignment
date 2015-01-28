import ROOT, array, os, sys, re, math, random
from math import *

sys.path.append("../Alignment/MuonAlignmentAlgorithms/scripts/") 
from signConventions import *

execfile("geometryXMLparser.py")
execfile("plotscripts.py")
execfile("tdrStyle.py")

#alignmentName = "mc_DT-1100-111111_MuIdeal_TkIdeal_v1"
#alignmentName = "mc_DT-1100-111001_MuIdeal_TkIdeal_v1"
#alignmentName = "mc_DT-1100-110111_MuIdeal_TkIdeal_v1"
#alignmentName = "mc_DT-1100-101111_MuIdeal_TkIdeal_v1"
#alignmentName = "mc_DT-1000-101001_MuIdeal_TkIdeal_v1"
#alignmentName = "mc_DT-1000-001000_MuIdeal_TkIdeal_v1"
#alignmentName = "mc_DT-1100-111111_MuIdeal_TkIdeal_XandYFiducialCuts_v3"
#alignmentName = "mc_DT-1100-110111_MuIdeal_TkIdeal_XandYFiducialCuts_v1"
# alignmentName = "mc_DT-1100-111111_MuIdeal_TkIdeal_XandYFiducialCuts_v1_compare"
# alignmentName = "mc_DT-1100-111111_MuIdeal_TkIdeal_CSA14_CMSSW_7_0_6_v1"

# alignmentName = "mc_DT-1100-111111_MuIdeal_TkIdeal_CSA14_CMSSW_7_1_0_localTest_singleMu71X_v3"
# alignmentName = "mic_DT-1100-111111_MuIdeal_TkIdeal_CSA14_CMSSW_7_1_0_localTest_singleMu71X_v4"

# alignmentName = "mc_DT-1111-111111_MuIdeal_TkIdeal_CSA14_CMSSW_7_1_0_localTest_singleMu71X_v2_combined"
alignmentName = "mc_DT-1100-111111_MuIdeal_TkIdeal_CSA14_CMSSW_7_1_0_localTest_singleMu71X_v3_combined"

#dx_bins, dx_min, dx_max = 1000, -0.3, 0.3
#dy_bins, dy_min, dy_max = 1000, -2.6, 2.6
#dz_bins, dz_min, dz_max = 1000, -2.6, 2.6
#dphix_bins, dphix_min, dphix_max = 1000, -1.1, 1.1
#dphiy_bins, dphiy_min, dphiy_max = 1000, -1.1, 1.1
#dphiz_bins, dphiz_min, dphiz_max = 1000, -0.3, 0.3

#alignmentName = "mc_DT_res1100_dt111111_HWuncert111111_v1"
dx_bins, dx_min, dx_max = 1000, -0.6, 0.6
dy_bins, dy_min, dy_max = 1000, -5.1, 5.1
dz_bins, dz_min, dz_max = 1000, -5.1, 5.1
dphix_bins, dphix_min, dphix_max = 1000, -1.1, 1.1
dphiy_bins, dphiy_min, dphiy_max = 1000, -1.1, 1.1
dphiz_bins, dphiz_min, dphiz_max = 1000, -1.1, 1.1

xmlfile1             = "Geometries/"+alignmentName+"_03.xml"
referenceName        = "MC_53_V14"
xmlfile_ref          = "Geometries/muonGeometry_MC_53_V14_Local.xml" # reference geometry: initial or IDEAL

folderName = "RESULT/"+alignmentName+"/"

pngPath = folderName+"/PNG/"
if not os.path.exists(pngPath):
   os.makedirs(pngPath)
pdfPath = folderName+"/PDF/"
if not os.path.exists(pdfPath):
   os.makedirs(pdfPath)

g1 = MuonGeometry(xmlfile1)
g_ref = MuonGeometry(xmlfile_ref)

c1 = ROOT.TCanvas("canvas", "canvas")
c1.SetCanvasSize(900,900)

legend = ROOT.TLegend(.17,.935,0.9,1.)
legend.SetFillColor(ROOT.kWhite)
legend.SetBorderSize(0)
legend.SetTextFont(42)
legend.SetTextSize(0.045)
legend.SetMargin(0.13)

h_dx_dy = ROOT.TH2F("h_dx_dy", "h_dx_dy", dx_bins, dx_min, dx_max, dy_bins, dy_min, dy_max)
h_dx_dy.SetXTitle("#delta x (mm)")
h_dx_dy.SetYTitle("#delta y (mm)")
h_dx_dy.SetMarkerColor(2)
h_dx_dy.SetMarkerSize(2)
h_dx_dy.StatOverflows(ROOT.kTRUE)

h_dx_dz = ROOT.TH2F("h_dx_dz", "h_dx_dz", dx_bins, dx_min, dx_max, dz_bins, dz_min, dz_max)
h_dx_dz.SetXTitle("#delta x (mm)")
h_dx_dz.SetYTitle("#delta z (mm)")
h_dx_dz.SetMarkerColor(2)
h_dx_dz.SetMarkerSize(2)
h_dx_dz.StatOverflows(ROOT.kTRUE)

h_dx_dphix = ROOT.TH2F("h_dx_dphix", "h_dx_dphix", dx_bins, dx_min, dx_max, dphix_bins, dphix_min, dphix_max)
h_dx_dphix.SetXTitle("#delta x (mm)")
h_dx_dphix.SetYTitle("#delta #phi_{x} (mrad)")
h_dx_dphix.SetMarkerColor(2)
h_dx_dphix.SetMarkerSize(2)
h_dx_dphix.StatOverflows(ROOT.kTRUE)

h_dx_dphiy = ROOT.TH2F("h_dx_dphiy", "h_dx_dphiy", dx_bins, dx_min, dx_max, dphiy_bins, dphiy_min, dphiy_max)
h_dx_dphiy.SetXTitle("#delta x (mm)")
h_dx_dphiy.SetYTitle("#delta #phi_{y} (mrad)")
h_dx_dphiy.SetMarkerColor(2)
h_dx_dphiy.SetMarkerSize(2)
h_dx_dphiy.StatOverflows(ROOT.kTRUE)

h_dx_dphiz = ROOT.TH2F("h_dx_dphiz", "h_dx_dphiz", dx_bins, dx_min, dx_max, dphiz_bins, dphiz_min, dphiz_max)
h_dx_dphiz.SetXTitle("#delta x (mm)")
h_dx_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
h_dx_dphiz.SetMarkerColor(2)
h_dx_dphiz.SetMarkerSize(2)
h_dx_dphiz.StatOverflows(ROOT.kTRUE)


h_dy_dz = ROOT.TH2F("h_dy_dz", "h_dy_dz", dy_bins, dy_min, dy_max, dz_bins, dz_min, dz_max)
h_dy_dz.SetXTitle("#delta y (mm)")
h_dy_dz.SetYTitle("#delta z (mm)")
h_dy_dz.SetMarkerColor(2)
h_dy_dz.SetMarkerSize(2)
h_dy_dz.StatOverflows(ROOT.kTRUE)

h_dy_dphix = ROOT.TH2F("h_dy_dphix", "h_dy_dphix", dy_bins, dy_min, dy_max, dphix_bins, dphix_min, dphix_max)
h_dy_dphix.SetXTitle("#delta y (mm)")
h_dy_dphix.SetYTitle("#delta #phi_{x} (mrad)")
h_dy_dphix.SetMarkerColor(2)
h_dy_dphix.SetMarkerSize(2)
h_dy_dphix.StatOverflows(ROOT.kTRUE)

h_dy_dphiy = ROOT.TH2F("h_dy_dphiy", "h_dy_dphiy", dy_bins, dy_min, dy_max, dphiy_bins, dphiy_min, dphiy_max)
h_dy_dphiy.SetXTitle("#delta y (mm)")
h_dy_dphiy.SetYTitle("#delta #phi_{y} (mrad)")
h_dy_dphiy.SetMarkerColor(2)
h_dy_dphiy.SetMarkerSize(2)
h_dy_dphiy.StatOverflows(ROOT.kTRUE)

h_dy_dphiz = ROOT.TH2F("h_dy_dphiz", "h_dy_dphiz", dy_bins, dy_min, dy_max, dphiz_bins, dphiz_min, dphiz_max)
h_dy_dphiz.SetXTitle("#delta y (mm)")
h_dy_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
h_dy_dphiz.SetMarkerColor(2)
h_dy_dphiz.SetMarkerSize(2)
h_dy_dphiz.StatOverflows(ROOT.kTRUE)


h_dz_dphix = ROOT.TH2F("h_dz_dphix", "h_dz_dphix", dz_bins, dz_min, dz_max, dphix_bins, dphix_min, dphix_max)
h_dz_dphix.SetXTitle("#delta z (mm)")
h_dz_dphix.SetYTitle("#delta #phi_{x} (mrad)")
h_dz_dphix.SetMarkerColor(2)
h_dz_dphix.SetMarkerSize(2)
h_dz_dphix.StatOverflows(ROOT.kTRUE)

h_dz_dphiy = ROOT.TH2F("h_dz_dphiy", "h_dz_dphiy", dz_bins, dz_min, dz_max, dphiy_bins, dphiy_min, dphiy_max)
h_dz_dphiy.SetXTitle("#delta z (mm)")
h_dz_dphiy.SetYTitle("#delta #phi_{y} (mrad)")
h_dz_dphiy.SetMarkerColor(2)
h_dz_dphiy.SetMarkerSize(2)
h_dz_dphiy.StatOverflows(ROOT.kTRUE)

h_dz_dphiz = ROOT.TH2F("h_dz_dphiz", "h_dz_dphiz", dz_bins, dz_min, dz_max, dphiz_bins, dphiz_min, dphiz_max)
h_dz_dphiz.SetXTitle("#delta z (mm)")
h_dz_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
h_dz_dphiz.SetMarkerColor(2)
h_dz_dphiz.SetMarkerSize(2)
h_dz_dphiz.StatOverflows(ROOT.kTRUE)


h_dphix_dphiy = ROOT.TH2F("h_dphix_dphiy", "h_dphix_dphiy", dphix_bins, dphix_min, dphix_max, dphiy_bins, dphiy_min, dphiy_max)
h_dphix_dphiy.SetXTitle("#delta #phi_{x} (mrad)")
h_dphix_dphiy.SetYTitle("#delta #phi_{y} (mrad)")
h_dphix_dphiy.SetMarkerColor(2)
h_dphix_dphiy.SetMarkerSize(2)
h_dphix_dphiy.StatOverflows(ROOT.kTRUE)

h_dphix_dphiz = ROOT.TH2F("h_dphix_dphiz", "h_dphix_dphiz", dphix_bins, dphix_min, dphix_max, dphiz_bins, dphiz_min, dphiz_max)
h_dphix_dphiz.SetXTitle("#delta #phi_{x} (mrad)")
h_dphix_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
h_dphix_dphiz.SetMarkerColor(2)
h_dphix_dphiz.SetMarkerSize(2)
h_dphix_dphiz.StatOverflows(ROOT.kTRUE)


h_dphiy_dphiz = ROOT.TH2F("h_dphiy_dphiz", "h_dphiy_dphiz", dphiy_bins, dphiy_min, dphiy_max, dphiz_bins, dphiz_min, dphiz_max)
h_dphiy_dphiz.SetXTitle("#delta #phi_{y} (mrad)")
h_dphiy_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
h_dphiy_dphiz.SetMarkerColor(2)
h_dphiy_dphiz.SetMarkerSize(2)
h_dphiy_dphiz.StatOverflows(ROOT.kTRUE)


for wheel in (-2, 0, 2):
  station = 1
  
  h_dx_dy.Reset("ICESM")
  h_dx_dz.Reset("ICESM")
  h_dx_dphix.Reset("ICESM")
  h_dx_dphiy.Reset("ICESM")
  h_dx_dphiz.Reset("ICESM")
  
  h_dy_dz.Reset("ICESM")
  h_dy_dphix.Reset("ICESM")
  h_dy_dphiy.Reset("ICESM")
  h_dy_dphiz.Reset("ICESM")
  
  h_dz_dphix.Reset("ICESM")
  h_dz_dphiy.Reset("ICESM")
  h_dz_dphiz.Reset("ICESM")
  
  h_dphix_dphiy.Reset("ICESM")
  h_dphix_dphiz.Reset("ICESM")
  
  h_dphiy_dphiz.Reset("ICESM")
  
  if station != 4: sectors = (1,2,3,4,5,6,7,8,9,10,11,12)
  else: sectors = (1,2,3,4,5,6,7,8,9,10,11,12,13,14)
  for sector in sectors:
    dx_mm = 10.0*(g1.dt[wheel, station, sector].x - g_ref.dt[wheel, station, sector].x)*signConventions["DT", wheel, station, sector][0]
    dy_mm = 10.0*(g1.dt[wheel, station, sector].y - g_ref.dt[wheel, station, sector].y)*signConventions["DT", wheel, station, sector][1]
    dz_mm = 10.0*(g1.dt[wheel, station, sector].z - g_ref.dt[wheel, station, sector].z)*signConventions["DT", wheel, station, sector][2]
    dphix_mrad = 1000.0*(g1.dt[wheel, station, sector].phix - g_ref.dt[wheel, station, sector].phix)
    dphiy_mrad = 1000.0*(g1.dt[wheel, station, sector].phiy - g_ref.dt[wheel, station, sector].phiy)
    dphiz_mrad = 1000.0*(g1.dt[wheel, station, sector].phiz - g_ref.dt[wheel, station, sector].phiz)
        
    h_dx_dy.Fill(dx_mm, dy_mm)
    h_dx_dz.Fill(dx_mm, dz_mm)
    h_dx_dphix.Fill(dx_mm, dphix_mrad)
    h_dx_dphiy.Fill(dx_mm, dphiy_mrad)
    h_dx_dphiz.Fill(dx_mm, dphiz_mrad)
    
    h_dy_dz.Fill(dy_mm, dz_mm)
    h_dy_dphix.Fill(dy_mm, dphix_mrad)
    h_dy_dphiy.Fill(dy_mm, dphiy_mrad)
    h_dy_dphiz.Fill(dy_mm, dphiz_mrad)
    
    h_dz_dphix.Fill(dz_mm, dphix_mrad)
    h_dz_dphiy.Fill(dz_mm, dphiy_mrad)
    h_dz_dphiz.Fill(dz_mm, dphiz_mrad)
    
    h_dphix_dphiy.Fill(dphix_mrad, dphiy_mrad)
    h_dphix_dphiz.Fill(dphix_mrad, dphiz_mrad)
    
    h_dphiy_dphiz.Fill(dphiy_mrad, dphiz_mrad)

  if wheel ==  0 and station == 1: plotsLabel, plotsHeader = "MB_0_1",  "MB 0/1/All"
  if wheel == -2 and station == 1: plotsLabel, plotsHeader = "MB_m2_1", "MB-2/1/All"
  if wheel ==  2 and station == 1: plotsLabel, plotsHeader = "MB_p2_1", "MB+2/1/All"

  legend.SetHeader(plotsHeader)

  h_dx_dy.Draw()
  legend.Draw()
  pngName = "DT_corr_dx_dy_" + plotsLabel + ".png"
  pdfName = "DT_corr_dx_dy_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dx_dz.Draw()
  legend.Draw()
  pngName = "DT_corr_dx_dz_" + plotsLabel + ".png"
  pdfName = "DT_corr_dx_dz_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dx_dphix.Draw()
  legend.Draw()
  pngName = "DT_corr_dx_dphix_" + plotsLabel + ".png"
  pdfName = "DT_corr_dx_dphix_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dx_dphiy.Draw()
  legend.Draw()
  pngName = "DT_corr_dx_dphiy_" + plotsLabel + ".png"
  pdfName = "DT_corr_dx_dphiy_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dx_dphiz.Draw()
  legend.Draw()
  pngName = "DT_corr_dx_dphiz_" + plotsLabel + ".png"
  pdfName = "DT_corr_dx_dphiz_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)


  h_dy_dz.Draw()
  legend.Draw()
  pngName = "DT_corr_dy_dz_" + plotsLabel + ".png"
  pdfName = "DT_corr_dy_dz_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dy_dphix.Draw()
  legend.Draw()
  pngName = "DT_corr_dy_dphix_" + plotsLabel + ".png"
  pdfName = "DT_corr_dy_dphix_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dy_dphiy.Draw()
  legend.Draw()
  pngName = "DT_corr_dy_dphiy_" + plotsLabel + ".png"
  pdfName = "DT_corr_dy_dphiy_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dy_dphiz.Draw()
  legend.Draw()
  pngName = "DT_corr_dy_dphiz_" + plotsLabel + ".png"
  pdfName = "DT_corr_dy_dphiz_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)


  h_dz_dphix.Draw()
  legend.Draw()
  pngName = "DT_corr_dz_dphix_" + plotsLabel + ".png"
  pdfName = "DT_corr_dz_dphix_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dz_dphiy.Draw()
  legend.Draw()
  pngName = "DT_corr_dz_dphiy_" + plotsLabel + ".png"
  pdfName = "DT_corr_dz_dphiy_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dz_dphiz.Draw()
  legend.Draw()
  pngName = "DT_corr_dz_dphiz_" + plotsLabel + ".png"
  pdfName = "DT_corr_dz_dphiz_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)


  h_dphix_dphiy.Draw()
  legend.Draw()
  pngName = "DT_corr_dphix_dphiy_" + plotsLabel + ".png"
  pdfName = "DT_corr_dphix_dphiy_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  h_dphix_dphiz.Draw()
  legend.Draw()
  pngName = "DT_corr_dphix_dphiz_" + plotsLabel + ".png"
  pdfName = "DT_corr_dphix_dphiz_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)


  h_dphiy_dphiz.Draw()
  legend.Draw()
  pngName = "DT_corr_dphiy_dphiz_" + plotsLabel + ".png"
  pdfName = "DT_corr_dphiy_dphiz_" + plotsLabel + ".pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)


