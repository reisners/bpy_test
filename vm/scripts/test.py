FREECADPATH = '/usr/lib/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import math
import bpy
import bmesh
from addon_utils import check, paths, enable
from collections import defaultdict

def convert_to_paper_model(filename, page_size_preset, split_index):
    try:
        import FreeCAD
    except ValueError:
        print ('import error\n')
    else:

        scene = provide_scene()

        doc = FreeCAD.open(filename)
#        parent_bmesh, parent = create_parent()
#        import_freecad_model(doc, parent_bmesh)
#        bmesh.update_edit_mesh(parent.data)
#        bpy.context.view_layer.objects.active = parent
#        parent.select_set(True)    

        objects = import_freecad_model(doc)
        #bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')

        print ("active object type "+bpy.context.active_object.type)

        bpy.ops.wm.save_as_mainfile(filepath="/work/output/paper_model.blend")

        pdffile='/work/output/paper_model.pdf'
        bpy.ops.export_mesh.paper_model(
            filepath=pdffile, 
            page_size_preset=page_size_preset, 
            scale=100)

def import_freecad_model(doc, parent_bmesh):
    objects = doc.Objects
    for ob in objects:
        print ("found "+ob.TypeId+" "+ob.Name)
        if ob.TypeId == 'Part::FeaturePython':
            if ob.Faces:
                obj = facebinder_to_object(ob)
                parent_bmesh.from_mesh(obj.data)

def import_freecad_model(doc):
    objects = doc.Objects
    return [facebinder_to_object(fb) for fb in objects if fb.TypeId == 'Part::FeaturePython' and fb.Faces]

def facebinder_to_object(ob):
    print (ob.Name+" has "+str(len(ob.Faces))+" faces")
    mesh = bpy.data.meshes.new("mesh_"+ob.Name)
    rawdata = ob.Shape.tessellate(0.1)
    mesh.from_pydata(rawdata[0], [], rawdata[1])

    obj = bpy.data.objects.new("obj_"+ob.Name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    print ( ob.Name + " -> "+str(len(rawdata[0]))+" vertices, " + str(len(rawdata[1]))+ " faces processed\n" )
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(obj.data)

    edges = defaultdict(set)

    for face in bm.faces:
        for edge in face.edges:
            edges[edge].add(face)

    boundary = [edge for edge in edges if len(edges[edge]) == 1]
    for edge in boundary:
        edge.seam = True

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    return obj

def create_parent():
    parent_mesh = bpy.data.meshes.new("mesh_parent")
    parent_mesh.from_pydata([], [], [])
    parent = bpy.data.objects.new("parent", parent_mesh)
    bpy.context.collection.objects.link(parent)
    bpy.context.view_layer.objects.active = parent
    bpy.ops.object.mode_set(mode='EDIT')

    parent_bmesh = bmesh.from_edit_mesh(parent_mesh)
    return parent_bmesh, parent

def provide_scene():
    scene = bpy.context.scene

    if scene.world is None:
        # create a new world
        new_world = bpy.data.worlds.new("New World")
        new_world.use_sky_paper = True
        scene.world = new_world

    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)

    return scene

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