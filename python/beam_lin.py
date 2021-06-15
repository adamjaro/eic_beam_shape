
import ROOT as rt
from ROOT import TVector2, TMath, TGraph

#_____________________________________________________________________________
class beam_lin:
    #_____________________________________________________________________________
    def __init__(self, zmin, zmax, a=0):

        self.p1 = TVector2(zmin, 0).Rotate(a*1e-3)
        self.p2 = TVector2(zmax, 0).Rotate(a*1e-3)

        self.col = rt.kBlue

    #_____________________________________________________________________________
    def draw(self):

        self.gr = TGraph(2)
        self.gr.SetLineColor(self.col)

        self.gr.SetPoint(0, self.p1.Px(), self.p1.Py())
        self.gr.SetPoint(1, self.p2.Px(), self.p2.Py())

        self.gr.Draw("lsame")

