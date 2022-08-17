import numpy as np
import matplotlib.pyplot as plt

def to_db(x):
    return 10*np.log10(x) 

def p_ber(eb_no):
    return np.log10(1/2*np.exp(-eb_no))

def log_p_ber_qpsl(ebno):
    return np.log10(3*np.exp(-ebno)/(4*np.pi*ebno)**0.5)

def compute_eb_no(input_power):
    P_t = to_db(input_power) 
    G_t = 0 
    G_r = 0 
    T_s = to_db(400)

    freq = 2.4*10**9
    c = 3*10**8
    l = c/freq
    d = 10
    L_fs = 20*np.log10(4*np.pi*d/l)

    L_a = 1
    k_b = to_db(1.38*10**(-23))
    R = to_db(850*10**6)
    eb_no_db = G_t + P_t + G_r - T_s - L_fs - L_a - k_b - R
    print("ebondb:", eb_no_db)
    return 10**(eb_no_db/10) 

def make_graph():
    powers = np.logspace(start=-0.5, stop=1, num=50)
    print("powers", powers)
    eb_nos = [compute_eb_no(p) for p in powers]
    eb_nos_db = [to_db(ebno) for ebno in eb_nos]
    plt.plot(eb_nos_db, [p_ber(eb_no) for eb_no in eb_nos])
    plt.xlabel("$E_b/N_0$, dB")
    plt.ylabel("$P_{ber}$, logP")
    plt.show()

p1 = 0.2
ebno = compute_eb_no(p1)
print("EB_NO: ", ebno)
print(f"BER for 1: {log_p_ber_qpsl(ebno)}")
