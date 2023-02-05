from typing import Any, Dict

import cv2
import numpy as np
import tensorflow as tf

from peekingduck.pipeline.nodes.abstract_node import AbstractNode

IMG_HEIGHT = 128
IMG_WIDTH = 128

class Node(AbstractNode):

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.baseline_model = tf.keras.models.load_model("models/baseline.h5")
        self.class_label_map = ['BLANK','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore

        """Reads the image input and returns the predicted class label and
        confidence score.

        Args:
                inputs (dict): Dictionary with key "img".

        Returns:
                outputs (dict): Dictionary with keys "pred_label" and "pred_score".
        """

        img = cv2.cvtColor(inputs["img"], cv2.COLOR_BGR2RGBA)
        img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
        img = np.expand_dims(img, axis=0)
        predictions = self.baseline_model.predict(img)
        score = tf.nn.softmax(predictions[0])

        return {
                "pred_label": self.class_label_map[np.argmax(score)],
                "pred_score": 100.0 * np.max(score),
        }
