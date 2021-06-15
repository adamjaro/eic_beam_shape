#ifndef sim_h
#define sim_h

//simulation

#include "TH1D.h"
#include "TH2D.h"

class sim {

  public:

    sim();

    void add_bunch(bunch *b) { bunches.push_back(b); }
    void move(double dt);

    void set_bins(int nx=60, double xmin=-2, double xmax=2, int ny=60, double ymin=-2, double ymax=2, int nz=60,
      double zmin=-200, double zmax=200);

    void run_evolution(double tmin, double tmax, int nstep);

    void draw();
    bunch *get_bunch(int id) { return bunches[id]; }
    void draw_xy();
    void draw_z();

    void draw_xt() { hxt.Draw(); }
    void draw_yt() { hyt.Draw(); }
    void draw_zt() { hzt.Draw(); }

    int get_hzmax() { return hz.GetMaximum(); }

  private:

    void make_pairs();

    std::vector<bunch*> bunches; // bunches in simulation

    TH2D hxy; // pairs distribution in x and y
    TH1D hz; // pairs distribution in z
    TH1D hxt, hyt, hzt; // time integrals in pairs along x, y and z

    double xymax; // initial maximum in xy

};

#endif

