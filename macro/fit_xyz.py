#!/usr/bin/python3

from ROOT import TFile

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np
import collections

import os

#_____________________________________________________________________________
def main():

    iplot = 3
    funclist = []
    funclist.append( fit_x ) # 0
    funclist.append( fit_y ) # 1
    funclist.append( fit_z ) # 2
    funclist.append( fit_xyz ) # 3

    funclist[iplot]()

#_____________________________________________________________________________
def fit_x(nam=None, out="01fig.pdf", title=None):

    if nam is None:
        #nam = "../sim_noy.root"
        #nam = "../sim_y.root"
        nam = "../sim.root"
        print("Local input: ", nam)

    inp = TFile.Open(nam)
    hx = inp.Get("hxt")

    #input distribution
    edges, content = h1_to_np(hx)

    #Gaussian fit
    centers = (0.5*( edges[1:] + edges[:-1]) )
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, content)

    #make the plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    plt.rc("text", usetex = True)

    fig, ax = plt.subplots(1, 1)
    set_axes_color(ax, col)

    ax.set_xlabel("$x$ (mm)")
    ax.set_ylabel("Normalized counts")
    if title is not None:
        ax.set_title(title)

    #plt.bar(edges[:-1], content, width=edges[1]-edges[0], align="edge")

    #data
    plot_np_step(ax, edges, content, "blue")

    #fit function
    x = np.linspace(centers[0], centers[-1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    ax.plot(x, y, "-", label="norm", color="red")

    set_grid(ax, col)
    ax.set_ylim([0, None])

    leg = legend()
    leg.add_entry(leg_txt(), "Bunch overlap in $x$")
    leg.add_entry(leg_lin("red"), "Gaussian fit")
    leg.add_entry(leg_txt(), "$\mu_x$ (mm): {0:.4f} $\pm$ {1:.4f}".format( pars[0], np.sqrt(cov[0,0]) ))
    leg.add_entry(leg_txt(), "$\sigma_x$ (mm): {0:.4f} $\pm$ {1:.4f}".format( pars[1], np.sqrt(cov[1,1]) ))
    leg.draw(plt, col)

    #log the results
    log = open("out.txt", "a+")
    log.write( "    $\mu_x$ (mm):    {0:.4f} $\pm$ {1:.4f}\n".format( pars[0], np.sqrt(cov[0,0]) ) )
    log.write( "    $\sigma_x$ (mm): {0:.4f} $\pm$ {1:.4f}\n\n".format( pars[1], np.sqrt(cov[1,1]) ) )

    fig.savefig(out, bbox_inches = "tight")

#fit_x

#_____________________________________________________________________________
def fit_y(nam=None, out="01fig.pdf", title=None):

    if nam is None:
        #nam = "../sim_noy.root"
        #nam = "../sim_y.root"
        nam = "../sim.root"
        print("Local input: ", nam)

    inp = TFile.Open(nam)
    hx = inp.Get("hyt")

    #input distribution
    edges, content = h1_to_np(hx)

    #Gaussian fit
    centers = (0.5*( edges[1:] + edges[:-1]) )
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, content)

    #make the plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    plt.rc("text", usetex = True)
    plt.rc("text.latex", preamble=r"\usepackage{siunitx}")

    fig, ax = plt.subplots(1, 1)
    set_axes_color(ax, col)

    ax.set_xlabel("$y$ (mm)")
    ax.set_ylabel("Normalized counts")
    if title is not None:
        ax.set_title(title)

    #data
    plot_np_step(ax, edges, content, "blue")

    #fit function
    x = np.linspace(centers[0], centers[-1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    ax.plot(x, y, "-", label="norm", color="red")

    set_grid(ax, col)
    ax.set_ylim([0, None])

    leg = legend()
    leg.add_entry(leg_txt(), "Bunch overlap in $y$")
    leg.add_entry(leg_lin("red"), "Gaussian fit")
    leg.add_entry(leg_txt(), "$\mu_y$ (\si{\micro\meter}): "+"{0:.4f} $\pm$ {1:.4f}".format( pars[0]*1e3, np.sqrt(cov[0,0]*1e3) ))
    leg.add_entry(leg_txt(), "$\sigma_y$ (\si{\micro\meter}): "+"{0:.4f} $\pm$ {1:.4f}".format( pars[1]*1e3, np.sqrt(cov[1,1]*1e3) ))
    leg.draw(plt, col)

    #log the results
    log = open("out.txt", "a+")
    log.write( "    $\mu_y$ (\si{\micro\meter}):    "+"{0:.4f} $\pm$ {1:.4f}\n".format( pars[0]*1e3, np.sqrt(cov[0,0]*1e3) ) )
    log.write( "    $\sigma_y$ (\si{\micro\meter}): "+"{0:.4f} $\pm$ {1:.4f}\n\n".format( pars[1]*1e3, np.sqrt(cov[1,1]*1e3) ) )

    fig.savefig(out, bbox_inches = "tight")

#fit_y

#_____________________________________________________________________________
def fit_z(nam=None, out="01fig.pdf", title=None):

    if nam is None:
        #nam = "../sim_noy.root"
        #nam = "../sim_y.root"
        nam = "../sim.root"
        print("Local input: ", nam)

    inp = TFile.Open(nam)
    hx = inp.Get("hzt")

    #input distribution
    edges, content = h1_to_np(hx)

    #Gaussian fit
    centers = (0.5*( edges[1:] + edges[:-1]) )
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, content, p0=[0, 10])

    #make the plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    plt.rc("text", usetex = True)

    fig, ax = plt.subplots(1, 1)
    set_axes_color(ax, col)

    ax.set_xlabel("$z$ (mm)")
    ax.set_ylabel("Normalized counts")
    if title is not None:
        ax.set_title(title)

    #data
    plot_np_step(ax, edges, content, "blue")

    #fit function
    x = np.linspace(centers[0], centers[-1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    ax.plot(x, y, "-", label="norm", color="red")

    set_grid(ax, col)
    ax.set_ylim([0, None])

    leg = legend()
    leg.add_entry(leg_txt(), "Bunch overlap in $z$")
    leg.add_entry(leg_lin("red"), "Gaussian fit")
    leg.add_entry(leg_txt(), "$\mu_z$ (mm): {0:.2f} $\pm$ {1:.2f}".format( pars[0], np.sqrt(cov[0,0]) ))
    leg.add_entry(leg_txt(), "$\sigma_z$ (mm): {0:.2f} $\pm$ {1:.2f}".format( pars[1], np.sqrt(cov[1,1]) ))
    leg.draw(plt, col)

    #log the results
    log = open("out.txt", "a+")
    log.write( "    $\mu_z$ (mm):    {0:.2f} $\pm$ {1:.2f}\n".format( pars[0], np.sqrt(cov[0,0]) ) )
    log.write( "    $\sigma_z$ (mm): {0:.2f} $\pm$ {1:.2f}\n".format( pars[1], np.sqrt(cov[1,1]) ) )

    fig.savefig(out, bbox_inches = "tight")

#fit_z

#_____________________________________________________________________________
def fit_xyz():

    #nam = "../sim_noy.root"
    #nam = "../sim_y.root"
    #nam = "../sim_5.root"
    #nam = "../sim_10.root"
    #nam = "../sim_18.root"
    nam = "../sim.root"

    #title = ", no y-angle"
    #title = ", y-angle included"
    title = ""

    os.system("rm -rf tmp")
    os.system("mkdir tmp")

    #fit_x(nam, "tmp/x.pdf", "Overlap in $x$"+title)
    #fit_y(nam, "tmp/y.pdf", "Overlap in $y$"+title)
    #fit_z(nam, "tmp/z.pdf", "Overlap in $z$"+title)

    #log the results (done in the individual functions)
    out = open("out.txt", "w")

    fit_x(nam, "tmp/x.pdf")
    fit_y(nam, "tmp/y.pdf")
    fit_z(nam, "tmp/z.pdf")

    out.close()

    os.system("pdfjam --nup 3x1 --papersize '{30in,8in}' --outfile 01fig.pdf tmp/x.pdf tmp/y.pdf tmp/z.pdf")
    os.system("rm -rf tmp")

#fit_xyz

#_____________________________________________________________________________
def h1_to_np(hx):

    #bin edges and content from TH1

    edges = np.zeros(hx.GetNbinsX()+1)
    content = np.zeros(hx.GetNbinsX())
    hsum = 0.
    nbins = hx.GetNbinsX()
    for i in range(nbins):
        edges[i] = hx.GetBinLowEdge(i)
        content[i] = hx.GetBinContent(i)
        hsum += content[i]

    #upper edge of last bin
    edges[nbins] = hx.GetBinLowEdge(nbins-1) + hx.GetBinWidth(nbins-1)

    #normalize the content to density
    for i in range(len(content)):
        content[i] = content[i]/(hsum*(edges[1]-edges[0]))

    return edges, content

#h1_to_np

#_____________________________________________________________________________
def plot_np_step(plt, edges, content, col):

    ix = []
    iy = []
    for i in range(len(content)):
        ix.append( edges[i] )
        ix.append( edges[i+1] )
        iy.append( content[i] )
        iy.append( content[i] )

    plt.plot(ix, iy, color=col, ls="-")

#plot_np_step

#_____________________________________________________________________________
def set_grid(px, col="lime"):

    px.grid(True, color = col, linewidth = 0.5, linestyle = "--")

#set_grid

#_____________________________________________________________________________
def set_axes_color(ax, col):

    #[t.set_color('red') for t in ax.xaxis.get_ticklines()]
    #[t.set_color('red') for t in ax.xaxis.get_ticklabels()]

    ax.xaxis.label.set_color(col)
    ax.yaxis.label.set_color(col)
    ax.tick_params(which = "both", colors = col)
    ax.spines["bottom"].set_color(col)
    ax.spines["left"].set_color(col)
    ax.spines["top"].set_color(col)
    ax.spines["right"].set_color(col)

#set_axes_color

#_____________________________________________________________________________
class legend:
    def __init__(self):
        self.items = []
        self.data = []
    def add_entry(self, i, d):
        self.items.append(i)
        self.data.append(d)
    def draw(self, px, col=None, **kw):
        leg = px.legend(self.items, self.data, **kw)
        if col is not None:
            px.setp(leg.get_texts(), color=col)
            if col != "black":
                leg.get_frame().set_edgecolor("orange")
        return leg

#_____________________________________________________________________________
def leg_lin(col, sty="-"):
    return Line2D([0], [0], lw=2, ls=sty, color=col)

#_____________________________________________________________________________
def leg_txt():
    return Line2D([0], [0], lw=0)

#_____________________________________________________________________________
def leg_dot(fig, col, siz=8):
    return Line2D([0], [0], marker="o", color=fig.get_facecolor(), markerfacecolor=col, markersize=siz)

#_____________________________________________________________________________
if __name__ == "__main__":

    main()












