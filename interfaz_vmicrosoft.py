# La ruta de ogre.mesh es ~/.local/share/Trash/files

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
import opcua
from opcua import ua

import os
import numpy as np

def inicio():
    files = open("./RA-OPC-OGRE/ip_server_opc.txt", "r")
    sw = True
    for file in files:
        client = opcua.Client(file)
        print(file)
        try:
            if client.connect() is None:
                sw = True
                break
        except:
            print("Ha ocurrido un error")
            print("")
            sw = False
    files.close()
    if sw:
        return client
    else:       
        return None
            
def calibracion():
    c_1 = False
    c_2 = False

    var = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcaOFF")
    dv = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
    try:
        var.set_value(dv)
    except:
        print("An exception occurred")

    print("Reseteando")
    time.sleep(1)
    var = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcaOFF")
    dv = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var.set_value(dv)
    except:
        print("An exception occurred")


    var = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcaON")
    dv = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
    try:
        var.set_value(dv)
    except:
        print("An exception occurred")
    time.sleep(1)
    var = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcaON")
    dv = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var.set_value(dv)
    except:
        print("An exception occurred")
    
    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.c1")
    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var1.set_value(dv1)
    except:
        print("An exception occurred")
    var2 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.c2")
    dv2 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var2.set_value(dv2)
    except:
        print("An exception occurred")
    
    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor0")
    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var1.set_value(dv1)
    except:
        print("An exception occurred")

    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor1")
    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var1.set_value(dv1)
    except:
        print("An exception occurred")

    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor2")
    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var1.set_value(dv1)
    except:
        print("An exception occurred")

    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor3")
    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var1.set_value(dv1)
    except:
        print("An exception occurred")

    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor4")
    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var1.set_value(dv1)
    except:
        print("An exception occurred")
    
    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor5")
    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
        var1.set_value(dv1)
    except:
        print("An exception occurred")
    #calibrate = True
    #while calibrate:
    #    calibrate = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.sensor0").get_value()
    
    imsize = (1280, 720)
    #K = cv2.getDefaultNewCameraMatrix(np.diag([800, 800, 1]), imsize, True)

    K = cv2.getDefaultNewCameraMatrix(np.diag([1280, 720, 1]), imsize, True)
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

    marker_node = scn_mgr.getRootSceneNode().createChildSceneNode()
    mesh_node = marker_node.createChildSceneNode()
    mesh_node.attachObject(scn_mgr.createEntity("Sinbad.mesh"))
    #mesh_node.attachObject(scn_mgr.createEntity("Cube.mesh"))
    mesh_node.rotate((1, 0, 0), math.pi/2)
    mesh_node.translate((0, 0, 5))
    mesh_node.setVisible(False)

    ## video capture

    cap = cv2.VideoCapture(0, apiPreference=cv2.CAP_ANY, params=[
    cv2.CAP_PROP_FRAME_WIDTH, imsize[0],
    cv2.CAP_PROP_FRAME_HEIGHT, imsize[1]])

    
    id_sensor_base1 = 13
    id_sensor_correa1 = 11

    id_sensor_base2 = 3
    id_sensor_correa2 = 12

    while  not (c_1 == True and c_2 == True):
        id_0 = False
        cont, img = cap.read()
        if not cont: 
            print("Error de lectura de imagen")
            break

        arucofound = findArucoMarkers(img,4,50, False)
        if len(arucofound[0])!=0:
            id_detect_1 = []
            x_detect_1 = []
            y_detect_1 = []
            id_detect_2 = []
            x_detect_2 = []
            y_detect_2 = []
            conta = len(arucofound[0])
            for i_c in range(conta):
                bbox = arucofound[0][i_c]
                id = arucofound[1][i_c]
                #print("bbox",bbox)
                print("id", id[0])
                v11, v12 = (bbox[0][0][0],bbox[0][0][1] )
                v21, v22 = (bbox[0][1][0],bbox[0][1][1] )
                v31, v32 = (bbox[0][2][0],bbox[0][2][1] )
                v41, v42 = (bbox[0][3][0],bbox[0][3][1] )
                v11_2, v12_2 = v11, v12
                v21_2, v22_2 = v21, v22
                v31_2, v32_2 = v31, v32
                v41_2, v42_2 = v41, v42
                
                if id[0] == id_sensor_base1 or id[0] == id_sensor_correa1:
                    id_detect_1.append(id[0])
                    x_detect_1.append((v11 + v21 + v31 + v41)/4)
                    y_detect_1.append((v12 + v22 + v32 + v42)/4)
                if id[0] == id_sensor_base2 or id[0] == id_sensor_correa2:
                    id_detect_2.append(id[0])
                    x_detect_2.append((v11_2 + v21_2 + v31_2 + v41_2)/4)
                    y_detect_2.append((v12_2 + v22_2 + v32_2 + v42_2)/4)
            if len(id_detect_1) == 2:
                print(id_detect_1)
                print(x_detect_1)
                print(y_detect_1)
                distancia =  ((x_detect_1[0]- x_detect_1[1])**2 + (y_detect_1[0]- y_detect_1[1])**2)**0.5
                print("distancia1:",distancia)
                if distancia <= 61:
                    c_1 = True
                    var = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.c1")
                    dv = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    try:
                        var.set_value(dv)
                    except:
                        print("An exception occurred")
                    

            if len(id_detect_2) == 2:
                print(id_detect_2)
                print(x_detect_2)
                print(y_detect_2)
                distancia =  ((x_detect_2[0]- x_detect_2[1])**2 + (y_detect_2[0]- y_detect_2[1])**2)**0.5
                print("distancia2:",distancia)
                if distancia <= 63:
                    c_2 = True
                    var = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.c2")
                    dv = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    try:
                        var.set_value(dv)
                    except:
                        print("An exception occurred")

        im = Ogre.Image(Ogre.PF_BYTE_BGR, img.shape[1], img.shape[0], 1, img, False)

        if bgtex.getBuffer():
            bgtex.getBuffer().blitFromMemory(im.getPixelBox())
        else:
            bgtex.loadImage(im)

        
        ctx.getRoot().renderOneFrame()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
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
def update_gauge():
    # upd88ate the gauges with the OPC-UA values every 1 second
    print()
    print("s0 ",client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.sensor0").get_value())
    print("s1 ",client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.sensor1").get_value())
    print("s2 ",client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.sensor2").get_value())
    print("s3 ",client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.sensor3").get_value())
    print("s4 ",client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.sensor4").get_value())
    print("s5 ",client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.sensor5").get_value())

def main(ctx):
    ## random calibration data. your mileage may vary
    imsize = (1280, 720)
    #K = cv2.getDefaultNewCameraMatrix(np.diag([800, 800, 1]), imsize, True)
    K = cv2.getDefaultNewCameraMatrix(np.diag([1280, 720, 1]), imsize, True)
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
    marker_node_3 = scn_mgr.getRootSceneNode().createChildSceneNode("n3")
    marker_node_4 = scn_mgr.getRootSceneNode().createChildSceneNode("n4")
    marker_node_5 = scn_mgr.getRootSceneNode().createChildSceneNode("n5")
    marker_node_6 = scn_mgr.getRootSceneNode().createChildSceneNode("n6")
    '''marker_node = scn_mgr.getRootSceneNode().createChildSceneNode()
    mesh_node = marker_node.createChildSceneNode()
    mesh_node.attachObject(scn_mgr.createEntity("Sinbad.mesh"))
    #mesh_node.attachObject(scn_mgr.createEntity("Cube.mesh"))
    mesh_node.rotate((1, 0, 0), math.pi/2)
    mesh_node.translate((0, 0, 5))
    mesh_node.setVisible(False)'''
    #Figura 1
    objeto1 = scn_mgr.createEntity("estator.mesh")
    mesh_node = marker_node.createChildSceneNode()
    mesh_node.attachObject(objeto1)
    mesh_node.scale(2,2,2)

    mesh_node.rotate((1, 0, 0), math.pi/2)
    mesh_node.translate((0, 0, 5))
    mesh_node.setVisible(False)

    #Figura 2
    objeto2 = scn_mgr.createEntity("insRotor.mesh")
    mesh_node_2 = marker_node_2.createChildSceneNode()    
    mesh_node_2.attachObject(objeto2)
    mesh_node_2.scale(2,2,2)

    mesh_node_2.rotate((1, 0, 0), math.pi/2)
    mesh_node_2.translate((0, 0, 5))
    mesh_node_2.setVisible(False)

    #Figura 3
    objeto3 = scn_mgr.createEntity("insTapaTras.mesh")
    mesh_node_3 = marker_node_3.createChildSceneNode()    
    mesh_node_3.attachObject(objeto3)
    mesh_node_3.scale(2,2,2)

    mesh_node_3.rotate((1, 0, 0), math.pi/2)
    mesh_node_3.translate((0, 0, 5))
    mesh_node_3.setVisible(False)
    #Figura 4
    objeto4 = scn_mgr.createEntity("insTapaDel.mesh")
    mesh_node_4 = marker_node_4.createChildSceneNode()    
    mesh_node_4.attachObject(objeto4)
    mesh_node_4.scale(2,2,2)

    mesh_node_4.rotate((1, 0, 0), math.pi/2)
    mesh_node_4.translate((0, 0, 5))
    mesh_node_4.setVisible(False)
    
    #Figura 5
    objeto5 = scn_mgr.createEntity("insPlaca.mesh")
    mesh_node_5 = marker_node_5.createChildSceneNode()    
    mesh_node_5.attachObject(objeto5)
    mesh_node_5.scale(2,2,2)

    mesh_node_5.rotate((1, 0, 0), math.pi/2)
    mesh_node_5.translate((0, 0, 5))
    mesh_node_5.setVisible(False)

    #Figura 6
    objeto6 = scn_mgr.createEntity("insPlaca.mesh")
    mesh_node_6 = marker_node_6.createChildSceneNode()    
    mesh_node_6.attachObject(objeto6)
    mesh_node_6.scale(2,2,2)

    mesh_node_6.rotate((1, 0, 0), math.pi/2)
    mesh_node_6.translate((0, 0, 5))
    mesh_node_6.setVisible(False)

    ## video capture

    cap = cv2.VideoCapture(0, apiPreference=cv2.CAP_ANY, params=[
    cv2.CAP_PROP_FRAME_WIDTH, imsize[0],
    cv2.CAP_PROP_FRAME_HEIGHT, imsize[1]])

      
    rvec, tvec = None, None
    contador = 0
    vf11, vf12 = 0, 0
    vf21, vf22 = 0, 0
    vf31, vf32 = 0, 0
    vf41, vf42 = 0, 0
    lastKey = cv2.waitKey(1)

    id_sensor_0 = 0
    id_sensor_1 = 1
    id_sensor_2 = 2
    id_sensor_3 = 70    #Queda fuera
    id_sensor_4 = 14
    id_sensor_5 = 5

    cont_d = [0,0,0,0,0,0,0,0,0]
    sw_d = [False,False, False, False, False, False, False, False, False]
    

    id_sensor_base1 = 13
    id_sensor_base2 = 3 
    id_vista_correa1 = 11
    id_vista_giro_1 = 8
    id_vista_giro_2_1 = 9
    id_vista_giro_2_2 = 10
    id_vista_correa2 = 12
    id_vista_pinza = 6
    id_Vista_pallet = 7

    time.sleep(3)    
    var = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.c1")
    dv = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
           var.set_value(dv)
    except:
           print("An exception occurred")
    
    var = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.c2")
    dv = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
    try:
           var.set_value(dv)
    except:
           print("An exception occurred")
    
    seleccion = [0,0,0]
    #inicio = None
    #contador_s0 = 0
    #sw_d = [False,False,False,False,False,False,False,False,False]
    cont_cambio_1 = 0
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

            id_detect_s6 = []
            x_detect_s6 = []
            y_detect_s6 = []

            id_detect_s7 = []
            x_detect_s7 = []
            y_detect_s7 = []

            id_detect_s8 = []
            x_detect_s8 = []
            y_detect_s8 = []

            conta = len(arucofound[0])
            #print("conta", conta)
            vf11 = 0
            vf12 = 0
            vf21 = 0
            vf22 = 0
            vf31 = 0
            vf32 = 0
            vf41 = 0
            vf42 = 0
            print("nueva imagen")
            for i_c in range(conta):
                bbox = arucofound[0][i_c]
                id = arucofound[1][i_c]

                #print("bbox",bbox)
                print("id", id[0])
                v11, v12 = (bbox[0][0][0],bbox[0][0][1] )
                v21, v22 = (bbox[0][1][0],bbox[0][1][1] )
                v31, v32 = (bbox[0][2][0],bbox[0][2][1] )
                v41, v42 = (bbox[0][3][0],bbox[0][3][1] )

                if id[0] == id_sensor_0 or id[0] == id_vista_correa1:
                    
                    id_detect_s0.append(id[0])
                    x_detect_s0.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s0.append((v12 + v22 + v32 + v42)/4)
                    print(id_detect_s0)
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
                if id[0] == id_sensor_base1 or id[0] == id_vista_giro_1:
                    id_detect_s6.append(id[0])
                    x_detect_s6.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s6.append((v12 + v22 + v32 + v42)/4)
                if id[0] == id_sensor_base2 or id[0] == id_vista_giro_2_2:
                    id_detect_s7.append(id[0])
                    x_detect_s7.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s7.append((v12 + v22 + v32 + v42)/4)
                if id[0] == id_sensor_2 or id[0] == id_vista_giro_2_1:
                    id_detect_s8.append(id[0])
                    x_detect_s8.append((v11 + v21 + v31 + v41)/4)
                    y_detect_s8.append((v12 + v22 + v32 + v42)/4)         
                #vistas
                if id[0] == id_vista_giro_1 and np.array_equal( np.array(cont_d),np.array([0,0,0,0,0,0,0,0,0])):
                   
                    print("entra pero no funca")
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                        #print("ax",ax,"ang",ang)
                        #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    pos = [tvec[0]+10,tvec[1]+3,tvec[2]]
                    marker_node.setPosition(pos)
                    mesh_node.setVisible(True)
            

                if id[0] == id_vista_correa1 and (np.array_equal( np.array(cont_d),np.array([0,0,0,0,0,0,1,0,0])) or np.array_equal( np.array(cont_d),np.array([0,1,0,0,0,0,1]))):                
                    #print("np.array([0,0,0,0,0,0,1])")
                    
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    #print("ax",ax,"ang",ang)
                    #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    pos = [tvec[0],tvec[1]+3,tvec[2]]
                    marker_node.setPosition(pos)
                    mesh_node.setVisible(True)
                   
                if id[0] == id_vista_correa1 and (np.array_equal( np.array(cont_d),np.array([1,1,0,0,0,0,1,0,0]))):                
                    mesh_node.setVisible(False)
                    if cont_cambio_1 < 20:
                        print("entra pero no funca")
                        bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                        bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                        bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                        bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                        rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                        rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                        ax = Ogre.Vector3(*rvec)
                        ang = ax.normalise()
                        #print("ax",ax,"ang",ang)
                        #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                        marker_node_2.setOrientation(Ogre.Quaternion(ang, ax))
                        pos = [tvec[0]-4,tvec[1],tvec[2]]
                        marker_node_2.setPosition(pos)
                        mesh_node_2.setVisible(True)
                    else:
                        mesh_node_2.setVisible(False)
                        bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                        bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                        bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                        bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                        rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                        rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                        ax = Ogre.Vector3(*rvec)
                        ang = ax.normalise()
                        #print("ax",ax,"ang",ang)
                        #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                        marker_node_3.setOrientation(Ogre.Quaternion(ang, ax))
                        pos = [tvec[0]-4,tvec[1],tvec[2]]
                        marker_node_3.setPosition(pos)
                        mesh_node_3.setVisible(True)
                    cont_cambio_1 = cont_cambio_1 + 1
                if id[0] == id_vista_correa1 and (np.array_equal( np.array(cont_d),np.array([1,2,0,0,0,0,1,0,0]))):                
                    #print("np.array([0,0,0,0,0,0,1])")
                    mesh_node.setVisible(False)
                    mesh_node_2.setVisible(False)
                    mesh_node_3.setVisible(False)
                    #mesh_node_3.setVisible(False)
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    #print("ax",ax,"ang",ang)
                    #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node_3.setOrientation(Ogre.Quaternion(ang, ax))
                    pos = [tvec[0],tvec[1],tvec[2]]
                    marker_node_3.setPosition(pos)
                    mesh_node_3.setVisible(True)  
                #Giro
                if id[0] == id_vista_giro_2_1 and (np.array_equal( np.array(cont_d),np.array([1,2,1,0,0,0,1,0,1]))):                
                    #print("np.array([0,0,0,0,0,0,1])")
                    mesh_node.setVisible(False)
                    mesh_node_2.setVisible(False)
                    mesh_node_3.setVisible(False)
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    #print("ax",ax,"ang",ang)
                    #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node_4.setOrientation(Ogre.Quaternion(ang, ax))
                    pos = [tvec[0],tvec[1]-3,tvec[2]]
                    marker_node_4.setPosition(pos)
                    mesh_node_4.setVisible(True)  
                if id[0] == id_vista_giro_2_2 and (np.array_equal( np.array(cont_d),np.array([1,2,1,0,0,0,1,1,1]))):                
                    #print("np.array([0,0,0,0,0,0,1])")
                    #mesh_node.setVisible(False)
                    #mesh_node_2.setVisible(False)
                    mesh_node_3.setVisible(False)
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    #print("ax",ax,"ang",ang)
                    #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node_4.setOrientation(Ogre.Quaternion(ang, ax))
                    pos = [tvec[0],tvec[1]-3,tvec[2]]
                    marker_node_4.setPosition(pos)
                    mesh_node_4.setVisible(True)  

                if id[0] == id_vista_correa1 and (np.array_equal( np.array(cont_d),np.array([1,2,1,0,0,0,1,2,1]))  or np.array_equal( np.array(cont_d),np.array([2,3,1,0,0,0,1,2,1])) or np.array_equal( np.array(cont_d),np.array([2,4,1,0,0,0,1,2,1]))):                
                    #print("np.array([0,0,0,0,0,0,1])")
                    #mesh_node.setVisible(False)
                    #mesh_node_2.setVisible(False)
                    mesh_node_4.setVisible(False)
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    #print("ax",ax,"ang",ang)
                    #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node_4.setOrientation(Ogre.Quaternion(ang, ax))
                    pos = [tvec[0],tvec[1]-3,tvec[2]]
                    marker_node_4.setPosition(pos)
                    mesh_node_4.setVisible(True)  

                if id[0] == id_vista_giro_2_1 and (np.array_equal( np.array(cont_d),np.array([2,4,2,0,0,0,1,2,2])) ):                
                    print("entro a fase final)")
                    mesh_node.setVisible(False)
                    mesh_node_2.setVisible(False)
                    mesh_node_4.setVisible(False)
                    #mesh_node_5.setVisible(False)
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    #print("ax",ax,"ang",ang)
                    #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node_5.setOrientation(Ogre.Quaternion(ang, ax))
                    pos = [tvec[0],tvec[1],tvec[2]]
                    marker_node_5.setPosition(pos)
                    mesh_node_5.setVisible(True)
                if id[0] == id_vista_correa2 and ( np.array_equal( np.array(cont_d),np.array([2,4,2,0,1,0,1,2,2])) or np.array_equal( np.array(cont_d),np.array([2,4,1,0,1,1,1,2,]))):                
                    print("np.array([0,0,0,0,0,0,1])")
                    mesh_node.setVisible(False)
                    mesh_node_2.setVisible(False)
                    mesh_node_3.setVisible(False)
                    mesh_node_4.setVisible(False)
                    mesh_node_5.setVisible(False)
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    #print("ax",ax,"ang",ang)
                    #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node_5.setOrientation(Ogre.Quaternion(ang, ax))
                    pos = [tvec[0],tvec[1],tvec[2]]
                    marker_node_5.setPosition(pos)
                    mesh_node_5.setVisible(True)  
                if id[0] == id_vista_pinza and   ( np.array_equal( np.array(cont_d),np.array([2,4,2,0,1,1,1,2,2])) or np.array_equal( np.array(cont_d),np.array([2,4,1,0,1,1,2,2,]))):                
                    print("np.array([0,0,0,0,0,0,1])")
                    mesh_node.setVisible(False)
                    mesh_node_2.setVisible(False)
                    mesh_node_3.setVisible(False)
                    mesh_node_4.setVisible(False)
                    mesh_node_5.setVisible(False)
                    bbox[0][0][0],bbox[0][0][1] = (v11, v12)
                    bbox[0][1][0],bbox[0][1][1] = (v21, v22)
                    bbox[0][2][0],bbox[0][2][1] = (v31, v32)
                    bbox[0][3][0],bbox[0][3][1] = (v41, v42)

                    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(bbox, 5, K, None)[:2]
                    rvec, tvec = rvecs[0].ravel(), tvecs[0].ravel()
                        
                    ax = Ogre.Vector3(*rvec)
                    ang = ax.normalise()
                    #print("ax",ax,"ang",ang)
                    #marker_node.setOrientation(Ogre.Quaternion(ang, ax))
                    marker_node_5.setOrientation(Ogre.Quaternion(ang, ax))
                    pos = [tvec[0]-4,tvec[1],tvec[2]]
                    marker_node_5.setPosition(pos)
                    mesh_node_5.setVisible(True)  
            if len(id_detect_s0) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s0[0]- x_detect_s0[1])**2 + (y_detect_s0[0]- y_detect_s0[1])**2)**0.5
                print("distancia0:",distancia)
                file.write("distancia0:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 90:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor0")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        if sw_d[0] == False:
                            cont_d[0] = cont_d[0] + 1
                            sw_d[0] = True
                    except:
                        print("An exception occurred")
                    #print("cont_d[0] ",cont_d[0]) 
                elif distancia > 94:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor0")
                    #var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.c1")
                    
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        sw_d[0] = False
                        cont_cambio_1 = 0
                    except:
                        print("An exception occurred")

            if len(id_detect_s1) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s1[0]- x_detect_s1[1])**2 + (y_detect_s1[0]- y_detect_s1[1])**2)**0.5
                print("distancia1:",distancia)
                file.write("distancia1:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 80:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor1")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        if sw_d[1] == False:
                            cont_d[1] = cont_d[1] + 1
                            sw_d[1] = True
                    except:
                        print("An exception occurred")
                    
                elif distancia > 84:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor1")
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        sw_d[1] = False
                    except:
                        print("An exception occurred")
                
            if len(id_detect_s2) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s2[0]- x_detect_s2[1])**2 + (y_detect_s2[0]- y_detect_s2[1])**2)**0.5
                print("distancia2:",distancia)
                file.write("distancia2:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 88:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor2")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        if sw_d[2] == False:
                            cont_d[2] = cont_d[2] + 1
                            sw_d[2] = True
                    except:
                        print("An exception occurred")
                elif distancia > 89:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor2")
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        sw_d[2] = False
                    except:
                        print("An exception occurred")
            if len(id_detect_s3) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s3[0]- x_detect_s3[1])**2 + (y_detect_s3[0]- y_detect_s3[1])**2)**0.5
                print("distancia3:",distancia)
                file.write("distancia3:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 58:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor3")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        if sw_d[3] == False:
                            cont_d[3] = cont_d[3] + 1
                            sw_d[3] = True
                    except:
                        print("An exception occurred")
                elif distancia > 60:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor3")
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        sw_d[3] = False
                    except:
                        print("An exception occurred")
            if len(id_detect_s4) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s4[0]- x_detect_s4[1])**2 + (y_detect_s4[0]- y_detect_s4[1])**2)**0.5
                print("distancia4:",distancia)
                file.write("distancia4:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 82:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor4")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        if sw_d[4] == False:
                            cont_d[4] = cont_d[4] + 1
                            sw_d[4] = True
                    except:
                        print("An exception occurred")
                elif distancia > 85:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor4")
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        sw_d[4] = False
                    except:
                        print("An exception occurred")
            if len(id_detect_s5) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s5[0]- x_detect_s5[1])**2 + (y_detect_s5[0]- y_detect_s5[1])**2)**0.5
                print("distancia5:",distancia)
                file.write("distancia5:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 62:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor5")
                    dv1 = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        if sw_d[5] == False:
                            cont_d[5] = cont_d[5] + 1
                            sw_d[5] = True
                    except:
                        print("An exception occurred")
                elif distancia > 64:
                    var1 = client.get_node("ns=2;s=Channel1.CPX-CEC-C1-V3.Application.GVL.marcasensor5")
                    dv1 = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                    try:
                        var1.set_value(dv1)
                        sw_d[5] = False
                    except:
                        print("An exception occurred")
            if len(id_detect_s6) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s6[0]- x_detect_s6[1])**2 + (y_detect_s6[0]- y_detect_s6[1])**2)**0.5
                print("distancia6:",distancia)
                file.write("distancia6:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 97:
                    if sw_d[6] == False:
                        cont_d[6] = cont_d[6] + 1
                        sw_d[6] = True
                elif distancia > 99:
                    sw_d[6] = False
            if len(id_detect_s7) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s7[0]- x_detect_s7[1])**2 + (y_detect_s7[0]- y_detect_s7[1])**2)**0.5
                print("distancia7:",distancia)
                file.write("distancia7:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 73:
                    if sw_d[7] == False:
                        cont_d[7] = cont_d[7] + 1
                        sw_d[7] = True
                elif distancia > 75:
                    sw_d[7] = False
            if len(id_detect_s8) == 2:
                file = open("./distancias.txt", "a")
                distancia =  ((x_detect_s8[0]- x_detect_s8[1])**2 + (y_detect_s8[0]- y_detect_s8[1])**2)**0.5
                print("distancia8:",distancia)
                file.write("distancia8:"+str(distancia)+ os.linesep)
                file.close()
                if distancia <= 159:
                    if sw_d[8] == False:
                        cont_d[8] = cont_d[8] + 1
                        sw_d[8] = True
                elif distancia > 161:
                    sw_d[8] = False
            print("cont_d",cont_d)
            print("cont_d",cont_d)
            print("cont_d",cont_d)
            print("cont_d",cont_d)
            print("cont_d",cont_d)
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
client = inicio()
if client is None:
    print("Error de conexion")
    exit()
#client = opcua.Client("opc.tcp://192.168.1.111:49320")

file = open("./distancias.txt", "w")
file.close()
ctx = Ogre.Bites.ApplicationContext()
#Calibracion
ctx.initApp()
calibracion()
ctx.closeApp()
print("Detectada")
print("Detectada")
print("Detectada")
time.sleep(1)
#proceso
ctx.initApp()
main(ctx)
ctx.closeApp()
