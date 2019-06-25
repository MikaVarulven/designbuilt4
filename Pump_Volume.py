'''
    This code is translated from Matlab so maybe some lines might
    seem weird, please change them if you can :)
'''

from math import exp

''' ---------------------- Declare Constants ---------------------- '''
C0 = 895000  # [cells/mL] Initial concentration in the food tank
Ca = 5000  # [cells/mL] Desired concentration in the mussel tank

time = [0]  # [min] Starting experiment time
Volume = [1025]  # [mL] Initial volume in the mussel tank
n_init = Ca * Volume[-1]  # [cells] Initial number of algae in the mussel tank
nAlgae = [n_init]

pump_threshold = 1  # [mL] Minimum amount of volume being pumped
V_pump = []  # Volume of algae solution pumped in each time interval

''' --------------- Declare Mathematical Functions ----------------- '''
k = 0.039344  # Exponential Constant
m = 57.2405  # Linear Regression Constant
t_Exp = 24 * 60  # [min] Total experimental time


def C_algae(t, C_init):
    # The theoretical algae growth function under controlled condition
    C_t = C_init * exp(k * t / 60)  # Concentration at time t
    return C_t


def F_mussel(C):
    # The theoretical algae consumption rate based on the algae concentration
    # that the mussel is situated in
    return m * C


def C_mussel(V, t):
    # The theoretical concentration changing curve in the mussel tank
    # assuming the starting concentration is always the desired concentration Ca
    return Ca * exp(-m / V * t)


def n_consume(V, t):
    # The theoretical number of algae that has been consumed in time interval t
    # in a mussel tank with volume V and initial concentration of Ca
    return V * (5000 - C_mussel(V, t))


''' --------------------- Simulation of the Model -------------------------- '''
while time[-1] < t_Exp:
    t_interval = 10  # Assume that the pumping interval is 10 minutes
    while True:
        t_now = time[-1] + t_interval  # Current time in the experiment
        n_now = nAlgae[-1] - n_consume(Volume[-1], t_interval)  # Current algae number in the mussel tank
        C_feed = C_algae(t_now, Ca)  # Current food concentration being pumped
        V_add = (Ca * Volume[-1] - n_now) / (C_feed - Ca)  # Theoretical volume to be pumped
        if V_add < pump_threshold:
            t_interval += 1
        else:
            break
    time += [t_now]
    V_pump += [V_add]
    Volume += [Volume[-1] + V_add]
    nAlgae += [n_now + V_add * C_feed]
