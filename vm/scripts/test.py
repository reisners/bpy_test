FREECADPATH = '/usr/lib/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import bpy,bmesh
import math

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
            if ob.TypeId[:12] == 'PartDesign::':
                shape = ob.Shape
                if shape.Faces:
                    mesh = bpy.data.meshes.new("my_mesh")
                    rawdata = shape.tessellate(1)
                    mesh.from_pydata(rawdata[0], [], rawdata[1])
                    obj = bpy.data.objects.new("my_obj", mesh)
                    bpy.context.collection.objects.link(obj)
                    print ( ob.Name + " -> "+str(len(rawdata[0]))+" vertices, " + str(len(rawdata[1]))+ " faces processed\n" )

import mathutils
import io_export_paper_model

def rotate_and_render(output_dir):
    origin = bpy.context.object
    scene = bpy.context.scene

    # Create a light
    light_data = bpy.data.lights.new('light', type='POINT')
    light = bpy.data.objects.new('light', light_data)
    scene.collection.objects.link(light)
    light.location = mathutils.Vector((3, -4.2, 5))

    # Create the camera
    cam_data = bpy.data.cameras.new('camera')
    cam = bpy.data.objects.new('camera', cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    cam.location = mathutils.Vector((6, -3, 5))
    cam.rotation_euler = mathutils.Euler((0.9, 0.0, 1.1))

    scene.render.engine = 'CYCLES'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = output_dir + '/image.png'

    print("rendering\n")
    bpy.ops.render.render(write_still = True)
    print("rendered\n")

def main():
    filename=sys.argv[1]
    import_fcstd(filename)
    rotate_and_render('/work/output/')

# This lets you import the script without running it
if __name__=='__main__':
   main()