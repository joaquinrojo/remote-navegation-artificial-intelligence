from pydantic import BaseModel
from typing import List

from process.object_processing.object_models.model_detect import (object_detection_model, object_detection_classes)


class ObjectModels(BaseModel):
    # ball model
    object_model: str = object_detection_model
    object_classes: List[str] = object_detection_classes

    # another models


ObjectModelConfig = ObjectModels()