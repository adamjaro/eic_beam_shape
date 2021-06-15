
//_____________________________________________________________________________
//
// Simulation implementation
//
//_____________________________________________________________________________

//C++
#include <iostream>

//ROOT
#include "TGraph.h"
#include "TVector3.h"
#include "TFile.h"

//local classes
#include "bunch.h"
#include "sim.h"

using namespace std;

//_____________________________________________________________________________
sim::sim() {

}//sim

//_____________________________________________________________________________
void sim::move(double dt) {

  for(auto i = bunches.begin(); i<bunches.end(); i++) {

    (*i)->move(dt);
  }

  make_pairs();

}//move

//_____________________________________________________________________________
void sim::set_bins(int nx, double xmin, double xmax, int ny, double ymin, double ymax, int nz, double zmin, double zmax) {

  for(auto i = bunches.begin(); i<bunches.end(); i++) {

    (*i)->set_bins(nx, xmin, xmax, ny, ymin, ymax, nz, zmin, zmax);
  }

  hxy.SetBins(nx, xmin, xmax, ny, ymin, ymax);
  hz.SetBins(nz, zmin, zmax);

  make_pairs();

  xymax = hxy.GetMaximum();

  hxt.SetBins(nx, xmin, xmax);
  hyt.SetBins(ny, ymin, ymax);
  hzt.SetBins(nz, zmin, zmax);

}//set_bins

//_____________________________________________________________________________
void sim::make_pairs() {

  hxy.Reset();
  hz.Reset();

  bunch *b0 = bunches[0];
  bunch *b1 = bunches[1];

  //electron-proton pairs in bunches
  for(int ix=0; ix<hxy.GetNbinsX()+1; ix++) {
    for(int iy=0; iy<hxy.GetNbinsY()+1; iy++) {
      for(int iz=0; iz<hz.GetNbinsX()+1; iz++) {

        double nb0 = b0->get_hxyz().GetBinContent(ix, iy, iz);
        double nb1 = b1->get_hxyz().GetBinContent(ix, iy, iz);
 
        double npair = min(nb0, nb1);

        hxy.SetBinContent(ix, iy, npair+hxy.GetBinContent(ix, iy));
        hz.SetBinContent(iz, npair+hz.GetBinContent(iz));

      }//z
    }//y
  }//x

}//make_pairs

//_____________________________________________________________________________
void sim::run_evolution(double tmin, double tmax, int nstep) {

  //bunches evolution over time interval in steps

  double dt = (tmax-tmin)/nstep;

  move(tmin-dt);

  for(int i=0; i<nstep; i++) {

    cout << i << endl;

    move(dt);

    for(int ix=0; ix<hxy.GetNbinsX()+1; ix++) {
      for(int iy=0; iy<hxy.GetNbinsY()+1; iy++) {

        hxt.AddBinContent(ix, hxy.GetBinContent(ix, iy));
        hyt.AddBinContent(iy, hxy.GetBinContent(ix, iy));

      }//y
    }//x

    for(int iz=0; iz<hz.GetNbinsX()+1; iz++) {

        hzt.AddBinContent(iz, hz.GetBinContent(iz));

    }//z

  }//dt

  TFile out("sim.root", "recreate");

  hxt.Write("hxt");
  hyt.Write("hyt");
  hzt.Write("hzt");

  out.Close();

}//run_evolution

//_____________________________________________________________________________
void sim::draw() {

  for(auto i: bunches) {

    i->draw();
  }

}//draw

//_____________________________________________________________________________
void sim::draw_xy() {

  hxy.SetMinimum(0.98);
  hxy.SetMaximum(xymax);
  hxy.SetContour(300);

  hxy.Draw("colz same");

}//draw_xy

//_____________________________________________________________________________
void sim::draw_z() {

  hz.SetFillColor(kBlue);

  hz.Draw("same");

}//draw_z

//_____________________________________________________________________________
extern "C" {

  sim *make_sim() { return new sim(); }

  void sim_add_bunch(sim& s, bunch *b) { s.add_bunch(b); }

  void sim_move(sim& s, double dt) { s.move(dt); }

  //void sim_set_bins(sim& s) { s.set_bins(); }
  void sim_set_bins(sim& s, int nx, double xmin, double xmax, int ny, double ymin, double ymax, int nz, double zmin, double zmax) {
    s.set_bins(nx, xmin, xmax, ny, ymin, ymax, nz, zmin, zmax);
  }

  void sim_draw(sim& s) { s.draw(); }

  bunch *sim_get_bunch(sim& s, int id) { return s.get_bunch(id); }

  void sim_draw_xy(sim& s) { s.draw_xy(); }

  void sim_draw_z(sim& s) { s.draw_z(); }

  int sim_get_hzmax(sim& s) { return s.get_hzmax(); }

  void sim_run_evolution(sim& s, double tmin, double tmax, int nstep) { s.run_evolution(tmin, tmax, nstep); }

  void sim_draw_xt(sim& s) { s.draw_xt(); }
  void sim_draw_yt(sim& s) { s.draw_yt(); }
  void sim_draw_zt(sim& s) { s.draw_zt(); }

}











