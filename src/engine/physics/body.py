from src.engine.physics.utils import fix_vec2d_polygon

import pymunk
import pygame

from math import cos, sin, radians
from pymunk.autogeometry import march_soft, convex_decomposition
from typing import Union, Tuple


class Body(pymunk.Body):
    __slots__ = ("shapes_attributes", "real_shapes")
    TOLERANCE = 5
    BASE_DENSITY = 50
    BASE_ELASTICITY = 0.2
    BASE_FRICTION = 0.2

    def __init__(self,
                 position: tuple[float, float] = (0, 0)) -> None:
        """
        A very, very smart class that is used to do physics.
        All credit goes to the creators of chipmunk and pymunk.

        Args:
            position: Initial body position
        """
        super(Body, self).__init__()
        self.position = position

        self.real_shapes = set()
        self.shapes_attributes = {"density": self.BASE_DENSITY,
                                  "elasticity": self.BASE_ELASTICITY,
                                  "friction": self.BASE_FRICTION}

    def shape_poly_from_surface(self,
                                surface: pygame.Surface,
                                radius: float = -1,
                                scale: float = 1,
                                concave: bool = False,
                                tolerance: float = None) -> None:
        """
        This method is used to set this body shape(s) as polygon from a surface effortlessly.

        Args:
            surface: The image.
            radius: A positive radius will make the polygon bigger, a negative radius will make it smaller. Avoid 0.
                Corners will be smoothed so the shape is less prone to be stuck on an edge.
            scale: Between 0 and 1. The smaller this value is, the less detailed the polygon will be.
                (useful if you want better performance)
            concave: Set to True if the shape of the image is concave. Will generate multiple convex polygons.
                Using concave shapes may create lots of polygons, thus altering performances.
            tolerance: The smaller the tolerance is, the more detailed the concave shape will be.
                The higher the tolerance, the better the performance!
        """

        size = surface.get_size()
        bounding_box = pymunk.BB(0, 0, size[0]-1, size[1]-1)
        surface_array = pygame.surfarray.pixels3d(surface)

        def sample_function(_point):
            return surface_array[int(_point[0]), int(_point[1])].max()

        # First decomposition
        polygons = list(march_soft(bounding_box, int(size[0]*scale), int(size[1]*scale), 1, sample_function))

        # Fixing polygons (vec2d -> tuple, centered)
        offset = -size[0]/2, -size[1]/2
        for i in range(len(polygons)):
            polygons[i] = fix_vec2d_polygon(polygons[i], offset)

        if concave:
            if tolerance is None:
                tolerance = self.TOLERANCE

            fixed_polygons = []
            for polygon in polygons:
                decomposed_shape = convex_decomposition(polygon, tolerance)
                for sub_polygon in decomposed_shape:
                    fixed_polygons.append(fix_vec2d_polygon(sub_polygon))
            polygons = fixed_polygons

        for polygon in polygons:
            new_shape = pymunk.Poly(body=self, vertices=polygon, radius=radius)
            self.real_shapes.add(new_shape)

    def shape_rect(self,
                   rect: Union[pygame.Rect, Tuple[float, float, float, float], Tuple[float, float]],
                   angle: float = 0,
                   radius: float = -1) -> None:
        """
        This method is used to set this body shape as a rect.

        Args:
            rect: Either a pygame rect style to specify position and size, either a tuple specifying only size.
            angle: The angle of the shape around (0, 0) in degrees (clockwise)
            radius: A positive radius will make the polygon bigger, a negative radius will make it smaller. Avoid 0.
                Corners will be smoothed so the shape is less prone to be stuck on an edge.
        """

        # If rect is pygame rect: convert to tuple
        if isinstance(rect, pygame.Rect):
            rect = tuple(rect)

        # If only the size is given: create offset rect centered around 0
        if len(rect) == 2:
            off_x, off_y = -rect[0]/2, -rect[1]/2
            rect = (off_x, off_y, rect[0], rect[1])

        # Creating vertices
        x_min = rect[0]
        y_min = rect[1]
        x_max = rect[0]+rect[2]
        y_max = rect[1]+rect[3]
        vertices = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max), (x_min, y_min)]

        # Applying rotation
        cosa, sina = cos(radians(-angle)), sin(radians(-angle))
        vertices = [(vx*cosa-vy*sina, vx*sina+vy*cosa) for vx, vy in vertices]

        new_shape = pymunk.Poly(body=self, vertices=vertices, radius=radius)
        self.real_shapes.add(new_shape)

    def shape_circle(self,
                     radius: float,
                     offset: tuple[float, float] = (0, 0)) -> None:
        """
        This method is used to set this body shape as a circle.

        Args:
            radius: The radius of the circle.
            offset: The center of the circle, default to (0, 0).
        """

        new_shape = pymunk.Circle(body=self, radius=radius, offset=offset)
        self.real_shapes.add(new_shape)

    def set_shapes_attributes(self,
                              density: float = None,
                              elasticity: float = None,
                              friction: float = None,
                              **kwargs) -> None:
        """
        Method used to set shapes properties.

        Args:
            density: How dense the body should be.
            elasticity: How bouncy the body should be.
            friction: How frictional the body should be.
            kwargs: Can define collision types, sensor, ... refer to pymunk doc for more info.
        """

        if density:
            kwargs["density"] = density

        if elasticity:
            kwargs["elasticity"] = elasticity

        if friction:
            kwargs["friction"] = friction

        for key in kwargs:
            self.shapes_attributes[key] = kwargs[key]

        for shape in self._shapes:
            for attribute in self.shapes_attributes:
                setattr(shape, attribute, self.shapes_attributes[attribute])

    def add_to_space(self,
                     new_space: pymunk.Space) -> None:
        """
        Add the current body and associated shapes to space. Can't belong to only one space at once.

        Args:
            new_space: The new space where the body should be.
        """

        if new_space is None:
            raise Exception("Fuck off")

        # self.remove_from_space()
        new_space.add(self, *self._shapes)

    def remove_from_space(self) -> None:
        """Remove the current body and associated shapes from space."""

        try:
            bool(self._space)

        # ReferenceError is raised if self._space doesn't exist anymore
        except ReferenceError:
            return

        if self._space is not None:
            self._space.remove(self, *self.shapes)

    def __del__(self):
        self.remove_from_space()

    def set_velocity(self, vel: Tuple[int, int]) -> None:
        pass
