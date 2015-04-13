'''
Copyright (C) 2015 YOUR NAME
YOUR@MAIL.com

Created by YOUR NAME

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "My Addon Name",
    "description": "",
    "author": "Your Name",
    "version": (0, 0, 1),
    "blender": (2, 74, 0),
    "location": "View3D",
    "warning": "This is an unstable version",
    "wiki_url": "",
    "category": "Object" }

import bpy


def import_submodules():
    import os, sys, importlib
    
    def use_file(path):
        if path == __file__: return False
        if path.endswith(".py"): return True
        return False
    
    # don't import other modules when the file is executed inside of Blender
    if __name__ == "__main__": return []

    current_path = os.path.dirname(__file__)
    
    # find all python files in this addon
    python_files = []
    for root, directories, files in os.walk(current_path):
        for file_name in files:
            file_path = root + "\\" + file_name
            if use_file(file_path):
                python_files.append(file_path)
    
    # import found files as submodules   
    loaded_modules = []          
    for file_path in python_files:
        module_name = __name__ + "." + file_path[len(current_path)+1:-3]
        if module_name in sys.modules:
            del sys.modules[module_name]
        loaded_modules.append(importlib.import_module(module_name))
        
    return loaded_modules
        
loaded_modules = import_submodules()  


   
   
def register():
    try: bpy.utils.register_module(__name__)
    except: pass
    
    # don't use a register function in a submodule to register classes
    for module in loaded_modules:
        if hasattr(module, "register"):
            module.register()

def unregister():
    try: bpy.utils.unregister_module(__name__)
    except: pass

    for module in loaded_modules:
        if hasattr(module, "unregister"):
            module.register()