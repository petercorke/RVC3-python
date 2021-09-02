#! /usr/bin/env python3
import vtk
import numpy as np
from vtk.util import numpy_support
import cv2



class Camera_VTK():
    """
    Example class showing how to project a 3D world coordinate onto a 2D image plane using VTK
    """

    def __init__(self, w, h, P, K):
        self.w = w
        self.h = h
        
        self.P = P # position of 3D sphere
        
        self.K = K # Camera matrix
        
        self.f = np.array( [K[0,0], K[1,1]] ) # focal lengths
        self.c = K[:2,2] # principal point
        
        # projection of 3D sphere center onto the image plane
        self.p_im = np.dot(self.K,P.reshape(3,1)).flatten()
        self.p_im /= self.p_im[-1]

        self.init_vtk()
        
    
    def getImage(self):
        """
        Render a sphere using VTK into an image, and plot the projection of that sphere onto the image plane. They should coincide
        """
        # Set basic camera parameters in VTK
        cam = self.renderer.GetActiveCamera()
        near = 0.1
        far = 1000.0
        cam.SetClippingRange(near, far)
        
        # Position is at origin, looking in z direction with y down
        cam.SetPosition(0, 0, 0)
        cam.SetFocalPoint(0, 0, 1)
        cam.SetViewUp(0, -1, 0)
        
        w,h = self.w, self.h
        
        # Set window center for offset principal point
        wcx = -2.0*(self.c[0] - self.w / 2.0) / self.w
        wcy = 2.0*(self.c[1] - self.h / 2.0) / self.h
        cam.SetWindowCenter(wcx, wcy)
        
        # Set vertical view angle as a indirect way of setting the y focal distance
        angle = 180 / np.pi * 2.0 * np.arctan2(self.h / 2.0, self.f[1])
        cam.SetViewAngle(angle)
        
        # Set the image aspect ratio as an indirect way of setting the x focal distance
        m = np.eye(4)
        aspect = self.f[1]/self.f[0]
        m[0,0] = 1.0/aspect
        t = vtk.vtkTransform()
        t.SetMatrix(m.flatten())
        cam.SetUserTransform(t)
        
        # Render the scene into a numpy array for openCV processing
        self.renWin.Render()
        winToIm = vtk.vtkWindowToImageFilter()
        winToIm.SetInput(self.renWin)
        winToIm.Update()
        vtk_image = winToIm.GetOutput()
        width, height, _ = vtk_image.GetDimensions()
        vtk_array = vtk_image.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()
        arr = cv2.flip(numpy_support.vtk_to_numpy(vtk_array).reshape(height, width, components), 0)
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
        
        # Draw a circle at the projected place of the 3D sphere onto the image plane
        cv2.circle(arr,(int(self.p_im[0]),int(self.p_im[1])),5,(0,0,255),1)
                
        return arr
        
        

    def init_vtk(self):
        """
        Initialize VTK actors and rendering pipeline
        """
        self.shpereSource = vtk.vtkSphereSource()
        self.shpereSource.SetCenter(self.P[0],self.P[1],self.P[2])
        self.shpereSource.SetRadius(1.0)
        self.shperemapper = vtk.vtkPolyDataMapper()
        self.shperemapper.SetInputConnection(self.shpereSource.GetOutputPort())
        self.shpereactor = vtk.vtkActor()
        self.shpereactor.SetMapper(self.shperemapper)

        self.renderer = vtk.vtkRenderer()
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.SetOffScreenRendering(1)

        self.renderer.AddActor(self.shpereactor)
        self.renderer.SetBackground(0.1, 0.2, 0.4)
        self.renderer.ResetCamera()

        self.renWin.AddRenderer(self.renderer)
        self.renWin.SetSize(self.w, self.h)
        self.renWin.Render()


if __name__ == '__main__':

    fx = 500.0
    fy = 400.0
    cx = 395.0
    cy = 275.0
    w = 760
    h = 570

    K = np.array( [ [fx, 0., cx],
                    [ 0. ,fx, cy],
                    [0.,0.,1.]])

    P = np.array([ 11.14230157 , 11.23046172 , 28.56272345])
    
    test = Camera_VTK(w,h,P,K)
    arr = test.getImage()
    
    cv2.imshow("test", arr)
    cv2.waitKey(0)