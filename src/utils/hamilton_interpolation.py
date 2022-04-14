import cv2
import numpy as np


class Hamilton:
    def __init__(self, path, height=1080, width=1920, dtype='uint16'):
        self.height = height
        self.width = width
        self.img = np.fromfile(path, dtype=dtype).reshape(height, width)
        self.img = np.float32(self.img) / 65535.
        self.result = np.zeros((height, width, 3))

    def offset(self, h, w, offset_h, offset_w):
        if 0 <= w + offset_w < self.width and 0 <= h + offset_h < self.height:
            return self.img[h + offset_h][w + offset_w]
        return 0

    def offset_green(self, h, w, offset_h, offset_w):
        if 0 <= h + offset_h < self.height and 0 <= w + offset_w < self.width:
            return self.result[h + offset_h][w + offset_w][1]
        return 0

    def rebuild_green_channel(self, h, w):
        nabla_h = abs(self.offset(h, w, 0, -1) - self.offset(h, w, 0, 1)) \
                  + abs(2 * self.img[h][w] - self.offset(h, w, 0, -2) - self.offset(h, w, 0, 2))
        nabla_v = abs(self.offset(h, w, -1, 0) - self.offset(h, w, 1, 0)) \
                  + abs(2 * self.img[h][w] - self.offset(h, w, -2, 0) + self.offset(h, w, 2, 0))

        if nabla_h < nabla_v:
            return (self.offset(h, w, 0, -1) + self.offset(h, w, 0, 1)) / 2 \
                   + (2 * self.img[h][w] - self.offset(h, w, 0, -2) - self.offset(h, w, 0, 2)) / 4
        elif nabla_h > nabla_v:
            return (self.offset(h, w, -1, 0) + self.offset(h, w, 1, 0)) / 2 + \
                   (self.img[h][w] - self.offset(h, w, -2, 0) - self.offset(h, w, 2, 0)) / 4
        else:
            return (self.offset(h, w, -1, 0) + self.offset(h, w, 1, 0) + self.offset(h, w, 0, -1) +
                    self.offset(h, w, 0, 1)) / 4 + (4 * self.img[h][w] - self.offset(h, w, -2, 0) -
                    self.offset(h, w, 2, 0) - self.offset(h, w, 0, -2) - self.offset(h, w, 0, 2)) / 8

    def rebuild_red_blue_on_green(self, h, w):
        red = (self.offset(h, w, -1, 0) + self.offset(h, w, 1, 0)) / 2 + \
              (2 * self.img[h][w] - self.offset_green(h, w, -1, 0) - self.offset_green(h, w, 1, 0)) / 2
        blue = (self.offset(h, w, 0, -1) + self.offset(h, w, 0, 1)) / 2 + \
               (2 * self.img[h][w] - self.offset_green(h, w, 0, -1) - self.offset_green(h, w, 0, 1)) / 2
        return red, blue

    def rebuild_blue_on_red(self, h, w):
        d_1 = abs(self.offset(h, w, -1, 1) - self.offset(h, w, 1, -1)) + \
              abs(2 * self.result[h][w][1] - self.offset_green(h, w, -1, 1) - self.offset_green(h, w, 1, -1))
        d_2 = abs(self.offset(h, w, -1, -1) - self.offset(h, w, 1, 1)) + \
              abs(2 * self.result[h][w][1] - self.offset_green(h, w, -1, -1) - self.offset_green(h, w, 1, 1))

        if d_1 < d_2:
            return (self.offset(h, w, -1, 1) + self.offset(h, w, 1, -1)) / 2 + \
                   (2 * self.result[h][w][1] - self.offset_green(h, w, -1, 1) - self.offset_green(h, w, 1, -1)) / 2
        elif d_1 > d_2:
            return (self.offset(h, w, -1, -1) + self.offset(h, w, 1, 1)) / 2 + \
                   (2 * self.result[h][w][1] - self.offset_green(h, w, -1, -1) - self.offset_green(h, w, 1, 1)) / 2
        else:
            return (4 * self.result[h][w][1] - self.offset_green(h, w, -1, 1) -
                    self.offset_green(h, w, 1, -1) - self.offset_green(h, w, -1, -1) - self.offset_green(h, w, 1, 1)) / 4

    def smooth(self):
        for i in range(0, self.height, 2):
            for j in range(0, self.width, 2):
                self.result[i][j][1], self.result[i+1][j+1][1] = self.img[i][j], self.img[i+1][j+1]
                # self.result[i+1][j][1] = self.rebuild_green_channel(i+1, j)
                # self.result[i][j + 1][1] = self.rebuild_green_channel(i, j+1)
                self.result[i+1][j][1] = self.result[i][j][1]
                self.result[i][j + 1][1] = self.result[i+1][j+1][1]
        self.result.clip(0, 1)
        # cv2.imshow('tt', np.uint8(self.result[:, :, 1] * 255))
        # cv2.waitKey(0)
        for i in range(0, self.height, 2):
            for j in range(0, self.width, 2):
                # self.result[i][j][2], self.result[i][j][0] = self.rebuild_red_blue_on_green(i, j)
                # self.result[i+1][j+1][0], self.result[i+1][j+1][2] = self.rebuild_red_blue_on_green(i+1, j+1)
                # self.result[i+1][j][2] = self.img[i+1][j]
                # self.result[i+1][j][0] = self.rebuild_blue_on_red(i+1, j)
                # self.result[i][j+1][0] = self.img[i][j+1]
                # self.result[i][j+1][2] = self.rebuild_blue_on_red(i, j+1)
                self.result[i][j][2], self.result[i][j][0] = self.img[i+1][j], self.img[i][j+1]
                self.result[i+1][j+1][0], self.result[i+1][j+1][2] = self.img[i][j+1], self.img[i+1][j]
                self.result[i+1][j][2] = self.img[i+1][j]
                self.result[i+1][j][0] = self.img[i][j+1]
                self.result[i][j+1][0] = self.img[i][j+1]
                self.result[i][j+1][2] = self.img[i+1][j]
        np.clip(self.result, 0, 1)
        cv2.imwrite('ttttt.png', np.uint8(self.result[:, :, 2] * 255))
        return np.uint8(self.result * 255)


hamilton = Hamilton('./tmp.raw')
result = hamilton.smooth()
cv2.imshow('t', result)
cv2.waitKey(0)
cv2.imwrite('t.png', result)