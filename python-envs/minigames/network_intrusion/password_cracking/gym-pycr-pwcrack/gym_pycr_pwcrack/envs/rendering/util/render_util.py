"""
Some OpenGL utility functions for drawing various shapes using the OpenGL primitive API
"""

import pyglet.gl as gl
import pyglet
import math

def create_circle_fill(x, y, radius, batch, group, color):
    """
    Creates a circle that can be rendered in OpenGL batch mode

    :param x: the x-coordinate of the circle center
    :param y: the y-coordinate of the circle center
    :param radius: the radius of the circle
    :param batch: the batch to render the circle in
    :param group: the group (e.g foreground or background)
    :param color: the color to fill the circle with
    :return: None
    """
    circle, indices = create_indexed_vertices(x, y, radius)
    vertex_count = len(circle) // 2
    return batch.add_indexed(vertex_count, pyglet.gl.GL_TRIANGLES, group,
                      indices,
                      ('v2f', circle),
                      ('c3B', color * vertex_count))


def create_circle(x, y, radius, batch, group, color):
    """
    Creates a circle that can be rendered in OpenGL batch mode

    :param x: the x-coordinate of the circle center
    :param y: the y-coordinate of the circle center
    :param radius: the radius of the circle
    :param batch: the batch to render the circle in
    :param group: the group (e.g foreground or background)
    :param color: the color to fill the circle with
    :return: None
    """
    circle, indices = create_indexed_vertices(x, y, radius)
    vertex_count = len(circle) // 2
    return batch.add_indexed(vertex_count, pyglet.gl.GL_TRIANGLES, group,
                      indices, ('v2f', circle), ('c3B', color * vertex_count))


def create_circle_no_batch(x, y, radius, color):
    circle, indices = create_indexed_vertices(x, y, radius)
    vertex_count = len(circle) // 2
    r = pyglet.graphics.vertex_list_indexed(vertex_count,
                             indices, ('v2f', circle), ('c3B', color * vertex_count))
    # return batch.add_indexed(vertex_count, pyglet.gl.GL_TRIANGLES, group,
    #                          indices, ('v2f', circle), ('c3B', color * vertex_count))


def create_indexed_vertices(x, y, radius, sides=24):
    """
    Utility function  that generates a vertex list for rendering a circle with openGL

    :param x: the x coordinate of the circle center
    :param y: the y coordinate of the circle center
    :param radius: the radius of the circle
    :param sides: the number of sides for the circle
    :return: the vertex list and their indices
    """
    vertices = [x, y]
    for side in range(sides):
        angle = side * 2.0 * math.pi / sides
        vertices.append(x + math.cos(angle) * radius)
        vertices.append(y + math.sin(angle) * radius)
    # Add a degenerated vertex
    vertices.append(x + math.cos(0) * radius)
    vertices.append(y + math.sin(0) * radius)

    indices = []
    for side in range(1, sides+1):
        indices.append(0)
        indices.append(side)
        indices.append(side + 1)
    return vertices, indices


def batch_line(x1, y1, x2, y2, color, batch, group, line_width):
    """
    Creates a line that can be rendered in OpenGL batch mode

    :param x1: the starting x coordinate of the line
    :param y1: the starting y coordinate of the line
    :param x2: the ending x coordinate of the line
    :param y2: the ending y coordinate of the line
    :param color: the color of the line
    :param batch: the batch to render the line in
    :param group: the group (e.g foreground or background)
    :param line_width: the width of the line
    :return: vertexlist of the created line
    """
    color_list = list(color) + list(color)
    pyglet.gl.glLineWidth(line_width)
    return batch.add(2, pyglet.gl.GL_LINES, group,
        ('v2f', (x1, y1, x2, y2)),
        ('c3B', tuple(color_list))
    )


def batch_label(text, x, y, font_size, color, batch, group, font_name='Times New Roman', multiline=False,
                width= None, bold=False):
    """
    Creates a text-label that can be rendered in OpenGL batch mode

    :param text: the text of the label
    :param bold: boolean flag whether to render the text as bold or not
    :param x: the x coordinate
    :param y: the y coordinate
    :param font_size: the font size
    :param color: the color of the label
    :param batch: the batch to render the label in
    :param group: the batch group (e.g. foreground or background)
    :param font_name: the font type
    :param multiline: whether it is a multiline label or not
    :param width: width of the layout
    :return: a reference to the label object (in case the label has to be updated later on)
    """
    label = pyglet.text.Label(text,
                          font_name=font_name,
                          font_size=font_size,
                          x=x, y=y,
                          anchor_x='center', anchor_y='center',
                          color=color,
                          batch=batch,
                          group=group,
                          multiline=multiline,
                          width=width,
                          bold = bold)
    return label


def batch_rect_fill(x, y, width, height, color, batch, group):
    """
    Method for rendering a filled rectangle in batch mode

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :param color: RGB color to fill the rectangle with [R,G,B] scaled between [0,1]
    :param batch: the batch to render the rectangle with
    :param group: the batch group (e.g. foreground or background)
    :return: None
    """
    color_list = list(color) + list(color) + list(color) + list(color)
    # Renders a "quad" (i.e. a shape with four sides, such as a rectangle).
    # 4 is the number of vertices (the four corners of the Quad)
    # "v2i" is the vertex format, which is 2 integers
    # the tuple list specifies four vertices (8 numbers)
    # "c3B" is the format of the color, which means RGB format 0-255
    # the color list is a list of 4*3 with a RGB color for each side of the quad
    return batch.add(4, pyglet.gl.GL_QUADS, group, ('v2i', (x, y, x+width, y, x+width, y+height, x, y+height)),
              ('c3B', tuple(color_list)))


def batch_rect_border(x, y, width, height, color, batch, group):
    """
    Method for rendering a the border of a rectangle in batch mode

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :param color: RGB color to fill the rectangle with [R,G,B] scaled between [0,1]
    :param batch: the batch to render the rectangle with
    :param group: the batch group (e.g. foreground or background)
    :return: None
    """

    color_list = list(color) + list(color) + list(color) + list(color)
    # Renders the lines of a rectangle
    # 4 is the number of vertices (the four corners of the rectangle)
    # "v2i" is the vertex format, which is 2 integers
    # the tuple list specifies four vertices (8 numbers)
    # "c3B" is the format of the color, which means RGB format 0-255
    # the color list is a list of 4*3 with a RGB color for each side of the quad

    # Draw vertical lines (x,y)-->(x,y+height) and (x+width, y)-->(x+width, y+height)
    batch.add(4, pyglet.gl.GL_LINES, group,
        ('v2f', (x, y, x, y+height, x+width, y+height, x+width, y)),
        ('c3B', tuple(color_list)))

    # Draw Horizontal lines (x,y)-->(x+width,y) and (x, y+height)-->(x+width, y+height)
    batch.add(4, pyglet.gl.GL_LINES, group,
              ('v2i', (x, y, x+width, y, x, y + height, x + width, y+height)),
              ('c3B', tuple(color_list)))


def draw_and_fill_rect(x, y, width, height, color):
    """
    Draws and fills a rectangle

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :param color: RGB color to fill the rectangle with [R,G,B] scaled between [0,1]
    :return: None
    """
    __rect(x, y, width, height, color, fill=True)


def draw_rect_border(x, y, width, height, color):
    """
    Draws a rectangle with a border

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :param color: RGB color of the border [R,G,B] scaled between [0,1]
    :return: None
    """
    __rect(x,y,width,height,color)


def __rect(x, y, width, height, color, fill=False):
    """
    Draws a rectangle

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :param color: RGB color of the rectangle [R,G,B] scaled between [0,1]
    :param fill: whether to fill the rectangle or just stroke it
    :return: None
    """
    # Set the color in the OpenGL Context (State)
    gl.glColor3f(color[0], color[1], color[2])
    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
    # Configure rectangle (fill or not)
    if fill:
        # Delimits the vertices of a primitive or group of primitives
        gl.glBegin(gl.GL_POLYGON)

    else:
        # Delimits the vertices of a primitive or group of primitives
        gl.glBegin(gl.GL_LINES)

    # Draw the vertices of the rectangle
    __rect_vertices(x, y, width, height)
    # Delimits the vertices of a primitive or group of primitives
    gl.glEnd()


def __rect_vertices(x, y, width, height):
    """
    Uses the OpenGL API to create vertices to form a rectangle of a primitive

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :return: None
    """
    gl.glVertex2f(x, y)  # coordinate A
    gl.glVertex2f(x, y + height)  # coordinate B and line AB
    gl.glVertex2f(x, y + height)  # coordinate B
    gl.glVertex2f(x + width, y + height)  # coordinate C and line BC
    gl.glVertex2f(x + width, y + height)  # coordinate C
    gl.glVertex2f(x + width, y)  # coordinate D and line CD
    gl.glVertex2f(x + width, y)  # coordinate D
    gl.glVertex2f(x, y)  # coordinate A and line DA