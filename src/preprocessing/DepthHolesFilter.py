class DepthHolesFilter(object):

    def __init__(self, foreground=1500, background=2100):
        self.foreground = foreground;
        self.background = background;

    def filter(self, rgb, depth, balls, args = {}):

        shadow = (depth <= self.foreground)
        depth[shadow] = 4095

        bg = (depth > self.background)
        depth[bg] = 4095

        return rgb, depth, balls