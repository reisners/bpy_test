FREECADPATH = '/usr/lib/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import math
import bpy
from addon_utils import check, paths, enable

def convert_to_paper_model(filename, page_size_preset, split_index):
    try:
        import FreeCAD
    except ValueError:
        print ('import error\n')
    else:
        print(bpy.context.area.type)
        previous_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'

        print(bpy.context.area.type)
        scene = bpy.context.scene

        if scene.world is None:
            # create a new world
            new_world = bpy.data.worlds.new("New World")
            new_world.use_sky_paper = True
            scene.world = new_world

        for vl in scene.view_layers:
            print(vl)
            for o in vl.objects:
                print(o)

        objs = bpy.data.objects
        objs.remove(objs["Cube"], do_unlink=True)

        print(bpy.context.area.type)

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
                    #bpy.context.collection.objects.link(obj)
                    print ( ob.Name + " -> "+str(len(rawdata[0]))+" vertices, " + str(len(rawdata[1]))+ " faces processed\n" )

        bpy.context.collection.objects.link(parent)
        bpy.context.view_layer.objects.active = parent

        for vl in scene.view_layers:
            print(vl)
            for o in vl.objects:
                print(o)

        print(bpy.context.area.type)

        pdffile='/work/output/paper_model.pdf'
        bpy.ops.export_mesh.paper_model(
            filepath=pdffile, 
            page_size_preset=page_size_preset, 
            scale=100)

        #restore previous context
        bpy.context.area.type = previous_context

import io_export_paper_model


def main():
    enable('io_export_paper_model')
    filename=sys.argv[1]
    page_size_preset=sys.argv[2]
    split_index=int(sys.argv[3])
    convert_to_paper_model(filename, page_size_preset, split_index)

# This lets you import the script without running it
if __name__=='__main__':
   main()