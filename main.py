# Rotating cube python project
from simulator import Simulator

sim = Simulator("Simulator", 1280, 720, True)

while sim.run:
    sim.handle_events()
    sim.update()
    sim.render()
    sim.clean()
