import cv2
import heapq
import numpy as np


def get_invert(img):
    return 255 - img


def get_air_light(invert):
    row, column = invert.shape[0], invert.shape[1]
    invert_min = invert.min(-1).flatten()
    finds = heapq.nlargest(100, zip(invert_min, range(len(invert_min))))
    index = [i for v, i in finds]

    air_light = [0, 0, 0]
    for i in index:
        r, c = int(i / column), i % column
        if sum(invert[r][c]) > sum(air_light):
            air_light = invert[r][c]
    return air_light


def get_min_val(invert_pad, air_light, channel, center_i, center_j):
    min_val = 255
    for i in range(center_i - 4, center_i + 4):
        for j in range(center_j - 4, center_j + 4):
            min_val = min(min_val, invert_pad[center_i][center_j][channel] / air_light[channel])
    return min_val


def get_transmission(invert, air_light):
    omega, kernel, offset = 0.8, 9, 4
    invert_pad = np.pad(invert, pad_width=((4, 4), (4, 4), (0, 0)), mode='constant', constant_values=(255))
    transmission = invert[:, :, 0].copy() * 1.0
    for i in range(offset, invert.shape[0] + offset):
        for j in range(offset, invert.shape[1] + offset):
            for c in range(3):
                transmission[i - offset][j - offset] = min(transmission[i - offset][j - offset],
                                                           get_min_val(invert_pad, air_light, c, i, j))
            transmission[i - offset][j - offset] = 1 - omega * transmission[i - offset][j - offset]
    return transmission


def enhance(invert, air_light, transmission):
    for i in range(transmission.shape[0]):
        for j in range(transmission.shape[1]):
            if transmission[i][j] < 0.5:
                transmission[i][j] = 2 * transmission[i][j] * transmission[i][j]
    result = invert.copy()
    for c in range(3):
        result[:, :, c] = (invert[:, :, c] - air_light[c])
        result[:, :, c] /=  transmission
        result[:, :, c] +=  air_light[c]
    return result


if __name__ == '__main__':
    img = cv2.imread('../test/80_rgb.bmp')
    img = np.double(img)

    invert = get_invert(img)

    air_light = get_air_light(invert)

    transmission = get_transmission(invert, air_light)

    result = enhance(invert, air_light, transmission)
    result = get_invert(result)

    result = np.uint8(result)
    cv2.imwrite('result.png', result)
    cv2.imshow('result', result)
    cv2.waitKey(0)

