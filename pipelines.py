import math
import cv2 as cv
import numpy as np
from   enum import Enum

def cv_resize(src, d_size, fx, fy, interpolation):
    """
    Resizes an Image.
    Args:
        src: A numpy.ndarray.
        d_size: Size to set the image.
        fx: The scale factor for the x.
        fy: The scale factor for the y.
        interpolation: Opencv enum for the type of interpolation.
    Returns:
        A resized numpy.ndarray.
    """
    return cv.resize(src, d_size, fx = fx, fy = fy, interpolation = interpolation)

def hsv_threshold(input, hue, sat, val):
    """
    Segment an image based on hue, saturation, and value ranges.
    Args:
        input: A BGR numpy.ndarray.
        hue: A list of two numbers the are the min and max hue.
        sat: A list of two numbers the are the min and max saturation.
        lum: A list of two numbers the are the min and max value.
    Returns:
        A black and white numpy.ndarray.
    """
    out = cv.cvtColor(input, cv.COLOR_BGR2HSV)

    return cv.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))

def find_contours(input, external_only):
    """
    Sets the values of pixels in a binary image to their distance to the nearest black pixel.
    Args:
        input: A numpy.ndarray.
        external_only: A boolean. If true only external contours are found.
    Return:
        A list of numpy.ndarray where each one represents a contour.
    """
    if (external_only):
        mode = cv.RETR_EXTERNAL
    else:
        mode = cv.RETR_LIST
    method = cv.CHAIN_APPROX_SIMPLE

    contours, hierarchy = cv.findContours(input, mode = mode, method = method)

    return contours

def filter_contours(input_contours, min_area, min_perimeter, min_width, max_width,
                    min_height, max_height, solidity, max_vertex_count, min_vertex_count,
                    min_ratio, max_ratio, fx, fy):
    """
    Filters out contours that do not meet certain criteria.
    Args:
        input_contours: Contours as a list of numpy.ndarray.
        min_area: The minimum area of a contour that will be kept.
        min_perimeter: The minimum perimeter of a contour that will be kept.
        min_width: Minimum width of a contour.
        max_width: MaxWidth maximum width.
        min_height: Minimum height.
        max_height: Maximimum height.
        solidity: The minimum and maximum solidity of a contour.
        min_vertex_count: Minimum vertex Count of the contours.
        max_vertex_count: Maximum vertex Count.
        min_ratio: Minimum ratio of width to height.
        max_ratio: Maximum ratio of width to height.
    Returns:
        Contours as a list of numpy.ndarray.
    """
    boxes = []
    output = []

    if (input_contours is not None):
        for contour in input_contours:
            x, y, w, h = cv.boundingRect(contour)

            if (w < min_width or w > max_width):
                continue
            if (h < min_height or h > max_height):
                continue

            area = cv.contourArea(contour)
            if (area < min_area):
                continue
            if (cv.arcLength(contour, True) < min_perimeter):
                continue

            hull  = cv.convexHull(contour)
            solid = 100 * area / cv.contourArea(hull)
            if (solid < solidity[0] or solid > solidity[1]):
                continue
            if (len(contour) < min_vertex_count or len(contour) > max_vertex_count):
                continue

            ratio = float(w) / h
            if (ratio < min_ratio or ratio > max_ratio):
                continue

            boxes.append([x / fx, y / fy, w / fx, h / fy])
            output.append(area)

    return np.array(boxes, dtype = np.int64).tolist(), output

class CubeTracking:
    """
    An OpenCV pipeline generated by GRIP.
    """
    def __init__(self):
        """
        Initializes all values to presets or None if need to be set
        """
        self.cv_resize_dsize = (0, 0)
        self.cv_resize_fx = 0.6
        self.cv_resize_fy = 0.6
        self.cv_resize_interpolation = cv.INTER_LINEAR
        self.cv_resize_output = None

        self.hsv_threshold_input = self.cv_resize_output
        self.hsv_threshold_hue = [120, 155]
        self.hsv_threshold_saturation = [100, 255.0]
        self.hsv_threshold_value = [110, 255.0]
        self.hsv_threshold_output = None

        self.find_contours_input = self.hsv_threshold_output
        self.find_contours_external_only = True
        self.find_contours_output = None

        self.filter_contours_contours = self.find_contours_output
        self.filter_contours_min_area = 20.0
        self.filter_contours_min_perimeter = 20.0
        self.filter_contours_min_width = 0.0
        self.filter_contours_max_width = 1000.0
        self.filter_contours_min_height = 0.0
        self.filter_contours_max_height = 1000.0
        self.filter_contours_solidity = [50, 100]
        self.filter_contours_max_vertices = 1000000.0
        self.filter_contours_min_vertices = 0.0
        self.filter_contours_min_ratio = 0.0
        self.filter_contours_max_ratio = 1000.0
        self.filter_contours_output = None

    def findCubes(self, source0):
        """
        Runs the pipeline and sets all outputs to new values.
        """
        # Step CV_resize0:
        self.cv_resize_src = source0
        (self.cv_resize_output) = cv_resize(self.cv_resize_src, self.cv_resize_dsize, self.cv_resize_fx, self.cv_resize_fy, self.cv_resize_interpolation)

        # Step HSV_Threshold0:
        self.hsv_threshold_input = self.cv_resize_output
        (self.hsv_threshold_output) = hsv_threshold(self.hsv_threshold_input, self.hsv_threshold_hue, self.hsv_threshold_saturation, self.hsv_threshold_value)

        # Step Find_Contours0:
        self.find_contours_input = self.hsv_threshold_output
        (self.find_contours_output) = find_contours(self.find_contours_input, self.find_contours_external_only)

        # Step Filter_Contours0:
        self.filter_contours_contours = self.find_contours_output
        (self.filter_contours_output) = filter_contours(self.filter_contours_contours, self.filter_contours_min_area, self.filter_contours_min_perimeter, self.filter_contours_min_width, self.filter_contours_max_width, self.filter_contours_min_height, self.filter_contours_max_height, self.filter_contours_solidity, self.filter_contours_max_vertices, self.filter_contours_min_vertices, self.filter_contours_min_ratio, self.filter_contours_max_ratio, self.cv_resize_fx, self.cv_resize_fy)

        # Returns the info to make a bounding box
        return self.filter_contours_output

class ConeTracking:
    """
    An OpenCV pipeline generated by GRIP.
    """
    def __init__(self):
        """
        Initializes all values to presets or None if need to be set
        """
        self.cv_resize_dsize = (0, 0)
        self.cv_resize_fx = 0.6
        self.cv_resize_fy = 0.6
        self.cv_resize_interpolation = cv.INTER_LINEAR
        self.cv_resize_output = None

        self.hsv_threshold_input = self.cv_resize_output
        self.hsv_threshold_hue = [15, 65]
        self.hsv_threshold_saturation = [135, 255.0]
        self.hsv_threshold_value = [135, 255.0]
        self.hsv_threshold_output = None

        self.find_contours_input = self.hsv_threshold_output
        self.find_contours_external_only = True
        self.find_contours_output = None

        self.filter_contours_contours = self.find_contours_output
        self.filter_contours_min_area = 20.0
        self.filter_contours_min_perimeter = 20.0
        self.filter_contours_min_width = 0.0
        self.filter_contours_max_width = 1000.0
        self.filter_contours_min_height = 0.0
        self.filter_contours_max_height = 1000.0
        self.filter_contours_solidity = [50, 100]
        self.filter_contours_max_vertices = 1000000.0
        self.filter_contours_min_vertices = 0.0
        self.filter_contours_min_ratio = 0.0
        self.filter_contours_max_ratio = 1000.0
        self.filter_contours_output = None

    def findCones(self, source0):
        """
        Runs the pipeline and sets all outputs to new values.
        """
        # Step CV_resize0:
        self.cv_resize_src = source0
        (self.cv_resize_output) = cv_resize(self.cv_resize_src, self.cv_resize_dsize, self.cv_resize_fx, self.cv_resize_fy, self.cv_resize_interpolation)

        # Step HSV_Threshold0:
        self.hsv_threshold_input = self.cv_resize_output
        (self.hsv_threshold_output) = hsv_threshold(self.hsv_threshold_input, self.hsv_threshold_hue, self.hsv_threshold_saturation, self.hsv_threshold_value)

        # Step Find_Contours0:
        self.find_contours_input = self.hsv_threshold_output
        (self.find_contours_output) = find_contours(self.find_contours_input, self.find_contours_external_only)

        # Step Filter_Contours0:
        self.filter_contours_contours = self.find_contours_output
        (self.filter_contours_output) = filter_contours(self.filter_contours_contours, self.filter_contours_min_area, self.filter_contours_min_perimeter, self.filter_contours_min_width, self.filter_contours_max_width, self.filter_contours_min_height, self.filter_contours_max_height, self.filter_contours_solidity, self.filter_contours_max_vertices, self.filter_contours_min_vertices, self.filter_contours_min_ratio, self.filter_contours_max_ratio, self.cv_resize_fx, self.cv_resize_fy)

        # Returns the info to make a bounding box
        return self.filter_contours_output
