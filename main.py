from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import Vec3, WindowProperties
from direct.task import Task

class CarRoamingGame(ShowBase):
    def __init__(self):
        super().__init__()

        # Window title
        props = WindowProperties()
        props.setTitle("Car Roaming System - Panda3D")
        self.win.requestProperties(props)

        # Disable default camera
        self.disableMouse()

        # Enable lighting (important for GLB)
        self.render.setShaderAuto()

        # ----------------------------
        # LOAD ENVIRONMENT
        # ----------------------------
        self.env = self.loader.loadModel("city/city.glb")
        self.env.reparentTo(self.render)
        self.env.setScale(10)
        self.env.setPos(0, 0, 0)

        # ----------------------------
        # LOAD CAR
        # ----------------------------
        self.car = self.loader.loadModel("car/car.glb")
        self.car.reparentTo(self.render)
        self.car.setScale(1)
        self.car.setPos(0, 0, 1)  # slightly above ground

        # ----------------------------
        # MOVEMENT VARIABLES
        # ----------------------------
        self.speed = 0
        self.max_speed = 50
        self.acceleration = 30
        self.friction = 10
        self.turn_speed = 100

        # ----------------------------
        # KEY INPUT
        # ----------------------------
        self.keys = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False
        }

        self.accept("w", self.set_key, ["forward", True])
        self.accept("w-up", self.set_key, ["forward", False])
        self.accept("s", self.set_key, ["backward", True])
        self.accept("s-up", self.set_key, ["backward", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])

        # Update loop
        self.taskMgr.add(self.update, "update")

    def set_key(self, key, value):
        self.keys[key] = value

    def update(self, task):
        dt = globalClock.getDt()

        # ----------------------------
        # ACCELERATION / BRAKING
        # ----------------------------
        if self.keys["forward"]:
            self.speed += self.acceleration * dt
        elif self.keys["backward"]:
            self.speed -= self.acceleration * dt
        else:
            # Apply friction
            if self.speed > 0:
                self.speed -= self.friction * dt
                if self.speed < 0:
                    self.speed = 0
            elif self.speed < 0:
                self.speed += self.friction * dt
                if self.speed > 0:
                    self.speed = 0

        # Clamp speed
        self.speed = max(-self.max_speed/2, min(self.speed, self.max_speed))

        # ----------------------------
        # TURNING (only when moving)
        # ----------------------------
        if abs(self.speed) > 1:
            if self.keys["left"]:
                self.car.setH(self.car.getH() + self.turn_speed * dt)
            if self.keys["right"]:
                self.car.setH(self.car.getH() - self.turn_speed * dt)

        # ----------------------------
        # MOVE CAR FORWARD
        # ----------------------------
        self.car.setPos(self.car, Vec3(0, self.speed * dt, 0))

        # ----------------------------
        # KEEP CAR ON GROUND (simple)
        # ----------------------------
        self.car.setZ(1)

        # ----------------------------
        # CAMERA FOLLOW SYSTEM
        # ----------------------------
        cam_offset = Vec3(0, -15, 6)
        self.camera.setPos(self.car.getPos() + cam_offset)
        self.camera.lookAt(self.car)

        return Task.cont

# RUN GAME
app = CarRoamingGame()
app.run()

