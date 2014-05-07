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
* By default, you'll want to `python main.py --detectball --cutoff  --simplehand --dummymode`

TODO / Ideas
===

* Filter potential ball positions to only include circular shapes 
 in depth image. 
 Demo*: `python main.py --cutoff--dummymode --showdepth --slowmotion`
 Pretty sure hands can already be filtered in most positions (not all, but that is okay)
 In Code: `RectsFilter.py:51` `ball_list.append(dict(position=ball_center, radius=ball_radius))` only execute this, if the detected shape is kind of circular
* there MUST be a bug in `TrajectoryBall.py` - the idea should work better than it does right now. Find this!
