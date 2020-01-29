FREECADPATH = '/usr/lib/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import bpy,bmesh
import math
from addon_utils import check, paths, enable

def import_fcstd(filename):
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
            
        import Part
        doc = FreeCAD.open(filename)
        objects = doc.Objects
        for ob in objects:
            print ("found "+ob.TypeId+" "+ob.Name)
            if ob.TypeId == 'PartDesign::Body':
                shape = ob.Shape
                if shape.Faces:
                    mesh = bpy.data.meshes.new("my_mesh")
                    rawdata = shape.tessellate(0.1)
                    mesh.from_pydata(rawdata[0], [], rawdata[1])

                    # post-process mesh
                    for edge in mesh.edges:   
                        edge.use_seam = True
                    #bpy.ops.uv.smart_project(mesh)

                    obj = bpy.data.objects.new("my_obj", mesh)
                    bpy.context.collection.objects.link(obj)
                    bpy.context.view_layer.objects.active = obj
                    print ( ob.Name + " -> "+str(len(rawdata[0]))+" vertices, " + str(len(rawdata[1]))+ " faces processed\n" )

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
    import_fcstd(filename)
    blendfile='/work/output/blender.blend'
    bpy.ops.wm.save_as_mainfile(filepath=blendfile)
    print("saved to "+blendfile)
    pdffile='/work/output/paper_model.pdf'
    #rotate_and_render('/work/output/')
    bpy.ops.export_mesh.paper_model(
        filepath=pdffile, 
        page_size_preset='A4', 
        scale=100)

# This lets you import the script without running it
if __name__=='__main__':
   main()