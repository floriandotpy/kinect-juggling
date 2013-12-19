import numpy as np
import vigra as vi
import cv
from DelayedBuffer import DelayedBuffer

class TemporalFilter(object):

    def __init__(self, minSize=100, maxRegions=50):
        self.buffer = DelayedBuffer(buffersize=5)
        self.minSize = minSize
        self.maxRegions = maxRegions

    def filter(self, rgb, depth, args = {}):

        self.buffer.add(depth)

        previous = self.buffer.get()

        if previous is not None:
            vi_img = vi.Image(previous > depth, dtype=np.uint8)
            vi_img = vi.filters.discErosion(vi_img, 3)
            vi_img = vi.filters.discDilation(vi_img, 1)
            vi_img = vi_img.astype(np.float32)

            vi_label_img = vi.analysis.labelImageWithBackground(vi_img)

            vi.analysis.supportedRegionFeatures(vi_img, vi_label_img)

            features = vi.analysis.extractRegionFeatures(vi_img, vi_label_img)

            regions = features.maxRegionLabel() + 1
            boxes = []
            if regions <= self.maxRegions:
                for i in range(1, features.maxRegionLabel() + 1):
                    if features['Sum'][i] >= self.minSize:
                        boxes.append((features['Coord<Minimum>'][i],features['Coord<Maximum>'][i]))

            d = np.array(depth, dtype=np.uint16)

            rgb_cv = cv.fromarray(np.array(rgb[:,:,::-1]))
            for box in boxes:
                [y, x] = box[0]
                [y2, x2] = box[1]
                cv.Rectangle(rgb_cv, (x, y), (x2, y2), cv.CV_RGB(0, 255,0), 2)
            rgb = np.copy(rgb_cv)[:,:,::-1]

        else:
            d = depth

        return rgb, d