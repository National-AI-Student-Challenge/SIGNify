from typing import Any, Dict

import cv2
import numpy as np
import tensorflow as tf

from peekingduck.pipeline.nodes.abstract_node import AbstractNode

IMG_HEIGHT = 224
IMG_WIDTH = 224

class Node(AbstractNode):

    def __init__(self, enabled, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.enabled = enabled
        self.class_label_map = ['A', 'B','_','C', 'D', 'E', 'F', 'G', 'H', 'I','K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

        if self.enabled:
                self.baseline_model = tf.keras.models.load_model("models/base_model.h5")
        

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore

        """Reads the image input and returns the predicted class label and
        confidence score.

        Args:
                inputs (dict): Dictionary with key "img".

        Returns:
                outputs (dict): Dictionary with keys "pred_label" and "pred_score".
        """
        if self.enabled:
                img = cv2.cvtColor(inputs["img"], cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                img = img/255
                cv2.imshow('image',img)

                img = np.expand_dims(img, axis=0)
                scores = self.baseline_model.predict(img)
                print(self.class_label_map[np.argmax(scores)])
                return {
                        "pred_label": self.class_label_map[np.argmax(scores)],
                        "pred_score": 100.0 * np.max(scores),
                }
        
        return {"pred_label": "_",
                "pred_score": 0}
        
