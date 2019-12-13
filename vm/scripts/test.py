FREECADPATH = '/usr/lib/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import bpy

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
            if ob.Type[:4] == 'Part':
                shape = ob.Shape
                if shape.Faces:
                    mesh = bpy.Mesh.New()
                    rawdata = shape.tessellate(1)
                    for v in rawdata[0]:
                        mesh.verts.append((v.x,v.y,v.z))
                    for f in rawdata[1]:
                        mesh.faces.append.append(f)
                    scene.objects.new(mesh,ob.Name)

def main():
    filename=sys.argv[1]
    import_fcstd(filename)
 
# This lets you import the script without running it
if __name__=='__main__':
   main()