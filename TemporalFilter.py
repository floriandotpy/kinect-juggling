import numpy as np
try:
    import vigra as vi
except:
    print "ERROR: vigra not installed. Cannot use temporal filtering"
from DelayedBuffer import DelayedBuffer

class TemporalFilter(object):

    def __init__(self):
        self.buffer = DelayedBuffer(buffersize=5)

    def filter(self, rgb, depth, args = {}):
        # d1 = self.buffer.get()

        self.buffer.add(depth)

        # d2 = self.buffer.get()

        previous = self.buffer.get()

        if previous is not None:
            vimg = vi.Image(previous < depth, dtype=np.uint8)
            vimg = vi.filters.discErosion(vimg, 3)
            vimg = vi.filters.discDilation(vimg, 1)

            vi_label_img = vi.analysis.labelImageWithBackground(vimg)
            # vi.imshow(vi_label_img)
            # vi.analysis.supportedRegionFeatures(diff, vi_label_img)
            features = vi.analysis.extractRegionFeatures(diff, vi_label_img)
            region_count = features.maxRegionLabel()+1
            print region_count

            # depth[diff == 0] = 0

            d = np.array(vi_label_img, dtype=np.uint16)

            # d = d * 4095
            # d[diff == 0] = 0
            # d[d >= 4000] = 0

        else:
            d = depth

        # if d1 is not None:
            # diff = (d1 - d2) + 2048
        # else:
            # diff = d2

        # print diff[300:305,300:305]


        # trash = (diff < 2048 + 300)

        # depth[(diff < 2048)] = 4095

        # trash = diff > 0

        # depth[trash] = 4095


        return rgb, d