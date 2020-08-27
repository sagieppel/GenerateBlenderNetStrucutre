import bpy
import math
import numpy as np
import bmesh
# mesh arrays
print("=================================================")

##########################################################################
def AddImagePlane(x,y,z,wx,wy,ImageMatName):
    wx=int(wx) 
    wy=int(wy) 
    x-=wx/2
    y-=wy/2 
    vs=np.zeros([4,3],dtype=float)
    i=0
    for dx in range(2):
       for dy in range(2):
          vs[i][0]=x+dx*wx
          vs[i][1]=y+dy*wy
          vs[i][2]=z
          i+=1
    
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    
    name=bpy.context.object.data.name
 #   print(bpy.context.object.data.name)
    me = bpy.data.meshes[name]#bpy.context.object.data
    bm = bmesh.new()   # create an empty BMesh 
    bm.from_mesh(me)   # fill it in from a Mesh
    for ff,v in enumerate(bm.verts):
    #   print("before")
     #  print(v.co)
       v.co.x = vs[ff][0]
       v.co.y = vs[ff][1]
       v.co.z = vs[ff][2]
     #  print("after")
    #   print(v.co)

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(me)
    bm.free()
    bpy.data.objects[bpy.context.object.name].data.materials.append(bpy.data.materials[ImageMatName])
################################################################################################
################################################################################################    
###############################################################################
def AddEdge(v1,v2,r,MatName):
    vs=np.zeros([8,3],dtype=float)
    i=0
    for dx in range(2):
       for dy in range(2):
          vs[i][0]=v1[0]+(dx*2-1)*r
          vs[i][1]=v1[1]+(dy*2-1)*r
          vs[i][2]=v1[2]
          i+=1
    #      print(i-1)
     #     print(vs[i-1])
    for dx in range(2):
       for dy in range(2):
          vs[i][0]=v2[0]+(dx*2-1)*r
          vs[i][1]=v2[1]+(dy*2-1)*r
          vs[i][2]=v2[2]
          i+=1
  #  print(vs)
    #----------------------------------------------------------
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    name=bpy.context.object.data.name
 #   print(bpy.context.object.data.name)
    me = bpy.data.meshes[name]#bpy.context.object.data
    bm = bmesh.new()   # create an empty BMesh 
    bm.from_mesh(me)   # fill it in from a Mesh
    for ff,v in enumerate(bm.verts):
    #   print("before")
     #  print(v.co)
       v.co.x = vs[ff][0]
       v.co.y = vs[ff][1]
       v.co.z = vs[ff][2]
     #  print("after")
    #   print(v.co)

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(me)
    bm.free()  # free and prevent further access
    bpy.data.objects[bpy.context.object.name].data.materials.append(bpy.data.materials[MatName])
#    bpy.data.objects[name].select_set(True)
#    bpy.context.view_layer.objects.active = bpy.data.objects[name]
   # bpy.ops.object.modifier_add(type='SUBSURF')
#    bpy.context.object.modifiers["Subdivision"].levels = 4
#    bpy.ops.object.shade_smooth()
################################################################################################
################################################################################################
def DeleteAll():    
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    allMeshes=[]
    for mes in bpy.data.meshes:
       allMeshes.append(mes)
       
    for mes in allMeshes:
        bpy.data.meshes.remove(mes)
##################################################################################################33
####################################################################################################
def CreateNet(wx,wy,h,stp,rb,rs,x0,y0,z0,SpherMat,EdgeMat,sz):  
    wx=int(wx) 
    wy=int(wy) 
    x0-=wx/2
    y0-=wy/2 
    grid=-np.ones([wx+1,wy+1,h],dtype=int)
    Sx=np.zeros([h],dtype=int)
    Fx=np.zeros([h],dtype=int)
    Sy=np.zeros([h],dtype=int)
    Fy=np.zeros([h],dtype=int)

    for i in range(h):
        Sx[i]=int(i)#/2)
        Sy[i]=int(i)#/2)
        Fx[i]=wx-Sx[i]
        Fy[i]=wy-Sy[i]
     #   print(" sx"+str(Sx[i])+" Fy"+str(Fx[i]))
    #----------------------------------------Add vertics---------------------------------------
    verts=[]
    for fz in range(h):
        for fx in range(Sx[fz],Fx[fz]+1,stp):
            for fy in range(Sy[fz],Fy[fz]+1,stp):
                 verts.append((fx+x0,fy+y0,fz*sz+z0))
                 grid[fx,fy,fz]=len(verts)
                 bpy.ops.mesh.primitive_uv_sphere_add(radius=rs, enter_editmode=False, location=(fx+x0,fy+y0,fz*sz+z0))
                 bpy.data.objects[bpy.context.object.name].data.materials.append(bpy.data.materials[SpherMat])
                 bpy.ops.object.shade_smooth()

#                 bpy.ops.object.modifier_add(type='SUBSURF')
#                 bpy.context.object.modifiers["Subdivision"].quality = 5

             #    bpy.data.objects[bpy.context.object.name].data.materials.append(bpy.data.materials['Glow1'])
             
    #------------------------------------Add Faces and Edges-----------------------------------------------

    for fz in range(h):
        for fx in range(Sx[fz],Fx[fz]+1,stp):
            for fy in range(Sy[fz],Fy[fz]+1,stp):
    #...............................................................
                i0=grid[fx,fy,fz] # index of center point
                i1=i2=-1
                if i0==-1: continue
                z=fz-1
                
                for x in range(fx-stp-1,fx+stp+1):
                    for y in range(fy-stp-1,fy+stp+1):
                        if  (x>=0)*(x<=wx)*(y>=0)*(y<=wy)*(z>=0)*(z<h)>0:
                            
                            if grid[x,y,z]>-1:
                                AddEdge((x+x0,y+y0,z*sz+z0),(fx+x0,fy+y0,fz*sz+z0),rb,EdgeMat)  
######################################################################################################################
##########################################################################################################################
H=5
Wy=16
Wx=12
Stp=2

RB=0.02
RS=0.4
sz=4
##########################################################################################################################



DeleteAll()
AddImagePlane(0,0,-23,Wx*2,Wy*2,"Img")
##CreateNet(Wx,Wy,H,Stp,RB,RS,0,0,0,"SideGlowPurple","SideGlowGreen",sz)
CreateNet(int(Wx),int(Wy),H,Stp,RB,RS,0,0,0,"Metal","MetalWhite",sz)
AddImagePlane(0,0,H*sz+2,int(Wx),int(Wy),"AnnVes")
CreateNet(int(Wx/2),int(Wy/2),int(H),Stp,RB,RS,0,0,H*sz+8,"Metal","MetalWhite",sz)

AddImagePlane(0,0,2*H*sz+2,int(Wx/1.5),int(Wy/1.5),"AnnMat")
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(17.2768611907959, 18.684276580810547, 69.47674560546875),rotation=(18.474485397338867, 43.626380920410156, 42.469425201416016))
#bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(29.24881935119629, 22.027719497680664, 78.00833129882812),rotation=(18.400497436523438, 43.60978698730469, 42.4684944152832))

#Toc
#bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(22.33749771118164, 25.219913482666016, 70.05426025390625),rotation=(18.474485397338867, 43.626380920410156, 42.469425201416016))







































