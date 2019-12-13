FREECADPATH = '/usr/lib/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import bpy,bmesh

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
def main():
    filename=sys.argv[1]
    import_fcstd(filename)
 
# This lets you import the script without running it
if __name__=='__main__':
   main()