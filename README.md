kinect-juggling
================

Realtime tracking of juggling objects using the depth information of the Microsoft Kinect. This is the Result - well, work in progress - of a university project in computer graphics and image processing. 

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
* By default, you'll want to `python main.py --detectball --cutoff  --simplehand --dummymode`

Current state
===

Ball detection and tracking works pretty well.

TODO / Ideas
===

* be more robust about the position of the juggler (in particular with regards to distance from the Kinect)
* use the tracking data for more information: count objects, analyse tossing height, detect actual juggling pattern (siteswaps?)