bl_info = {
    "name": "Auto Apply Scale on Confirmation",
    "author": "KeelanJon",
    "version": (1, 0),  # Set version to 1.0
    "blender": (4, 2, 0),  # Set compatibility for Blender 4.2
    "description": "Applies scale reset after confirming scaling in Object Mode",
    "category": "Object",
}

import bpy

# Define a property for the toggle in the Scene
bpy.types.Scene.auto_apply_scale = bpy.props.BoolProperty(
    name="Auto Apply Scale",
    description="Automatically apply scale after confirming.",
    default=True
)

class OBJECT_OT_scale_and_apply(bpy.types.Operator):
    """Scale and apply scale reset on confirmation"""
    bl_idname = "object.scale_and_apply"
    bl_label = "Scale and Apply Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.transform.resize('INVOKE_DEFAULT')  # Invoke the scale operation
        context.window_manager.modal_handler_add(self)  # Add this operator as a modal handler
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        # If Enter or Left Click is pressed, apply the scale
        if event.type in {'LEFTMOUSE', 'RET', 'NUMPAD_ENTER'} and event.value == 'RELEASE':
            if context.scene.auto_apply_scale:  # Check if auto apply scale is enabled
                for obj in context.selected_objects:
                    if obj.type == 'MESH':
                        context.view_layer.objects.active = obj
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            return {'FINISHED'}

        # If ESC is pressed, cancel scaling
        if event.type == 'ESC' and event.value == 'PRESS':
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

class VIEW3D_PT_auto_apply_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Auto Apply Scale"
    bl_idname = "VIEW3D_PT_auto_apply"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Auto Apply"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "auto_apply_scale")  # Add the toggle switch

def register():
    bpy.utils.register_class(OBJECT_OT_scale_and_apply)
    bpy.utils.register_class(VIEW3D_PT_auto_apply_panel)
    # Replace the default scale operator with our custom one
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name="Object Mode")
    kmi = km.keymap_items.new("object.scale_and_apply", 'S', 'PRESS')

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_scale_and_apply)
    bpy.utils.unregister_class(VIEW3D_PT_auto_apply_panel)
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.get("Object Mode")
        if km:
            for kmi in km.keymap_items:
                if kmi.idname == "object.scale_and_apply":
                    km.keymap_items.remove(kmi)
    del bpy.types.Scene.auto_apply_scale  # Remove the property when unregistering

if __name__ == "__main__":
    register()
