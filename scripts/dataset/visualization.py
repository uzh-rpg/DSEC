import cv2
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np


def disp_img_to_rgb_img(disp_array: np.ndarray):
    disp_pixels = np.argwhere(disp_array > 0)
    u_indices = disp_pixels[:, 1]
    v_indices = disp_pixels[:, 0]
    disp = disp_array[v_indices, u_indices]
    max_disp = 80

    norm = mpl.colors.Normalize(vmin=0, vmax=max_disp, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap='inferno')

    disp_color = mapper.to_rgba(disp)[..., :3]
    output_image = np.zeros((disp_array.shape[0], disp_array.shape[1], 3))
    output_image[v_indices, u_indices, :] = disp_color
    output_image = (255 * output_image).astype("uint8")
    output_image = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
    return output_image

def show_image(image):
    cv2.namedWindow('viz', cv2.WND_PROP_FULLSCREEN)
    cv2.imshow('viz', image)
    cv2.waitKey(0)

def get_disp_overlay(image_1c, disp_rgb_image, height, width):
    image = np.repeat(image_1c[..., np.newaxis], 3, axis=2)
    overlay = cv2.addWeighted(image, 0.1, disp_rgb_image, 0.9, 0)
    return overlay

def show_disp_overlay(image_1c, disp_rgb_image, height, width):
    overlay = get_disp_overlay(image_1c, disp_rgb_image, height, width)
    show_image(overlay)
