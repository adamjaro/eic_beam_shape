#!/usr/bin/python3

#import ctypes
from ctypes import CDLL, c_double
import os
import sys

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, gSystem, TCanvas
from ROOT import TDatabasePDG, TVector3, TH1D, TMath

sys.path.append("./python")
from beam_lin import beam_lin
import plot_utils as ut
from read_con import read_con

#_____________________________________________________________________________
def main():

    #name of config file from command line argument
    args = sys.argv
    if len(args) < 2:
        print("No configuration specified.")
        quit()
    args.pop(0)
    #config = args.pop(0)

    cf = read_con(args.pop(0))

    lib = CDLL("build/libeic_beam_shape.so")

    cross_angle = cf.flt("cross_angle") # mrad
    y_angle = cf.flt("y_angle") # urad

    #simulation instance
    sim = lib.make_sim()

    #electron bunch
    b1 = lib.make_bunch(cf.int("e_np"), cf("e_rmsx"), cf("e_bsx"), cf("e_rmsy"), cf("e_bsy"), cf("e_rmsz"))
    lib.bunch_rotate_y(b1, c_double(-cross_angle/2.))

    me = TDatabasePDG.Instance().GetParticle(11).Mass()
    b1_p = TMath.Sqrt(cf.flt("Ee")**2 - me**2)
    b1_dir = TVector3(0, 0, -1)
    lib.bunch_set_kinematics(b1, cf("Ee"), c_double(b1_p), c_double(b1_dir.x()), c_double(b1_dir.y()), c_double(b1_dir.z()))

    #proton/nucleus bunch
    b2 = lib.make_bunch(cf.int("p_np"), cf("p_rmsx"), cf("p_bsx"), cf("p_rmsy"), cf("p_bsy"), cf("p_rmsz"))
    lib.bunch_set_color(b2, rt.kRed)
    #lib.bunch_rotate_y(b2, c_double(-cross_angle))
    lib.bunch_rotate_y(b2, c_double(-cross_angle/2.))

    #bunch kinematics for proton/nucleus
    nA = 1
    nZ = 1
    if cf.has_option("A"):
        nA = cf.int("A")
    if cf.has_option("Z"):
        nZ = cf.int("Z")
    mp = TDatabasePDG.Instance().GetParticle(2212).Mass()
    nmass = mp*nA
    b2_p = TMath.Sqrt( cf.flt("Ep")**2 - mp**2 )*nZ
    b2_en = TMath.Sqrt( b2_p**2 + nmass**2 )
    #print("en: ", b2_en/nA)

    #direction for proton/nucleus bunch
    b2_dir = TVector3(0, 0, 1)
    b2_dir.RotateY(-cross_angle*1e-3)
    #b2_dir = TVector3(TMath.Sin(cross_angle*1e-3), 0, TMath.Cos(cross_angle*1e-3))
    #print(b2_dir.x(), b2_dir.y(), b2_dir.z())
    #print(TMath.Sin(cross_angle*1e-3), TMath.Cos(cross_angle*1e-3))
    b2_dir.RotateX(y_angle*1e-6)
    lib.bunch_set_kinematics(b2, c_double(b2_en), c_double(b2_p), c_double(b2_dir.x()), c_double(b2_dir.y()), c_double(b2_dir.z()))

    #put bunches to the simulation
    lib.sim_add_bunch(sim, b2)
    lib.sim_add_bunch(sim, b1)

    lib.sim_set_bins(sim, cf.int("nx"), cf("xmin"), cf("xmax"), cf.int("ny"), cf("ymin"), cf("ymax"), cf.int("nz"), cf("zmin"), cf("zmax"))

    #select the function
    iplot = 5

    func = []
    func.append( make_plot ) # 0
    func.append( make_video ) # 1
    func.append( project_xy ) # 2
    func.append( pairs_xyz ) # 3
    func.append( evolution ) # 4
    func.append( make_plot_pairs ) # 5
    func.append( video_pairs ) # 6

    func[iplot](lib, sim, cross_angle)

#main

#_____________________________________________________________________________
def make_plot(lib, sim, cross_angle):

    #zmin = -40
    #zmax = 40
    zmin = -370
    zmax = 370

    #xmin = -1
    #xmax = 1
    xmin = -10
    xmax = 10

    #electron and proton beams
    beam_el = beam_lin(zmin, zmax)
    beam_p = beam_lin(zmin, zmax, -cross_angle)
    beam_p.col = rt.kRed

    c1 = TCanvas("c1","c1",1200,900)
    frame = gPad.DrawFrame(zmin, xmin, zmax, xmax) # xmin, ymin, xmax, ymax in ROOT
    ut.put_frame_yx_tit(frame, "#it{x} (mm)", "#it{z} (mm)", 1, 1.2)
    ut.set_margin_lbtr(gPad, 0.07, 0.09, 0.02, 0.03)

    gPad.SetGrid()

    beam_el.draw()
    beam_p.draw()

    #t0 = -1
    #dt = 0.01
    #nstep = 200

    time = 0.3

    lib.sim_move(sim, c_double(time))

    leg = ut.prepare_leg(0.7, 0.8, 0.15, 0.25)
    leg.AddEntry("", "#it{t} = "+"{0:.2f}".format(time)+" ns", "")
    leg.Draw("same")

    lib.sim_draw(sim)

    ut.invert_col(gPad)
    c1.SaveAs("01fig.png")

#make_plot

#_____________________________________________________________________________
def make_video(lib, sim, cross_angle):

    #zmin = -40
    #zmax = 40
    zmin = -370
    zmax = 370

    #xmin = -1
    #xmax = 1
    xmin = -10
    xmax = 10

    t0 = -1
    dt = 0.01
    nstep = 200

    out = "movie.mp4"

    lib.sim_move(sim, c_double(t0-dt))
    time = t0-dt

    #electron and proton beams
    beam_el = beam_lin(zmin, zmax)
    beam_p = beam_lin(zmin, zmax, -cross_angle)
    beam_p.col = rt.kRed

    c1 = TCanvas("c1","c1",1200,900)

    os.system("rm -f "+out)
    os.system("rm -rf tmp")
    os.system("mkdir tmp")

    for i in range(nstep):

        time += dt

        lib.sim_move(sim, c_double(dt))

        c1.Clear()

        frame = gPad.DrawFrame(zmin, xmin, zmax, xmax) # xmin, ymin, xmax, ymax in ROOT
        ut.put_frame_yx_tit(frame, "#it{x} (mm)", "#it{z} (mm)", 1, 1.2)
        ut.set_margin_lbtr(gPad, 0.07, 0.09, 0.02, 0.03)

        gPad.SetGrid()

        beam_el.draw()
        beam_p.draw()

        lib.sim_draw(sim)

        leg = ut.prepare_leg(0.7, 0.8, 0.15, 0.25)
        leg.AddEntry("", "#it{t} = "+"{0:.2f}".format(time)+" ns", "")
        leg.Draw("same")

        nam = "tmp/fig_"+"{0:04d}".format(i)+".png"

        ut.invert_col(gPad)
        c1.SaveAs(nam)

    os.system("ffmpeg -r 30 -i tmp/fig_%04d.png -r 30 "+out)

#make_video

#_____________________________________________________________________________
def project_xy(lib, sim, cross_angle):

    time = 0.3

    bunch_id = 1

    lib.sim_move(sim, c_double(time))
    b = lib.sim_get_bunch(sim, bunch_id)

    #can = TCanvas("c1","c1",800,800)
    can = TCanvas("c1","c1",1086, 543)
    can.Divide(2,1)

    can.cd(1)
    frame = gPad.DrawFrame(-2, -2, 2, 2) # xmin, ymin, xmax, ymax in ROOT
    ut.put_frame_yx_tit(frame, "#it{y} (mm)", "#it{x} (mm)", 1, 1.2)

    gPad.SetGrid()
    lib.bunch_draw_xy(b)

    can.cd(2)
    frame2 = gPad.DrawFrame(-200, 0, 200, 2e3)
    lib.bunch_draw_z(b)

    #ut.invert_col(gPad)
    can.SaveAs("01fig.png")

#project_xy

#_____________________________________________________________________________
def pairs_xyz(lib, sim, cross_angle):

    zmax = lib.sim_get_hzmax(sim)

    time = -0.05

    lib.sim_move(sim, c_double(time))

    #can = TCanvas("c1","c1",800,800)
    can = TCanvas("c1","c1",1086, 543)
    can.Divide(2,1)

    can.cd(1)
    frame = gPad.DrawFrame(-1, -1, 1, 1) # xmin, ymin, xmax, ymax in ROOT
    ut.put_frame_yx_tit(frame, "#it{y} (mm)", "#it{x} (mm)", 1, 1.2)

    gPad.SetGrid()
    lib.sim_draw_xy(sim)

    can.cd(2)
    frame2 = gPad.DrawFrame(-150, 0, 150, zmax*1.1)
    lib.sim_draw_z(sim)

    #ut.invert_col(gPad)
    #can.SaveAs("01fig.png")
    can.SaveAs("01fig.pdf")

#pairs_xyz

#_____________________________________________________________________________
def evolution(lib, sim, cross_angle):

    tmin = -0.6
    tmax = 0.6
    nstep = 200

    lib.sim_run_evolution(sim, c_double(tmin), c_double(tmax), nstep)

    can = TCanvas("c1","c1",2400,800)
    can.Divide(3,1)

    can.cd(1)
    gPad.SetGrid()
    lib.sim_draw_xt(sim)

    can.cd(2)
    gPad.SetGrid()
    gPad.SetLogy()
    lib.sim_draw_yt(sim)

    can.cd(3)
    gPad.SetGrid()
    lib.sim_draw_zt(sim)

    can.SaveAs("01fig.pdf")

#evolution

#_____________________________________________________________________________
def make_plot_pairs(lib, sim, cross_angle):

    time = 0.

    #maximum for z pairs
    zpmax = lib.sim_get_hzmax(sim)

    lib.sim_move(sim, c_double(time))

    can = TCanvas("c1","c1",950,950)

    create_plot_pairs(lib, sim, cross_angle, can, zpmax, time, "01fig.png")

#make_plot_pairs

#_____________________________________________________________________________
def create_plot_pairs(lib, sim, cross_angle, can, zpmax, time, outnam):

    zmin = -370
    zmax = 370

    xmin = -10
    xmax = 10

    tsiz = 0.045
    tsiz2 = 0.04

    invert = True

    #electron and proton beams
    beam_el = beam_lin(zmin, zmax)
    beam_p = beam_lin(zmin, zmax, -cross_angle)
    beam_p.col = rt.kRed

    can.SetMargin(0, 0, 0, 0)
    #can = TCanvas("c1","c1",1086, 543)
    can.Divide(1, 2, 0, 0)

    can.cd(1)

    frame = gPad.DrawFrame(zmin, xmin, zmax, xmax) # xmin, ymin, xmax, ymax in ROOT
    ut.put_frame_yx_tit(frame, "#it{x} (mm)", "#it{z} (mm)", 0.6, 1.2)
    ut.set_frame_text_size(frame, tsiz)
    ut.set_margin_lbtr(gPad, 0.06, 0.11, 0.03, 0.01)
    gPad.SetGrid()
    #frame.Draw()

    beam_el.draw()
    beam_p.draw()

    leg = ut.prepare_leg(0.75, 0.73, 0.15, 0.22, tsiz)
    hle = TH1D()
    hle.SetMarkerColor(rt.kBlue)
    hle.SetMarkerStyle(rt.kFullCircle)
    hlp = TH1D()
    hlp.SetMarkerColor(rt.kRed)
    hlp.SetMarkerStyle(rt.kFullCircle)
    leg.AddEntry("", "#it{t} = "+"{0:.2f}".format(time)+" ns", "")
    leg.AddEntry(hle, "Electrons", "p")
    leg.AddEntry(hlp, "Protons", "p")
    leg.Draw("same")

    lib.sim_draw(sim)

    if invert: ut.invert_col(gPad)

    can.cd(2)
    gPad.Divide(2, 1, 0, 0)

    can.cd(2)
    gPad.cd(1)

    frame2 = gPad.DrawFrame(-1, -1, 1, 1) # xmin, ymin, xmax, ymax in ROOT
    ut.put_frame_yx_tit(frame2, "#it{y} (mm)", "#it{x} (mm)", 1.5, 1.2)
    ut.set_frame_text_size(frame2, tsiz2)
    ut.set_margin_lbtr(gPad, 0.12, 0.14, 0.02, 0.1)
    gPad.SetGrid()
    #frame2.Draw()

    lib.sim_draw_xy(sim)

    if invert: ut.invert_col(gPad)

    can.cd(2)
    gPad.cd(2)

    frame3 = gPad.DrawFrame(-150, 0, 150, zpmax*1.1)
    ut.put_frame_yx_tit(frame3, "Bunch overlap (a.u.)", "#it{z} (mm)", 1.5, 1.2)
    frame3.GetYaxis().CenterTitle(rt.kFALSE)
    ut.set_margin_lbtr(gPad, 0.14, 0.14, 0.02, 0.04)
    ut.set_frame_text_size(frame3, tsiz2)
    gPad.SetGrid()
    frame3.Draw()

    lib.sim_draw_z(sim)

    if invert: ut.invert_col(gPad)

    can.SaveAs(outnam)

#create_plot_pairs

#_____________________________________________________________________________
def video_pairs(lib, sim, cross_angle):

    tmin = -0.7
    tmax = 0.6
    nstep = 200

    out = "movie.mp4"

    #maximum for z pairs
    zpmax = lib.sim_get_hzmax(sim)

    dt = float(tmax-tmin)/nstep
    time = tmin-dt
    lib.sim_move(sim, c_double(time))

    can = TCanvas("c1","c1",950,950)

    os.system("rm -f "+out)
    os.system("rm -rf tmp")
    os.system("mkdir tmp")

    for i in range(nstep):

        lib.sim_move(sim, c_double(dt))

        time += dt
        can.Clear()

        nam = "tmp/fig_"+"{0:04d}".format(i)+".png"
        create_plot_pairs(lib, sim, cross_angle, can, zpmax, time, nam)

    os.system("ffmpeg -r 30 -i tmp/fig_%04d.png -r 30 "+out)
    os.system("rm -rf tmp")

#video_pairs

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetFrameLineWidth(2)
    gStyle.SetPalette(1)

    main()
















