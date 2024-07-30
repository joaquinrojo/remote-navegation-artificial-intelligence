from typing import List
import numpy as np
from ultralytics import YOLO

from process.object_processing.object_processing_tools import ObjectTools
from process.object_processing.models import ObjectModelConfig

class FrameProcessing:
    def __init__(self):
        self.execute = ObjectTools()

        # ball
        self.object_detection_model: YOLO = YOLO(ObjectModelConfig.object_model)
        self.object_detection_classes: List[str] = ObjectModelConfig.object_classes

    def process(self, image: np.ndarray, classToDetect: str) :
        # Step 1: ball detect

        object_bbox, object_cls, object_conf = self.execute.frame_model_inference(image, self.object_detection_model,
                                                                            self.object_detection_classes,classToDetect)
        # [axis x, axis z]
        error_vector = [0, 0]
        if len(object_bbox) != 0:
            if object_cls == classToDetect:
                self.execute.draw_rect(image, object_bbox, (255, 0, 0), 2)
                # x axis
                object_xc, object_yc = self.execute.extract_center_object(image, object_bbox, (0, 0, 255), viz=True)
                frame_xc, frame_yc = self.execute.extract_center_frame(image)
                error_vector = self.execute.error_calculated_x_axis(object_xc, frame_xc, error_vector)

                # z axis
                object_area = self.execute.calculate_area(object_bbox)
                error_vector = self.execute.error_calculated_z_axis(object_area, error_vector)


        #print(f'vector send: {error_vector}')
        return object_cls, error_vector
