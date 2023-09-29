import definitions
import random

## trisolaris preset
# Initial objects (for testing)
# Randomized values
ACA = definitions.MassiveObject(6.96*(10**8), definitions.Position(random.uniform(-3.5*(10**12), 3.5*(10**12)), random.uniform(-3.5*(10**12), 3.5*(10**12))), definitions.Velocity(random.uniform(-5000, 5000), random.uniform(-5000, 5000)), 2*(10**30), "Alpha Centauri A")
ACB = definitions.MassiveObject(4.91*(10**8), definitions.Position(random.uniform(-3.5*(10**12), 3.5*(10**12)), random.uniform(-3.5*(10**12), 3.5*(10**12))), definitions.Velocity(random.uniform(-5000, 5000), random.uniform(-5000, 5000)), 1.6*(10**30), "Alpha Centauri B", (255, 100, 40))
PC = definitions.MassiveObject(7.4*(10**7), definitions.Position(random.uniform(-3.5*(10**12), 3.5*(10**12)), random.uniform(-3.5*(10**12), 3.5*(10**12))), definitions.Velocity(random.uniform(-5000, 5000), random.uniform(-5000, 5000)), 2.39*(10**29), "Proxima Centauri", (255, 194, 77))
TS = definitions.MassiveObject(7*(10**7), definitions.Position(random.uniform(-3.5*(10**12), 3.5*(10**12)), random.uniform(-3.5*(10**12), 3.5*(10**12))), definitions.Velocity(random.uniform(-5000, 5000), random.uniform(-5000, 5000)), 5.97*(10**24), "Trisolaris", (77, 255, 194))

objects_Trisolaris = [ACA, ACB, PC, TS]

## sol system preset
# Initial objects (for testing)
Sol = definitions.MassiveObject(6.96*(10**8), definitions.Position(0, 0), definitions.Velocity(0, 0), 1.9891*(10**30), "Sol", (255, 255, 0))
Mercury = definitions.MassiveObject(2.4397*(10**6), definitions.Position(5.791*(10**10), 0), definitions.Velocity(0, 47.362*(10**3)), 3.3011*(10**23), "Mercury", (255, 255, 255))
Venus = definitions.MassiveObject(6.0518*(10**6), definitions.Position(1.082*(10**11), 0), definitions.Velocity(0, 35.02*(10**3)), 4.8675*(10**24), "Venus", (255, 255, 255))
Earth = definitions.MassiveObject(6.371*(10**6), definitions.Position(1.496*(10**11), 0), definitions.Velocity(0, 29.78*(10**3)), 5.97237*(10**24), "Earth", (0, 0, 255))
Mars = definitions.MassiveObject(3.3895*(10**6), definitions.Position(2.279*(10**11), 0), definitions.Velocity(0, 24.077*(10**3)), 6.4171*(10**23), "Mars", (255, 0, 0))
Jupiter = definitions.MassiveObject(6.9911*(10**7), definitions.Position(7.785*(10**11), 0), definitions.Velocity(0, 13.07*(10**3)), 1.8982*(10**27), "Jupiter", (255, 255, 0))
Saturn = definitions.MassiveObject(5.8232*(10**7), definitions.Position(1.433*(10**12), 0), definitions.Velocity(0, 9.69*(10**3)), 5.6834*(10**26), "Saturn", (255, 255, 0))
Uranus = definitions.MassiveObject(2.5362*(10**7), definitions.Position(2.877*(10**12), 0), definitions.Velocity(0, 6.81*(10**3)), 8.6810*(10**25), "Uranus", (0, 255, 255))
Neptune = definitions.MassiveObject(2.4622*(10**7), definitions.Position(4.503*(10**12), 0), definitions.Velocity(0, 5.43*(10**3)), 1.02413*(10**26), "Neptune", (0, 0, 255))
Pluto = definitions.MassiveObject(1.1883*(10**6), definitions.Position(5.906*(10**12), 0), definitions.Velocity(0, 4.67*(10**3)), 1.303*(10**22), "Pluto", (255, 255, 255))

objects_Sol = [Sol, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]


## Three identical sun system
# Initial objects (for testing)
FlennestraA = definitions.MassiveObject(6.96*(10**8), definitions.Position(random.uniform(-1.5*(10**11), 1.5*(10**11)), random.uniform(-1.5*(10**11), 1.5*(10**11))), definitions.Velocity(0, 0), 1.9891*(10**30), "Flennestra 34-A", (0, 255, 255))
FlennestraB = definitions.MassiveObject(6.96*(10**8), definitions.Position(random.uniform(-1.5*(10**11), 1.5*(10**11)), random.uniform(-1.5*(10**11), 1.5*(10**11))), definitions.Velocity(0, 0), 1.9891*(10**30), "Flennestra 34-B", (0, 255, 255))
FlennestraC = definitions.MassiveObject(6.96*(10**8), definitions.Position(random.uniform(-1.5*(10**11), 1.5*(10**11)), random.uniform(-1.5*(10**11), 1.5*(10**11))), definitions.Velocity(0, 0), 1.9891*(10**30), "Flennestra 34-C", (0, 255, 255))

objects_Flennestra = [FlennestraA, FlennestraB, FlennestraC]