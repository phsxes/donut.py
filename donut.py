import math as m
import numpy as np
import sys
import os

theta_spacing = 0.07
phi_spacing   = 0.02
screen_width = 40
screen_height = 40


R1 = 1
R2 = 2
K2 = 5
# Calculate K1 based on screen size: the maximum x-distance occurs
# roughly at the edge of the torus, which is at x=R1+R2, z=0.  we
# want that to be displaced 3/8ths of the width of the screen, which
# is 3/4th of the way from the center to the side of the screen.
# screen_width*3/8 = K1*(R1+R2)/(K2+0)
# screen_width*K2*3/(8*(R1+R2)) = K1
K1 = screen_width*K2*3/(8*(R1+R2))


def render_frame(A, B):
    # precompute sines and cosines of A and B
    cosA = m.cos(A)
    sinA = m.sin(A)
    cosB = m.cos(B)
    sinB = m.sin(B)

    output = np.empty([screen_width, screen_height], dtype=str)
    output.fill(' ')
    zbuffer = np.empty([screen_width, screen_height])
    zbuffer.fill(0)

    # theta goes around the cross-sectional circle of a torus
    for theta in np.arange(0, 2*m.pi, theta_spacing):
        # precompute sines and cosines of theta
        costheta = m.cos(theta)
        sintheta = m.sin(theta)

        # phi goes around the center of revolution of a torus
        for phi in np.arange(0, 2*m.pi, phi_spacing):
            # precompute sines and cosines of phi
            cosphi = m.cos(phi)
            sinphi = m.sin(phi)
    
            # the x,y coordinate of the circle, before revolving (factored
            # out of the above equations)
            circlex = R2 + R1*costheta
            circley = R1*sintheta

            # final 3D (x,y,z) coordinate after rotations, directly from
            # our math above
            x = circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB
            y = circlex*(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB
            z = K2 + cosA*circlex*sinphi + circley*sinA
            ooz = 1/z;  # "one over z"
      
            # x and y projection.  note that y is negated here, because y
            # goes up in 3D space but down on 2D displays.
            xp = int(screen_width/2 + K1*ooz*x)
            yp = int(screen_height/2 - K1*ooz*y)
            # calculate luminance.  ugly, but correct.
            L = cosphi*costheta*sinB - cosA*costheta*sinphi - sinA*sintheta + cosB*(cosA*sintheta - costheta*sinA*sinphi)
            # L ranges from -sqrt(2) to +sqrt(2).  If it's < 0, the surface
            # is pointing away from us, so we won't bother trying to plot it.
            if (L > 0): 
                # test against the z-buffer.  larger 1/z means the pixel is
                # closer to the viewer than what's already plotted.

                if ooz > zbuffer[xp, yp]:
                    zbuffer[xp, yp] = ooz
                    luminance_index = int(L*8)
                    # luminance_index is now in the range 0..11 (8*sqrt(2) = 11.3)
                    # now we lookup the character corresponding to the
                    # luminance and plot it in our output:
                    output[xp, yp] = ".,-~:;=!*#$@"[luminance_index]

    # now, dump output[] to the screen.
    # bring cursor to "home" location, in just about any currently-used
    # terminal emulation mode
    os.system('clear')
    sys.stdout.write('\x1b[H')
    for j in range(0, screen_height):
        for i in range(0, screen_width):
            sys.stdout.write(output[i,j])
        sys.stdout.write('\n')

A = 1
B = 1
while 1:
    A += 0.07
    B += 0.03
    render_frame(A, B)
