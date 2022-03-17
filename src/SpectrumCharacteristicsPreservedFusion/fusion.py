import cv2
import numpy as np
from reflection import *
from transmission import *


def enhancement(vis, nir):
    # vis = cv2.imread('../../data/visual_results/full_resolution_images_of_fig_3_and_4/fig_4_a_rgb.tiff')
    # nir = cv2.imread('../../data/visual_results/full_resolution_images_of_fig_3_and_4/fig_4_a_nir.tiff')[:, :, 0]

    # reflection model
    reflection = reflection_model_init(vis, nir)
    reflection = reflection_model(reflection)

    # transmission model
    first_base_layer_b, second_base_layer_b = base_layer(vis[:, :, 0])
    first_base_layer_g, second_base_layer_g = base_layer(vis[:, :, 1])
    first_base_layer_r, second_base_layer_r = base_layer(vis[:, :, 2])
    first_base_layer_n, second_base_layer_n = base_layer(nir)

    first_detail_layer_b, second_detail_layer_b = detail_layer(vis[:, :, 0], first_base_layer_b, second_base_layer_b)
    first_detail_layer_g, second_detail_layer_g = detail_layer(vis[:, :, 1], first_base_layer_g, second_base_layer_g)
    first_detail_layer_r, second_detail_layer_r = detail_layer(vis[:, :, 2], first_base_layer_r, second_base_layer_r)
    first_detail_layer_n, second_detail_layer_n = detail_layer(nir, first_base_layer_n, second_base_layer_n)

    first_gradient_map_b, second_gradient_map_b = gradient_map(first_detail_layer_b, second_detail_layer_b)
    first_gradient_map_g, second_gradient_map_g = gradient_map(first_detail_layer_g, second_detail_layer_g)
    first_gradient_map_r, second_gradient_map_r = gradient_map(first_detail_layer_r, second_detail_layer_r)
    first_gradient_map_n, second_gradient_map_n = gradient_map(first_detail_layer_n, second_detail_layer_n)

    first_transmission_b = transmission_model(vis[:, :, 0], first_gradient_map_b, first_gradient_map_n)
    second_transmission_b = transmission_model(vis[:, :, 0], second_gradient_map_b, second_gradient_map_n)
    first_transmission_g = transmission_model(vis[:, :, 1], first_gradient_map_g, first_gradient_map_n)
    second_transmission_g = transmission_model(vis[:, :, 1], second_gradient_map_g, second_gradient_map_n)
    first_transmission_r = transmission_model(vis[:, :, 2], first_gradient_map_r, first_gradient_map_n)
    second_transmission_r = transmission_model(vis[:, :, 2], second_gradient_map_r, second_gradient_map_n)

    # fusion
    first_fusion_weight_b = reflection[:, :, 0] * first_transmission_b
    second_fusion_weight_b = reflection[:, :, 0] * second_transmission_b
    first_fusion_weight_g = reflection[:, :, 1] * first_transmission_g
    second_fusion_weight_g = reflection[:, :, 1] * second_transmission_g
    first_fusion_weight_r = reflection[:, :, 2] * first_transmission_r
    second_fusion_weight_r = reflection[:, :, 2] * second_transmission_r

    fusion_map = np.float32(vis.copy())
    fusion_map[:, :, 0] = second_base_layer_b * (second_detail_layer_b * second_fusion_weight_b + second_detail_layer_n * (1 - second_fusion_weight_b))
    fusion_map[:, :, 0] = fusion_map[:, :, 0] * (first_detail_layer_b * first_fusion_weight_b + first_detail_layer_n * (1 - first_fusion_weight_b))
    fusion_map[:, :, 1] = second_base_layer_g * (second_detail_layer_g * second_fusion_weight_g + second_detail_layer_n * (1 - second_fusion_weight_g))
    fusion_map[:, :, 1] = fusion_map[:, :, 1] * (first_detail_layer_g * first_fusion_weight_g + first_detail_layer_n * (1 - first_fusion_weight_g))
    fusion_map[:, :, 2] = second_base_layer_r * (second_detail_layer_r * second_fusion_weight_r + second_detail_layer_n * (1 - second_fusion_weight_r))
    fusion_map[:, :, 2] = fusion_map[:, :, 2] * (first_detail_layer_r * first_fusion_weight_r + first_detail_layer_n * (1 - first_fusion_weight_r))
    fusion_map = np.uint8(fusion_map * 255)
    # cv2.imshow('f', fusion_map)
    # cv2.waitKey(0)

    fusion_map = light_enhance(fusion_map, nir)
    fusion_map = np.uint8(fusion_map)
    # cv2.imshow('f', fusion_map)
    # cv2.waitKey(0)
    return fusion_map