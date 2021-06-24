
//_____________________________________________________________________________
//
// Bunch representation
//
//_____________________________________________________________________________

//C++
#include <iostream>
#include <math.h>

//ROOT
#include "TVector3.h"
#include "TF1.h"
#include "TGraph.h"
#include "TLorentzVector.h"
#include "TProfile2D.h"
#include "TH1D.h"

//local classes
#include "bunch.h"

using namespace std;

//_____________________________________________________________________________
bunch::bunch(int npart, double rmsx, double bsx, double rmsy, double bsy, double rmsz) {

  //RMS emittance h/v, rmsx and rmsy in nm
  //beta* h/v, bsx and bsy in cm
  //RMS bunch length, rmsz in cm

  //width in x, mm
  double sx = sqrt( rmsx*1e-6*bsx*10 );
  double smax = 4;
  auto fx = TF1("fx", "gaus", -smax*sx, smax*sx);
  fx.SetParameters(1, 0, sx);

  //width in y, mm
  double sy = sqrt( rmsy*1e-6*bsy*10 );
  auto fy = TF1("fy", "gaus", -smax*sy, smax*sy);
  fy.SetParameters(1, 0, sy);

  //width in z, mm
  double sz = rmsz*10;
  auto fz = TF1("fz", "gaus", -smax*sz, smax*sz);
  fz.SetParameters(1, 0, sz);

  //bunch particles
  for(int i=0; i<npart; i++) {

    points.push_back(TVector3(fx.GetRandom(), fy.GetRandom(), fz.GetRandom()));
  }

  gr.Set(npart);
  gr.SetMarkerColor(kBlue);
  gr.SetMarkerStyle(kFullCircle);
  //gr.SetMarkerSize(0.2);
  gr.SetMarkerSize(0.1);

}//bunch

//_____________________________________________________________________________
void bunch::rotate_y(double a) {

  //rotate individual particles along y, angle a in mrad

  for(int i=0; i<points.size(); i++) {

    points[i].RotateY(a*1e-3);
  }

}//rotate_y

//_____________________________________________________________________________
void bunch::set_kinematics(double en, double p, double dx, double dy, double dz) {

  auto vec = TLorentzVector();
  vec.SetPxPyPzE(0, 0, p, en);
  double beta = vec.Beta();

  //cout << beta << endl;
  //cout << vec.Gamma() << endl;

  double light = 299.792; // mm/ns

  vel = beta*light;

  dir.SetXYZ(dx, dy, dz);

}//set_kinematics

//_____________________________________________________________________________
void bunch::set_bins(int nx, double xmin, double xmax, int ny, double ymin, double ymax, int nz, double zmin, double zmax) {

  //hxyz.SetBins(60, -2, 2, 60, -2, 2, 60, -200, 200);

  hxyz.SetBins(nx, xmin, xmax, ny, ymin, ymax, nz, zmin, zmax);

  //initial particle distribution
  hxyz.Reset();

  for(auto i: points) {

    hxyz.Fill(i.x(), i.y(), i.z());
  }

}//set_bins

//_____________________________________________________________________________
void bunch::move(double dt) {

  //dt in ns
  double ds = vel*dt;
  auto delt = TVector3(ds*dir.x(), ds*dir.y(), ds*dir.z());

  for(int i=0; i<points.size(); i++) {

    points[i] += delt;
  }

  //particle distribution
  hxyz.Reset();

  for(auto i: points) {

    hxyz.Fill(i.x(), i.y(), i.z());
  }

}//move

//_____________________________________________________________________________
void bunch::print() {

  //cout << "hi from bunch" << endl;

  //cout << "hi from bunch: " << id << endl;

  for(auto i: points) {

    cout << i.x() << " " << i.y() << " " << i.z() << endl;

  }

}//print

//_____________________________________________________________________________
void bunch::draw() {

  for(int i=0; i<points.size(); i++) {

    gr.SetPoint(i, points[i].z(), points[i].x());

  }

  //gr.Draw("psame");
  gr.Draw("*same");

}//draw

//_____________________________________________________________________________
void bunch::draw_xy() {

  auto profile = hxyz.Project3DProfile("yx");

  profile->SetContour(300);

  profile->Draw("colz same");

}//draw_xy

//_____________________________________________________________________________
void bunch::draw_z() {

  auto profile_z = hxyz.ProjectionZ();

  profile_z->Draw("same");

}//draw_z

//_____________________________________________________________________________
extern "C" {

bunch* make_bunch(int npart, double rmsx, double bsx, double rmsy, double bsy, double rmsz) {
//bunch* make_bunch(int npart, double rmsx) {
//bunch* make_bunch(int npart) {

  //return new bunch(npart, 24, 59, 2, 5.7, 0.9);

  return new bunch(npart, rmsx, bsx, rmsy, bsy, rmsz);
}//make_bunch

void bunch_rotate_y(bunch *b, double a) {

  b->rotate_y(a);
}//bunch_rotate_y

void bunch_set_kinematics(bunch& b, double en, double m, double dx, double dy, double dz) {b.set_kinematics(en, m, dx, dy, dz);}

void bunch_move(bunch& b, double dt) {b.move(dt);}

void bunch_set_color(bunch& b, Color_t col) {

  b.set_color(col);
}//bunch_set_color

void bunch_print(bunch *b) {

  b->print();
}//bunch_print

void bunch_draw(bunch& b) {

  b.draw();
}//bunch_draw

void bunch_draw_xy(bunch& b) { b.draw_xy(); }
void bunch_draw_z(bunch& b) { b.draw_z(); }

}//extern "C"















