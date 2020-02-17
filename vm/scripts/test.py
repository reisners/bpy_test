FREECADPATH = '/usr/lib/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import bpy,bmesh
import math
from addon_utils import check, paths, enable

def convert_to_paper_model(filename, page_size_preset, split_index):
    try:
        import FreeCAD
    except ValueError:
        print ('import error\n')
    else:
        scene = bpy.context.scene

        if scene.world is None:
            # create a new world
            new_world = bpy.data.worlds.new("New World")
            new_world.use_sky_paper = True
            scene.world = new_world
            
        for o in bpy.context.scene.objects:
            if o.type == 'MESH':
                o.select_set(True)
                print(o)
            else:
                o.select_set(False)

        # Call the operator only once
        bpy.ops.object.delete()

        import Part
        doc = FreeCAD.open(filename)
        
        parent = bpy.data.objects.new("parent", None)

        objects = doc.Objects
        for ob in objects:
            print ("found "+ob.TypeId+" "+ob.Name)
            if ob.TypeId == 'Part::FeaturePython':
                if ob.Faces:
                    print ("facebinder has "+str(len(ob.Faces))+" faces")
                    mesh = bpy.data.meshes.new("mesh_"+ob.Name)
                    rawdata = ob.Shape.tessellate(0.1)
                    mesh.from_pydata(rawdata[0], [], rawdata[1])
                    obj = bpy.data.objects.new("obj_"+ob.Name, mesh)
                    obj.parent = parent
                    bpy.context.collection.objects.link(obj)
                    print ( ob.Name + " -> "+str(len(rawdata[0]))+" vertices, " + str(len(rawdata[1]))+ " faces processed\n" )
            if False: # ob.TypeId == 'PartDesign::Body':
                shape = ob.Shape
                if shape.Faces:
#                    for faceindex, face in enumerate(shape.Faces):
#                        color=shape.DiffuseColor
#                        if len(color) ==1:
#                            facecolor = color[0]
#                        else:
#                            facecolor = color[faceindex]
#                        print (shape.Label, face.Label, color[faceindex])
                    mesh = bpy.data.meshes.new("my_mesh")
                    rawdata = shape.tessellate(0.1)
                    mesh.from_pydata(rawdata[0], [], rawdata[1])

                    mesh.edges[split_index].use_seam = True
                    pdffile='/work/output/paper_model.pdf'
                    #bpy.ops.uv.smart_project()

                    obj = bpy.data.objects.new("my_obj", mesh)
                    bpy.context.collection.objects.link(obj)
                    bpy.context.view_layer.objects.active = obj
                    print ( ob.Name + " -> "+str(len(rawdata[0]))+" vertices, " + str(len(rawdata[1]))+ " faces processed\n" )

        bpy.context.collection.objects.link(parent)
        bpy.context.view_layer.objects.active = parent
        #bpy.context.view_layer.update()

        pdffile='/work/output/paper_model.pdf'
        bpy.ops.export_mesh.paper_model(
            filepath=pdffile, 
            page_size_preset=page_size_preset, 
            scale=100)


import mathutils
import io_export_paper_model

def rotate_and_render(output_dir):
    origin = bpy.context.object
    scene = bpy.context.scene

    # Create a light
    light_data = bpy.data.lights.new('light', type='SUN')
    light = bpy.data.objects.new('light', light_data)
    scene.collection.objects.link(light)
    light.location = mathutils.Vector((30, -42, 50))

    # Create the camera
    cam_data = bpy.data.cameras.new('camera')
    cam = bpy.data.objects.new('camera', cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    cam.location = mathutils.Vector((120, -60, 100))
    cam.rotation_euler = mathutils.Euler((0.9, 0.0, 1.1))

    scene.render.engine = 'CYCLES'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = output_dir + '/image.png'

    print("rendering\n")
    bpy.ops.render.render(write_still = True)
    print("rendered\n")

def main():
    enable('io_export_paper_model')
    filename=sys.argv[1]
    page_size_preset=sys.argv[2]
    split_index=int(sys.argv[3])
    convert_to_paper_model(filename, page_size_preset, split_index)

# This lets you import the script without running it
if __name__=='__main__':
   main()