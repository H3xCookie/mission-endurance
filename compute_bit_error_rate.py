import numpy as np
import matplotlib.pyplot as plt
def to_db(x):
    return 10*np.log10(x) 

def p_ber(eb_no):
    return np.log10(1/2*np.exp(-eb_no))

def compute_eb_no(input_power):
    P_t = to_db(input_power) 
    G_t = -2
    G_r = 14
    T_s = to_db(500)

    freq = 435*10**6
    c = 3*10**8
    l = c/freq
    L_fs = 20*np.log10(4*np.pi*2640000/l)

    L_a = 9
    k_b = to_db(1.38*10**(-23))
    R = to_db(19200)
    eb_no_db = G_t + P_t + G_r - T_s - L_fs - L_a + k_b - R
    print(eb_no_db) 
    return 10**(eb_no_db/10) 

def make_graph():
    powers = np.logspace(start=-2, stop=2, num=50)
    eb_nos = [compute_eb_no(p) for p in powers]
    print(eb_nos)
    plt.plot(eb_nos, [p_ber(eb_no) for eb_no in eb_nos])
    plt.xlabel("$E_b/N_0$, unitless")
    plt.ylabel("$P_{ber}$, logP")
    plt.show()


print(compute_eb_no(2))
