import cv2
import numpy as np


def guide_filter(I, p, win_size=5, eps=0.01):
    mean_I = cv2.blur(I, (win_size, win_size))
    mean_p = cv2.blur(p, (win_size, win_size))
    mean_II = cv2.blur(I * I, (win_size, win_size))
    mean_Ip = cv2.blur(I * p, (win_size, win_size))

    var_I = mean_II - mean_I * mean_I
    cov_Ip = mean_Ip - mean_I * mean_p
    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I
    mean_a = cv2.blur(a, (win_size, win_size))
    mean_b = cv2.blur(b, (win_size, win_size))
    return mean_a * I + mean_b


def base_layer(channel):
    channel = channel / 255.
    first_base_layer = guide_filter(channel, channel)
    second_base_layer = cv2.GaussianBlur(first_base_layer, (5, 5), 0)
    return first_base_layer, second_base_layer


def detail_layer(channel, first_base_layer, second_base_layer):
    channel = channel / 255.
    first_detail_layer = channel / (first_base_layer + 0.01)
    second_detail_layer = first_base_layer / (second_base_layer + 0.01)
    return first_detail_layer, second_detail_layer


def gradient_map(first_detail_layer, second_detail_layer):
    first_detail_layer, second_detail_layer = np.float32(first_detail_layer), np.float32(second_detail_layer)
    first_layer_dx = cv2.Sobel(first_detail_layer, cv2.CV_32F, 1, 0)
    first_layer_dy = cv2.Sobel(first_detail_layer, cv2.CV_32F, 0, 1)
    first_layer_gradient = ((first_layer_dx ** 2) + (first_layer_dy ** 2)) ** 0.5

    second_layer_dx = cv2.Sobel(second_detail_layer, cv2.CV_32F, 1, 0)
    second_layer_dy = cv2.Sobel(second_detail_layer, cv2.CV_32F, 0, 1)
    second_layer_gradient = ((second_layer_dx ** 2) + (second_layer_dy ** 2)) ** 0.5

    return first_layer_gradient, second_layer_gradient


def get_sum_win(map, center_x, center_y, win_size=20):
    left = int(max(0, center_y - win_size/2))
    top = int(max(0, center_x - win_size/2))
    right = int(min(map.shape[1]-1, center_y + win_size/2))
    down = int(min(map.shape[0]-1, center_x + win_size/2))
    sum = 0
    for y in range(left, right+1):
        for x in range(top, down+1):
            sum += map[x][y]
    return sum


def transmission_model(channel, vis_gradient, nir_gradient):
    channel = channel / 255.
    trainsmission_weight = vis_gradient.copy()
    kernel = np.array([[1 for i in range(21)] for j in range(21)])
    vis_sum = cv2.filter2D(vis_gradient, -1, kernel)
    nir_sum = cv2.filter2D(nir_gradient, -1, kernel)
    for x in range(vis_gradient.shape[0]):
        for y in range(vis_gradient.shape[1]):
            if vis_sum[x][y] <= nir_sum[x][y]:
                trainsmission_weight[x][y] = vis_sum[x][y] / nir_sum[x][y]
            else:
                trainsmission_weight[x][y] = 1
    # for x in range(vis_gradient.shape[0]):
    #     for y in range(vis_gradient.shape[1]):
    #         vis_win_sum = get_sum_win(vis_gradient, x, y)
    #         nir_win_sum = get_sum_win(nir_gradient, x, y)
    #         if vis_win_sum <= nir_win_sum:
    #             trainsmission_weight[x][y] = vis_win_sum / nir_win_sum
    #         else:
    #             trainsmission_weight[x][y] = 1
    trainsmission_weight = guide_filter(channel, trainsmission_weight)
    return trainsmission_weight

