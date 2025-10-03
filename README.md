# Beam shape at the Electron Ion Collider (EIC)

Implements transport model for expected distribution of primary vertices
with electron-proton and electron-nucleus beams at the EIC as was used
in note on beam conditions for EIC, available [here](https://eic.github.io/resources/simulations.html).

## Dependencies

- CERN ROOT
- ffmpeg (for animation)

## Steps to compile

<pre><code> mkdir build </pre></code>
<pre><code> cd build </pre></code>
<pre><code> cmake ../ </pre></code>
<pre><code> make </pre></code>

## Run

Example gif animation showing bunch collision for 18x275 GeV ep beams:

<pre><code> ./run.py cards/ep_18x275_Tab3p3.ini </pre></code>

## Configuration

Simulation is configured by .ini file provided to run.py, examples can be found in the *cards* directory.

Particular simulation function is selected by *iplot* parameter in run.py. Function video_pairs() creates
an animation, function evolution() simulates time-integrated vertex distribution.

