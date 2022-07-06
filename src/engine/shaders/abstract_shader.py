from src.engine.typing import rect_style, surfarray_style

from typing import Any


class AbstractShader:
    WINDOW_SIZE = (400, 300)
    SHADER_MAX_SIZE = 100

    @classmethod
    def compute(cls,
                input_array: surfarray_style,
                values: Any,
                rect: rect_style = None,
                output_array: surfarray_style = None) -> None:
        """
        Args:
            input_array: A numpy array or a pygame surface that contain information to shade.
            values: A argument that may change from one shader to another. No defined type.
            rect: A rect style argument that describe the zone to shade. Default to the whole array.
            output_array: A numpy array or a pygame surface that will receive the shaded array.
                Default to the input_array.
        """

        return
