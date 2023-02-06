from typing import Any, Dict

import cv2
import numpy as np
import tensorflow as tf

from peekingduck.pipeline.nodes.abstract_node import AbstractNode

IMG_HEIGHT = 28
IMG_WIDTH = 28

class Node(AbstractNode):

    def __init__(self, enabled, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.enabled = enabled
        self.class_label_map = ['A', 'B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

        if self.enabled:
                self.baseline_model = tf.keras.models.load_model("models/model.h5")
        

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore

        """Reads the image input and returns the predicted class label and
        confidence score.

        Args:
                inputs (dict): Dictionary with key "img".

        Returns:
                outputs (dict): Dictionary with keys "pred_label" and "pred_score".
        """
        if self.enabled:
                img = cv2.cvtColor(inputs["img"], cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                img = cv2.flip(img, 1)
                cv2.imshow('image', img)


                img = np.expand_dims(img, axis=0)
                scores = self.baseline_model.predict(img)
                print(scores)

                return {
                        "pred_label": self.class_label_map[np.argmax(scores)],
                        "pred_score": 100.0 * np.max(scores),
                }
        
        return {"pred_label": "_",
                "pred_score": 0}
        
