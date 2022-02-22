#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera
import threading
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *


class Perception():

    def __init__(self,camera):
        self.range_rgb = {
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255)
        }
        self.size = (640, 480)
        self.count = 0
        self.get_roi = False
        self.detect_color = 'None'
        self.target_color = ()
        self.camera = camera
        self.camera.camera_open()

    def getAreaMaxContour(self,contours):
        contour_area_temp = 0
        contour_area_max = 0
        area_max_contour = None

        for c in contours:  # traversal all the contours
            contour_area_temp = math.fabs(cv2.contourArea(c))  # calculate the countour area
            if contour_area_temp > contour_area_max:
                contour_area_max = contour_area_temp
                if contour_area_temp > 300:  # only when the area is greater than 300, the contour of the maximum area is effective to filter interference
                    area_max_contour = c

        return area_max_contour, contour_area_max  # return the maximum area countour

    def get_frame(self, show_frame=False):
        img = self.camera.frame
        if img is not None:
            frame = img.copy()
            if show_frame:
                cv2.imshow('Raw Frame', frame)
            return frame
        return None

    def read_image(self,image):
        self.image = image
        img_h, img_w = image.shape[:2]
        self.img_h = img_h
        self.img_w = img_w
        cv2.line(self.image, (0, int(img_h / 2)), (img_w, int(img_h / 2)), (0, 0, 200), 1)
        cv2.line(self.image, (int(img_w / 2), 0), (int(img_w / 2), img_h), (0, 0, 200), 1)

    def convert2LAB(self):
        frame_resize = cv2.resize(self.image, self.size, interpolation=cv2.INTER_NEAREST)
        frame_gb = cv2.GaussianBlur(frame_resize, (11, 11), 11)
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)
        return frame_lab

    def detect_object(self,frame_lab,frame):
        area_max = 0
        max_area = 0
        color_area_max = None
        areaMaxContour_max = 0
        for i in color_range:
            if i in self.target_color:
                detect_color = i
                frame_mask = cv2.inRange(frame_lab, color_range[detect_color][0], color_range[detect_color][
                    1])  # mathematical operation on the original image and mask
                opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8))  # Opening (morphology)
                closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6, 6), np.uint8))  # Closing (morphology)
                contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # find countour
                areaMaxContour, area_max = self.getAreaMaxContour(contours)  # find the maximum countour
                if areaMaxContour is not None:
                    if area_max > max_area:  # find the maximum area
                        max_area = area_max
                        color_area_max = i
                        areaMaxContour_max = areaMaxContour
        world_x = None  # if no
        world_y = None
        if area_max > 2500:  # find the maximum area
            rect = cv2.minAreaRect(areaMaxContour)
            box = np.int0(cv2.boxPoints(rect))

            roi = getROI(box)  # get roi zone

            img_centerx, img_centery = getCenter(rect, roi, self.size, square_length)  # get the center coordinates of block
            world_x, world_y = convertCoordinate(img_centerx, img_centery, self.size)  # convert to world coordinates

            cv2.drawContours(frame, [box], -1, self.range_rgb[detect_color], 2)
            cv2.putText(frame, '(' + str(world_x) + ',' + str(world_y) + ')', (min(box[0, 0], box[2, 0]), box[2, 1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.range_rgb[detect_color], 1)  # draw center position

            if color_area_max == 'red':  # red area is the maximum
                color = 1
            elif color_area_max == 'green':  # green area is the maximum
                color = 2
            elif color_area_max == 'blue':  # blue area is the maximum
                color = 3
            else:
                color = 0
            color_list.append(color)

            if len(color_list) == 3:  # multipe judgments
                # take evaluation value
                color = int(round(np.mean(np.array(color_list))))
                color_list = []
                if color == 1:
                    detect_color = 'red'
                    draw_color = range_rgb["red"]
                elif color == 2:
                    detect_color = 'green'
                    draw_color = range_rgb["green"]
                elif color == 3:
                    detect_color = 'blue'
                    draw_color = range_rgb["blue"]
                else:
                    detect_color = 'None'
                    draw_color = range_rgb["black"]
            cv2.putText(frame, "Color: " + detect_color, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                        draw_color, 2)
        return frame, world_x, world_y

    def reset(self) -> None:
        """ Reset all defaults, no parameters, returns nothing"""
        self.count = 0
        self.get_roi = False
        self.detect_color = 'None'
        self.target_color = ()

    if __name__ == "__main__":
        camera = Camera.Camera()
        perception = Perception(camera)
        while True:
            frame = perception.get_frame()
            if frame is not None:
                frame_read = perception.read_image(frame)
                frame_lab = perception.convert2LAB()
                frame_final, world_x_cor, world_y_cor = perception.detect_object(frame_lab, frame)
                cv2.imshow("Frame", frame_final)
                key = cv2.waitKey(1)
                if key == 27:
                    break
        camera.camera_close()
        cv2.destroyAllWindows()