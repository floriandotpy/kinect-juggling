Bildverarbeitung
================

Collected code samples for a university project in computer graphics and image
processing, mainly working with the Kinect. For now this is just demo code
until we start working on something serious.

Requirements
===

* libfreenect
* python modules:
    * opencv
    * freenect (with python binding, you'll need the unstable)
    * numpy
* And you'll need to have a kinect wired up to your machine

Run it
===

* If you want to use the dummymode, set a symlink to captured frames like so: `ln -s ~/Dropbox/Uni\ 2013/Bildverarbeitung/frames frames`
* Then just run `python <script>` for whatever script you like. Well, right now there's just one.
* By default, you'll want to `python main.py --dummymode --detectball --cutoff`