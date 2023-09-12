import omni.ext
import omni.ui as ui
import omni.kit.commands


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[omniversefromscratch.core.walls] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class OmniversefromscratchCoreWallsExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[omniversefromscratch.core.walls] omniversefromscratch core walls startup")

        self._count = 0
        # left/right
        self._z = 0
        self._scale = 1.0
        self._deltaZ = 10
        self._deltaScale = 0.1
        self._frCurrent = 1.0
        self._fr1 = 1.0
        self._fr2 = 1.5
        self._fr3 = 2.0

        self._window = ui.Window("Walls", width=300, height=300)
        with self._window.frame:
            with ui.VStack():

                def new_wall():
                    omni.kit.commands.execute('CreateMeshPrimWithDefaultXform', prim_type='Cube', above_ground=True)

                def move_left():
                    omni.kit.commands.execute('TransformMultiPrimsSRTCpp', count=1, paths=['/World/Cube'],
                                              new_translations=[0.0, 0.0, self._z + self._deltaZ],
                                              old_translations=[0.0, 0.0, self._z])
                    self._z += self._deltaZ

                def move_right():
                    omni.kit.commands.execute('TransformMultiPrimsSRTCpp', count=1, paths=['/World/Cube'],
                                              new_translations=[0.0, 0.0, self._z-self._deltaZ],
                                              old_translations=[0.0, 0.0, self._z])
                    self._z -= self._deltaZ

                def shorten_wall():
                    omni.kit.commands.execute('TransformMultiPrimsSRTCpp', count=1, paths=['/World/Cube'],
                                              new_translations=[0.0, 0.0, self._z],
                                              new_scales=[self._frCurrent, 1.0, self._scale * (1-self._deltaScale)],
                                              old_translations=[0.0, 0.0, self._z],
                                              old_scales=[self._frCurrent, 1.0, self._scale])
                    self._scale *= (1-self._deltaScale)

                def lengthen_wall():
                    omni.kit.commands.execute('TransformMultiPrimsSRTCpp', count=1, paths=['/World/Cube'],
                                              new_translations=[0.0, 0.0, self._z],
                                              new_scales=[self._frCurrent, 1.0, self._scale * (1+self._deltaScale)],
                                              old_translations=[0.0, 0.0, self._z],
                                              old_scales=[self._frCurrent, 1.0, self._scale])
                    self._scale *= (1+self._deltaScale)

                def firerate_1hr():
                    omni.kit.commands.execute('TransformMultiPrimsSRTCpp', count=1, paths=['/World/Cube'],
                                              new_translations=[0.0, 0.0, self._z],
                                              new_scales=[self._fr1, 1.0, self._scale],
                                              old_translations=[0.0, 0.0, self._z],
                                              old_scales=[self._frCurrent, 1.0, self._scale])
                    self._frCurrent = self._fr1

                def firerate_2hr():
                    omni.kit.commands.execute('TransformMultiPrimsSRTCpp', count=1, paths=['/World/Cube'],
                                              new_translations=[0.0, 0.0, self._z],
                                              new_scales=[self._fr2, 1.0, self._scale],
                                              old_translations=[0.0, 0.0, self._z],
                                              old_scales=[self._frCurrent, 1.0, self._scale])
                    self._frCurrent = self._fr2

                def firerate_3hr():
                    omni.kit.commands.execute('TransformMultiPrimsSRTCpp', count=1, paths=['/World/Cube'],
                                              new_translations=[0.0, 0.0, self._z],
                                              new_scales=[self._fr3, 1.0, self._scale],
                                              old_translations=[0.0, 0.0, self._z],
                                              old_scales=[self._frCurrent, 1.0, self._scale])
                    self._frCurrent = self._fr3

                def on_reset():
                    omni.kit.commands.execute('DeletePrims', paths=['/World/Cube'], destructive=False)
                    self._z = 0
                    self._scale = 1.0

                with ui.HStack():
                    ui.Button("+ New Wall", clicked_fn=new_wall)
                    ui.Button("Move Left", clicked_fn=move_left)
                    ui.Button("Move Right", clicked_fn=move_right)

                with ui.HStack():
                    ui.Button("Shorten Wall", clicked_fn=shorten_wall)
                    ui.Button("Lengthen Wall", clicked_fn=lengthen_wall)

                with ui.HStack():
                    ui.Label("Fire Rating")

                with ui.HStack():
                    ui.Button("1hr", clicked_fn=firerate_1hr)
                    ui.Button("2hr", clicked_fn=firerate_2hr)
                    ui.Button("3hr", clicked_fn=firerate_3hr)

                with ui.HStack():
                    ui.Button("Reset", clicked_fn=on_reset)

    def on_shutdown(self):
        print("[omniversefromscratch.core.walls] omniversefromscratch core walls shutdown")
