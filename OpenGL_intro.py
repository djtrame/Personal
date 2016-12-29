import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

#12 edges to a cube
#edges between nodes/vertices
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)

def Draw_Cube():
    #delimit vertices that define your primitives
    glBegin(GL_LINES)

    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])

    glEnd()

def main():
    pygame.init()

    display = (800,600)

    #double buffer - we see 1 image, in the background there's another image.  handles monitor refresh rates
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #field of view, aspect ratio, clipping closest, clipping distance
    gluPerspective(45.0, (display[0]/display[1]), 0.1, 50)

    #multiplies the current matrix by a translated matrix
    #take 5 steps back from the cube
    #where are we in relation to the cube
    glTranslatef(0.0,0.0,-5.0)

    #angle, x, y, z
    #move 90 degrees and we're on top of the cube
    #glRotatef(90, 5, 0, 0)
    glRotatef(40,20,20,0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #automatically rotate the cube
        #glRotatef(1,1,1,1)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        Draw_Cube()
        #pygame.display.update() threw an error called "Cannot update an OPENGL display"
        pygame.display.flip()
        pygame.time.wait(10)

main()