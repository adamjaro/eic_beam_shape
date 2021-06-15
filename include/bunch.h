#ifndef bunch_h
#define bunch_h

//bunch representation

#include <vector>
#include "TH3D.h"
class TVector3;

class bunch {

  public:

    bunch(int npart, double rmsx, double bsx, double rmsy, double bsy, double rmsz);

    void rotate_y(double a);
    void set_color(Color_t col) {gr.SetMarkerColor(col);}

    void set_bins(int nx, double xmin, double xmax, int ny, double ymin, double ymax, int nz, double zmin, double zmax);

    void set_kinematics(double en, double m, double dx, double dy, double dz);
    void move(double dt);

    TH3D& get_hxyz() { return hxyz; }

    void print();
    void draw();
    void draw_xy();
    void draw_z();

  private:

    std::vector<TVector3> points; // particles in bunch
    TGraph gr; // graph xz representation
    TH3D hxyz; // particle distribution in x, y and z

    double vel; // velocity in mm/ns
    TVector3 dir; // direction unit vector

};

#endif


