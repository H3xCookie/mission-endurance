import numpy as np
import math
import matplotlib.pyplot as plt

def to_db(x):
    return 10*np.log10(x) 

# for 2-fsk
def p_ber(eb_no):
    return np.log10(1/2*np.exp(-eb_no))

def log_p_ber_qpsk(ebno):
    return 1/2*math.erfc((ebno)**0.5)

def compute_eb_no(input_power, d):
    P_t = to_db(input_power)
    G_t = 3 
    G_r = 0
    T_s = to_db(450)

    freq = 450*10**6 
    c = 3*10**8
    l = c/freq
    L_fs = 20*np.log10(4*np.pi*d/l)

    L_a = 1
    k_b = to_db(1.38*10**(-23))
    R = to_db(15200)
    eb_no_db = G_t + P_t + G_r - T_s - L_fs - L_a - k_b - R
    return 10**(eb_no_db/10) 

def make_graph():
    p1 = 10**(46/10) / 1000
    distances = np.linspace(start=7, stop=8, num=50) 
    eb_nos = [compute_eb_no(p1, 10**d) for d in distances]
    eb_nos_db = [to_db(ebno) for ebno in eb_nos]
    print(eb_nos_db)
    plt.plot(distances, [np.log10(log_p_ber_qpsk(eb_no)) for eb_no in eb_nos])
    plt.xlabel("logD")
    plt.ylabel("$P_{ber}$, logP")
    plt.show()

make_graph()
