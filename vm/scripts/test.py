FREECADPATH = '/usr/lib/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import math
import bpy
import bmesh
from addon_utils import check, paths, enable
from collections import defaultdict

def convert_to_paper_model(filename, page_size_preset, overriddenProperties):
    try:
        import FreeCAD
    except ValueError:
        print ('import error\n')
    else:
        scene = provide_scene()

        doc = FreeCAD.open(filename)

        parameterize(doc, overriddenProperties)

        objects = import_freecad_model(App.ActiveDocument)
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
            scale=100,
            output_type='TEXTURE')

def parameterize(doc, overriddenProperties):
    sheet = doc.Spreadsheet
    sheetProperties = [property for property in sheet.PropertiesList if not "Hidden" in sheet.getTypeOfProperty(property)]
    print("template property values:")
    for property in sheetProperties:
        print("  " + property + " = " + str(sheet.get(property)))

    for property in overriddenProperties:
        oldval = str(sheet.get(property))
        sheet.set(property, str(overriddenProperties[property]))
    sheet.recompute()

    print("actual property values:")
    for property in sheetProperties:
        print("  " + property + " = " + str(sheet.get(property)))

def import_freecad_model(doc):
    objects = doc.Objects

    mat = bpy.data.materials.get("texture_1")
    if mat is None:
        mat = bpy.data.materials.new(name="texture_1")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load("/work/textures/texture_1.png")
        mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    return [facebinder_to_object(fb, mat) for fb in objects if fb.TypeId == 'Part::FeaturePython' and fb.Faces]

def facebinder_to_object(facebinder, mat):
    print (facebinder.Name+" \""+facebinder.Label+"\" has "+str(len(facebinder.Faces))+" faces")
    mesh = bpy.data.meshes.new("mesh_"+facebinder.Name)
    rawdata = facebinder.Shape.tessellate(0.1)
    mesh.from_pydata(rawdata[0], [], rawdata[1])

    obj = bpy.data.objects.new("obj_"+facebinder.Name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    print ( facebinder.Name + " -> "+str(len(rawdata[0]))+" vertices, " + str(len(rawdata[1]))+ " faces processed\n" )
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

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

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

def parse_properties(argv):
    properties = {property:value for (property, value) in [split_arg(arg) for arg in argv]}
    print("parsed "+str(argv)+" -> "+str(properties))
    return properties

def split_arg(arg):
    (property,value) = arg.split('=')
    return (property, value)

import io_export_paper_model


def main():
    enable('io_export_paper_model')
    filename=sys.argv[1]
    page_size_preset=sys.argv[2]
    overriddenProperties=parse_properties(sys.argv[3:])
    convert_to_paper_model(filename, page_size_preset, overriddenProperties)

# This lets you import the script without running it
if __name__=='__main__':
   main()