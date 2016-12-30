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

#6 faces in a cube.  connect the vertices.
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)

)

def Draw_Cube():

    #draw quads first so the lines appear on top
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glColor3fv((1,0,1))
            glVertex3fv(vertices[vertex])

    glEnd()

    #delimit vertices that define your primitives
    glBegin(GL_LINES)

    for edge in edges:
        for vertex in edge:
            #color the lines of the cube RGB
            glColor3fv((0,1,1))
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
    glRotatef(20,2,0,0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #4 is mouse wheel forward, 5 is reverse
                print(event.button)

                if event.button == 4:
                    glTranslatef(0.0,0.0,1.0)
                elif event.button == 5:
                    glTranslatef(0.0,0.0,-1.0)

        #automatically rotate the cube
        glRotatef(1,3,1,1)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        Draw_Cube()
        #pygame.display.update() threw an error called "Cannot update an OPENGL display"
        pygame.display.flip()
        pygame.time.wait(10)

main()