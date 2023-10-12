import math


import numpy as np
import cv2
from  cv2 import aruco

import Ogre
import Ogre.Bites
import Ogre.RTShader


import tkinter as tk
from tkinter import ttk

#import tk_tools
import time

import os

            
    
def set_camera_intrinsics(cam, K, imsize):
    cam.setAspectRatio(imsize[0]/imsize[1])

    zNear = cam.getNearClipDistance()
    top = zNear * K[1, 2] / K[1, 1]
    left = -zNear * K[0, 2] / K[0, 0]
    right = zNear * (imsize[0] - K[0, 2]) / K[0, 0]
    bottom = -zNear * (imsize[1] - K[1, 2]) / K[1, 1]

    cam.setFrustumExtents(left, right, top, bottom)

    fovy = math.atan2(K[1, 2], K[1, 1]) + math.atan2(imsize[1] - K[1, 2], K[1, 1])
    cam.setFOVy(fovy)

def create_image_background(scn_mgr):
    tex = Ogre.TextureManager.getSingleton().create("bgtex", Ogre.RGN_DEFAULT, True)
    tex.setNumMipmaps(0)

    mat = Ogre.MaterialManager.getSingleton().create("bgmat", Ogre.RGN_DEFAULT)
    mat.getTechnique(0).getPass(0).createTextureUnitState().setTexture(tex)
    mat.getTechnique(0).getPass(0).setDepthWriteEnabled(False)
    mat.getTechnique(0).getPass(0).setLightingEnabled(False)

    rect = scn_mgr.createScreenSpaceRect(True)
    rect.setMaterial(mat)
    rect.setRenderQueueGroup(Ogre.RENDER_QUEUE_BACKGROUND)
    scn_mgr.getRootSceneNode().attachObject(rect)

    return tex

def findArucoMarkers(img, markerSize = 6, totalMarkers=250, draw=True):                            
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    #key = getattr(cv2, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    #key = getattr(cv2, cv2.aruco.DICT_4X4_50)
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    corners, ids_ = cv2.aruco.detectMarkers(img, arucoDict)[:2]
    #print("cosas",bboxs)
    #print("tras cosas",corners)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
    return [bboxs, ids]


def main(ctx):
    ## random calibration data. your mileage may vary
    imsize = (1280, 720)
    K = cv2.getDefaultNewCameraMatrix(np.diag([800, 800, 1]), imsize, True)

    ## setup Ogre for AR
    scn_mgr = ctx.getRoot().createSceneManager()
    Ogre.RTShader.ShaderGenerator.getSingleton().addSceneManager(scn_mgr)

    cam = scn_mgr.createCamera("camera")
    cam.setNearClipDistance(5)
    ctx.getRenderWindow().addViewport(cam)

    camnode = scn_mgr.getRootSceneNode().createChildSceneNode()
    # convert OpenCV to OGRE coordinate system
    camnode.rotate((1, 0, 0), math.pi)
    camnode.attachObject(cam)

    set_camera_intrinsics(cam, K, imsize)
    bgtex = create_image_background(scn_mgr)

    ## setup 3D scene
    scn_mgr.setAmbientLight((.1, .1, .1))
    scn_mgr.getRootSceneNode().createChildSceneNode().attachObject(scn_mgr.createLight())


    marker_node = scn_mgr.getRootSceneNode().createChildSceneNode("n1")
    marker_node_2 = scn_mgr.getRootSceneNode().createChildSceneNode("n2")
    
    #Figura 1
    cubo = scn_mgr.createEntity("insRotor.mesh")
    #si = scn_mgr.createEntity("Sword.mesh")
    mesh_node = marker_node.createChildSceneNode()
    mesh_node.attachObject(cubo)
    #mesh_node.attachObject(si)
    mesh_node.scale(2,2,2)

    mesh_node.rotate((1, 0, 0), math.pi/2)
    mesh_node.translate((0, 0, 5))
    mesh_node.setVisible(False)

    #Figura 2
    ogro = scn_mgr.createEntity("TapaDel.mesh")
    mesh_node_2 = marker_node_2.createChildSceneNode()    
    mesh_node_2.attachObject(ogro)
    mesh_node_2.scale(3,3,3)

    mesh_node_2.rotate((1, 0, 0), math.pi/2)
    mesh_node_2.translate((0, 0, 5))
    mesh_node_2.setVisible(False)

    
    ## video capture

    cap = cv2.VideoCapture(0, apiPreference=cv2.CAP_ANY, params=[
    cv2.CAP_PROP_FRAME_WIDTH, imsize[0],
    cv2.CAP_PROP_FRAME_HEIGHT, imsize[1]])

    #cap = cv2.VideoCapture(2, apiPreference=cv2.CAP_ANY, params=[
    #cv2.CAP_PROP_FRAME_WIDTH, 800,
    #cv2.CAP_PROP_FRAME_HEIGHT, 600])

    #cap = cv2.VideoCapture(2)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, imsize[0])
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, imsize[1])

    ## aruco
    #adict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    #cv2.imshow("marker", cv2.aruco.drawMarker(adict, 0, 400))
    #cv2.imwrite('Grises.png',cv2.aruco.drawMarker(adict, 0, 400))
    
    rvec, tvec = None, None
    contador = 0
    contador_2 = 0
    vf11, vf12 = 0, 0
    vf21, vf22 = 0, 0
    vf31, vf32 = 0, 0
    vf41, vf42 = 0, 0
    lastKey = cv2.waitKey(1)

    id_sensor_0 = 0
    id_sensor_1 = 1
    id_sensor_2 = 2
    id_sensor_3 = 3
    id_sensor_4 = 4
    id_sensor_5 = 5
    
    id_vista_cal = 6
    id_vista_correa1 = 11
    id_vista_giro_1 = 8
    id_vista_giro_2 = 9
    id_vista_correa2 = 12


    vf11 = 0
    vf12 = 0
    vf21 = 0
    vf22 = 0
    vf31 = 0
    vf32 = 0
    vf41 = 0
    vf42 = 0
    vf11_2 = 0
    vf12_2 = 0
    vf21_2 = 0
    vf22_2 = 0
    vf31_2 = 0
    vf32_2 = 0
    vf41_2 = 0
    vf42_2 = 0
    seleccion = [0,0,0]
    while lastKey != 27:
        id_0 = False
        #lastKey = cv2.waitKey(1)
        cont, img = cap.read()
        if not cont: break

        arucofound = findArucoMarkers(img,4,50, False)
        seleccion = [0,0,1]
        if len(arucofound[0])!=0:
            id_detect_s0 = []
            x_detect_s0 = []
            y_detect_s0 = []

            id_detect_s1 = []
            x_detect_s1 = []
            y_detect_s1 = []

            id_detect_s2 = []
            x_detect_s2 = []
            y_detect_s2 = []

            id_detect_s3 = []
            x_detect_s3 = []
            y_detect_s3 = []

            id_detect_s4 = []
            x_detect_s4 = []
            y_detect_s4 = []

            id_detect_s5 = []
            x_detect_s5 = []
            y_detect_s5 = []


            conta = len(arucofound[0])
            #print("conta", conta)
            

            for i_c in range(conta):
                bbox = arucofound[0][i_c]
                id = arucofound[1][i_c]

                #print("bbox",bbox)
                print("id", id)
                v11, v12 = (bbox[0][0][0],bbox[0][0][1] )
                v21, v22 = (bbox[0][1][0],bbox[0][1][1] )
                v31, v32 = (bbox[0][2][0],bbox[0][2][1] )
                v41, v42 = (bbox[0][3][0],bbox[0][3][1] )

                if id[0] == id_sensor_0 or id[0] == id_vista_correa1:
                    id_detect_s0.append(id[0])
                    x_detect_s0.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s0.append((v12 + v22 + v32 + v42)/4)
                if id[0] == id_sensor_1 or id[0] == id_vista_correa1:
                    id_detect_s1.append(id[0])
                    x_detect_s1.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s1.append((v12 + v22 + v32 + v42)/4)
                if id[0] == id_sensor_2 or id[0] == id_vista_correa1:
                    id_detect_s2.append(id[0])
                    x_detect_s2.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s2.append((v12 + v22 + v32 + v42)/4)
                if id[0] == id_sensor_3 or id[0] == id_vista_correa2:
                    id_detect_s3.append(id[0])
                    x_detect_s3.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s3.append((v12 + v22 + v32 + v42)/4)
                if id[0] == id_sensor_4 or id[0] == id_vista_correa2:
                    id_detect_s4.append(id[0])
                    x_detect_s4.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s4.append((v12 + v22 + v32 + v42)/4)
                if id[0] == id_sensor_5 or id[0] == id_vista_correa2:
                    id_detect_s5.append(id[0])
                    x_detect_s5.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s5.append((v12 + v22 + v32 + v42)/4)

                if id[0] == id_vista_correa1:

                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()

                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node.setPosition(tvec)
                    mesh_node.setVisible(True)

                if id[0] == id_vista_correa2:
                   
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()

                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    marker_node_2.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node_2.setPosition(tvec)
                    #marker_node_2.absDotProducto(tvec)
                    mesh_node_2.setVisible(True)


                #print("id:",id_detect_1[-1],"x:",x_detect_1[-1],"y:",y_detect_1[-1])
                if seleccion in error:
                    pass
                    #print("Error en proceso o sensores")
                if seleccion in bloque:
                    if id == 5:
                        pass
                        #Poner imagen
                        #img = arucoAug(bbox, id, img, imgAug1)
                    if id == 9:
                        pass
                        #Poner imagen
                        #img = arucoAug(bbox, id, img, imgAug2)
                if seleccion in carcul:
                    if id == 5:
                        pass
                        #Poner imagen
                        #img = arucoAug(bbox, id, img, imgAug3)
                    if id == 9:
                        pass
                        #Poner imagen
                        #img = arucoAug(bbox, id, img, imgAug4)
            if len(id_detect_s0) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s0[0]- x_detect_s0[1])**2 + (y_detect_s0[0]- y_detect_s0[1])**2)**0.5
                print("distancia0:",distancia)
                file.write("distancia0:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 120:
                    pass
                    '''var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor0")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
                else:
                    pass
                    '''var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor0")
                    #var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.c1")
                    
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
            if len(id_detect_s1) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s1[0]- x_detect_s1[1])**2 + (y_detect_s1[0]- y_detect_s1[1])**2)**0.5
                print("distancia1:",distancia)
                file.write("distancia1:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 120:
                    pass
                    '''                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor1")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
                else:
                    pass
                    '''var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor1")
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
            if len(id_detect_s2) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s2[0]- x_detect_s2[1])**2 + (y_detect_s2[0]- y_detect_s2[1])**2)**0.5
                print("distancia2:",distancia)
                file.write("distancia2:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 120:
                    pass
                    '''var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor2")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
                else:
                    pass
                    '''var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor2")
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
            if len(id_detect_s3) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s3[0]- x_detect_s3[1])**2 + (y_detect_s3[0]- y_detect_s3[1])**2)**0.5
                print("distancia3:",distancia)
                file.write("distancia3:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 120:
                    pass
                    '''var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor3")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
                else:
                    pass
                    '''var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor3")
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
            if len(id_detect_s4) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s3[0]- x_detect_s3[1])**2 + (y_detect_s3[0]- y_detect_s3[1])**2)**0.5
                print("distancia4:",distancia)
                file.write("distancia4:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 120:
                    pass
                    '''var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor4")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
                else:
                    pass
                    '''var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor4")
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    var1.set_value(dv1)'''
            if len(id_detect_s5) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s3[0]- x_detect_s3[1])**2 + (y_detect_s3[0]- y_detect_s3[1])**2)**0.5
                print("distancia5:",distancia)
                file.write("distancia5:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 120:
                    pass
                    #var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor5")
                    #dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    #var1.set_value(dv1)
                else:
                    pass
                    #var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor5")
                    #dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    #var1.set_value(dv1)
            #update_gauge()
        im = Ogre.Image(Ogre.PF_BYTE_BGR, img.shape[1], img.shape[0], 1, img, False)
        if bgtex.getBuffer():
            bgtex.getBuffer().blitFromMemory(im.getPixelBox())
        else:
            bgtex.loadImage(im)

        #corners, ids = cv2.aruco.detectMarkers(img, adict)[:2]
        #print( "esquinas ",corners)
        #print( "ids ",ids)
        #print(corners)
        #if id_0:
            #print( "ids ",ids)
            #print( "esquinas ",corners)
        #    time.sleep(1)
            
        lastKey = cv2.waitKey(1)
        ctx.getRoot().renderOneFrame()
        #update_gauge()
        #time.sleep(0.1)

#global corners
bloque = [[0,0,0],[0,1,0],[1,2,2],[1,3,2]]
error = [[0,0,1],[1,0,0],[1,0,1],[1,1,1]]
carcul = [[1,1,0],[1,2,0],[1,2,1],[2,3,2],[2,4,2],[2,4,3]]

file = open("./distancias.txt", "w")
file.close()
ctx = Ogre.Bites.ApplicationContext()


ctx.initApp()
main(ctx)
ctx.closeApp()
