kinect-juggling
================

Realtime tracking of juggling objects using the depth information of the Microsoft Kinect. This is the result - well, work in progress - of a university project in computer vision. 

## Demo and current state

Ball detection and tracking works pretty well.

[Demo video](http://quick.as/aygwtl9a).

## Requirements

* libfreenect
* python modules:
    * opencv
    * freenect (with python binding, you'll need the unstable)
    * numpy
* And you'll need to have a kinect wired up to your machine

## Run it

* If you want to use the dummymode, set a symlink to captured frames like so: `ln -s ~/Dropbox/Uni\ 2013/Bildverarbeitung/frames frames`
* Then just run `python <script>` for whatever script you like. Well, right now there's just one.
* By default, you'll want to `python main.py --detectball --cutoff  --dummymode --handtracking --simplehand`

## TODO / Ideas

* be more robust about the position of the juggler (in particular with regards to distance from the Kinect)
* use the tracking data for more information: count objects, analyse tossing height, detect actual juggling pattern (siteswaps?)
* read from OpenNI file (very WIP): `python main.py --cutoff  --openni --handtracking --simplehand --detectball`

## Licensed under MIT License (MIT)

**The MIT License (MIT)**

Copyright (c) 2014 Florian Letsch, Rolf Boomgaarden, Thiemo Gries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
