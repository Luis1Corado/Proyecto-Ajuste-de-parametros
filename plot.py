import numpy as np
import math
import matplotlib.pyplot as plt
from numpy.core._multiarray_umath import ndarray
from sympy import *


# Funcion para calcular la presion de saturacion
def psat(CoefA, temp):

    n= len(temp)
    Ps= np.zeros(n)

    for i in range(0, n):
        Ps[i] = math.e**(CoefA[0]-CoefA[1]/(temp[i]+CoefA[2]))
    return Ps

def psatalternativa(CoefA, temp):

    n= len(temp)
    Ps= np.zeros(n)

    for i in range(0, n):
        Ps[i] = (math.exp(CoefA[0]-CoefA[1]/(temp[i]+CoefA[2])))/7.50062

    return Ps
#talter=np.array([100,98.59,95.09,91.05,88.96,88.26,87.96,87.79,87.66,87.83,89.34,92.3,97.18])
#xalte=np.array([0,0.003,0.0123,0.0322,0.0697,0.139,0.231,0.311,0.412,0.545,0.73,0.878,1])
#yalte=np.array([0,0.0544,0.179,0.304,0.365,0.384,0.397,0.406,0.428,0.465,0.567,0.721,1])
#Coefalt=np.array([17.5439,3166.38,193])

#Psalt= psatalternativa(Coefalt,talter)



# Funcion para calcular las composiciones del segundo elemento
def c2(x):
    n = len(x)
    x2 = np.zeros(n)
    for i in range(n):
        x2[i] = 1 - x[i]
    return x2


def gamas(P, Ps, x, y):
    n= len(x)
    gama = np.zeros(n-2)

    for i in range(0 , n-2):
        gama[i] = (y[i+1]*P)/(x[i+1]*Ps[i+1])

    return gama
#print(Psalt)
#print(gamas(101.3, Psalt, xalte, yalte))
# Funcion para calcular la energia de gibss en exceso partida RT
def gibbsE(g1, g2, x1):
     n = len(g1)
     Ge = np.zeros(n)
     x2 = c2(x1)

     for i in range(n):
         Ge[i] = x1[i+1]*math.log(g1[i])+x2[i+1]*math.log(g2[i])

     return Ge

# print(gibbsE(gamas(P,psat(Coef,t),x1, y1), gamas(P , psat(Coef2,t), c2(x1), c2(y1)), x1))
def cortar(x1):
    n = len(x1)
    x = np.zeros(n-2)
    for i in range(n-2):
        x[i] = x1[i+1]
    return x

def experimental(temp, x1, y1, coef1, coef2, P):
    n = len(x1)
    psat1 = psatalternativa(coef1, temp)
    psat2 = psatalternativa(coef2, temp)

    gama1 = gamas(P, psat1, x1, y1)
    gama2 = gamas(P, psat2, c2(x1), c2(y1))

    Gibbs = gibbsE(gama1, gama2, x1)


    x = cortar(x1)

    return x , gama1, gama2, Gibbs

def experimental2(temp, x1, y1, coef1, coef2, P):
    n = len(x1)
    psat1 = psat(coef1, temp)
    psat2 = psat(coef2, temp)

    gama1 = gamas(P, psat1, x1, y1)
    gama2 = gamas(P, psat2, c2(x1), c2(y1))

    Gibbs = gibbsE(gama1, gama2, x1)


    x = cortar(x1)

    return x , gama1, gama2, Gibbs

def BublxP(x1, P, Coeficientes, Coef1, Coef2, V1, V2):

    l1 = Coeficientes[0]
    l2 = Coeficientes[1]
    a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))

    a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))
    x1 = cortar(x1)
    n = len(x1)

    g1 = np.zeros(n)
    g2 = np.zeros(n)
    Ge= np.zeros(n)
    y1 = np.zeros(n)
    T = np.zeros(n)
    Ps1 = np.zeros(n)
    w, z = symbols('w, z')

    x2 = c2(x1)
    for i in range(n):

        g1[i] = math.exp(-math.log(x1[i] + a12 * x2[i]) + x2[i] * (a12 / (x1[i] + a12 * x2[i]) - a21 / (x2[i] + a21 * x1[i])))

        g2[i] = math.exp(-math.log(x2[i] + a21 * x1[i]) + x1[i] * (-a12/(x1[i]+a12*x2[i]) + a21/(x2[i]+a21*x1[i])))

        Ge[i] = (- x1[i] * math.log(x1[i] + (1 - x1[i]) * a12) - (1-x1[i]) * math.log(1 - x1[i] + x1[i] * a21))

        y1[i], T[i] = nsolve([Eq(x1[i] * exp(Coef1[0] - Coef1[1] / (z + Coef1[2])) * g1[i]- P*w, 0), Eq(x2[i] * exp(Coef2[0] - Coef2[1] / (z + Coef2[2])) * g2[i]- P*(1-w), 0)], [w, z], [0.5, 77])

        #y1, t = nsolve ([Eq(0.027 * exp(16.8958- 3795.17 / (z + 230.918)) * 5.73865- 101.3*w, 0), Eq(0.973* exp(13.7819- 2726.81/(z+217.572))* 1.001441 -101.3*(1-w) ,  0)], [w, z], [0.1, 75])
        #print(g1[i],g2[i], x1[i], x2[i],  y1[i], T[i])





    return x1, y1, T,g1,g2,Ge

def BublxPaltern(x1, P, Coeficientes, Coef1, Coef2, V1, V2):

    l1 = Coeficientes[0]
    l2 = Coeficientes[1]
    a12 = (V2 / V1) * math.exp(-l1 / (1.987 * 298.15))

    a21 = (V1 / V2) * math.exp(-l2 / (1.987 * 298.15))
    x1 = cortar(x1)
    n = len(x1)
    P= P*7.50062

    g1 = np.zeros(n)
    g2 = np.zeros(n)
    y1 = np.zeros(n)
    T = np.zeros(n)
    Ge = np.zeros(n)
    Ps1 = np.zeros(n)

    w, z = symbols('w, z')

    x2 = c2(x1)
    for i in range(n):
        g1[i] = math.exp(-math.log(x1[i] + a12 * x2[i]) + x2[i] * (a12 / (x1[i] + a12 * x2[i]) - a21 / (x2[i] + a21 * x1[i])))

        g2[i] = math.exp(-math.log(x2[i] + a21 * x1[i]) + x1[i] * (-a12/(x1[i]+a12*x2[i]) + a21/(x2[i]+a21*x1[i])))

        Ge[i] = (- x1[i] * math.log(x1[i] + (1 - x1[i]) * a12) - (1 - x1[i]) * math.log(1 - x1[i] + x1[i] * a21))

        y1[i], T[i] = nsolve([Eq(x1[i] *exp(Coef1[0] - Coef1[1] / (z+ Coef1[2])) * g1[i]- P*w, 0), Eq(x2[i] *exp(Coef2[0] - Coef2[1] / (z + Coef2[2])) * g2[i]- P*(1-w), 0)], [w, z], [0.5, 90])


        #y1, t = nsolve ([Eq(0.027 * exp(16.8958- 3795.17 / (z + 230.918)) * 5.73865- 101.3*w, 0), Eq(0.973* exp(13.7819- 2726.81/(z+217.572))* 1.001441 -101.3*(1-w) ,  0)], [w, z], [0.1, 75])
        #print(g1[i],g2[i], x1[i], x2[i],  y1[i], T[i])

    return x1, y1, T,g1,g2,Ge

def BublxPNRTL(x1, P, Parametros, Coef1, Coef2, V1, V2):

    a = Parametros[0]
    b12 = Parametros[1]
    b21 = Parametros[2]

    t12 = b12 / (1.987 * 298.15)
    t21 = b21 / (1.987 * 298.15)
    G12 = exp(- a * t12)
    G21 = exp(- a * t21)

    P = P * 7.50062
    x1 = cortar(x1)
    n = len(x1)

    g1 = np.zeros(n)
    g2 = np.zeros(n)
    Ge= np.zeros(n)
    y1 = np.zeros(n)
    T = np.zeros(n)
    Ps1 = np.zeros(n)
    w, z = symbols('w, z')

    x2 = c2(x1)
    for i in range(n):

        g1[i] = math.exp((x2[i]**2) * (t21 * (G21/(x1[i] + G21 * x2[i]) ) ** 2 +(t12 * G12/(x2[i] + G12 * x1[i])**2)))

        g2[i] = math.exp((x1[i]**2) * (t12 * (G12/(x2[i] + G12 * x1[i]) ) ** 2 +(t21 * G21/(x1[i] + G21 * x2[i])**2)))

        Ge[i] = x1[i] * math.log(g1[i]) + x2[i] * math.log(g2[i])

        y1[i], T[i] = nsolve([Eq(x1[i] * exp(Coef1[0] - Coef1[1] / (z + Coef1[2])) * g1[i]- P*w, 0), Eq(x2[i] * exp(Coef2[0] - Coef2[1] / (z + Coef2[2])) * g2[i]- P*(1-w), 0)], [w, z], [0.5, 77])
#DewxP(x1,101.3, [1054.01695409, 231.91745538], Coef, Coef2)
#x, gama1, gama2, gibbs = experimental(t, x1, y1, Coef, Coef2, 101.3)

    return x1, y1, T, g1, g2, Ge


def calc_parametros(x, param):
    n = len(x)
    primer_parametro = np.zeros(n)
    segundo_parametro = np.zeros(n)
    x2 = c2(x)
    for i in range(n):
        primer_parametro[i] = (x[i]*param[0])/(x[i]*param[0] + x2[i]*param[1])
        segundo_parametro[i] = (x2[i] * param[1]) / (x[i] * param[0] + x2[i] * param[1])

    return [primer_parametro, segundo_parametro]

def calc_eles(param_r, param_q, z):
    l1= (z/2)*(param_r[0]-param_q[0]) - (param_r[0]-1)
    l2 = (z / 2) * (param_r[1] - param_q[1]) - (param_r[1] - 1)

    return [l1, l2]

def valoresUNIQUAC(param_r, param_q, param_qprima, x):
    n = len(x)
    Ge_combinatoria = np.zeros(n)
    x2 = c2(x)

    phis = calc_parametros(x, param_r)
    thetas = calc_parametros(x, param_q)
    thetaprimas =calc_parametros(x, param_qprima)
    ls = calc_eles(param_r, param_q, 10)

    for i in range(n):
        Ge_combinatoria[i]=x[i]*math.log(phis[0][i]/x[i]) + x2[i]*math.log(phis[1][i]/x2[i]) +5*(x[i] * param_q[0] * log(thetas[0][i]/phis[0][i]) +x2[i] * param_q[1] * log(thetas[1][i]/phis[1][i])  )

    return Ge_combinatoria , thetaprimas, ls, thetas, phis


#print(valoresUNIQUAC([2.7799 ,0.92  ],[2.5129, 1.4   ],[0.89, 1.  ],[0.003 , 0.0123 ,0.0322 ,0.0697 ,0.139  ,0.231  ,0.311  ,0.412  ,0.545, 0.73   ,0.878 ]))

def BublxUNIQUAC(x1, P, Parametros, Coef1, Coef2, param_r, param_q, param_qprima):

    u12 = Parametros[0]
    u21 = Parametros[1]
    x1 = cortar(x1)

    Ge_combinatoria, thetaprimas, ls, thetas, phis = valoresUNIQUAC(param_r, param_q, param_qprima, x1)

    t12 = exp( -u12 / (1.987 * 298.15))
    t21 = exp(-u21 / (1.987 * 298.15))

    P = P * 7.50062
    n = len(x1)

    g1 = np.zeros(n)
    g2 = np.zeros(n)
    Ge= np.zeros(n)
    y1 = np.zeros(n)
    T = np.zeros(n)
    Ps1 = np.zeros(n)
    w, z = symbols('w, z')

    x2 = c2(x1)

    for i in range(n):

        g1[i] = math.exp(math.log(phis[0][i]/x1[i]) + 5 * param_q[0] * math.log(thetas[0][i]/phis[0][i]) + phis[1][i] * (ls[0]- (param_r[0]*ls[1] / param_r[1])) -
        param_qprima[0]* math.log(thetaprimas[0][i] + thetaprimas[1][i]*t21) + thetaprimas[1][i] * param_qprima[0]* (t21/(thetaprimas[0][i] + thetaprimas[1][i]* t21) - t12/(thetaprimas[1][i] + thetaprimas[0][i]* t12) ))

        g2[i] = math.exp(math.log(phis[1][i]/x2[i]) + 5 * param_q[1] * math.log(thetas[1][i]/phis[1][i]) + phis[0][i] * (ls[1]- (param_r[1]*ls[0] / param_r[0])) -
        param_qprima[1]* math.log(thetaprimas[1][i] + thetaprimas[0][i]*t12) + thetaprimas[0][i] * param_qprima[1]* (-t21/(thetaprimas[0][i] + thetaprimas[1][i]* t21) + t12/(thetaprimas[1][i] + thetaprimas[0][i]* t12) ))

        Ge[i] = x1[i] * math.log(g1[i]) + x2[i] * math.log(g2[i])

        y1[i], T[i] = nsolve([Eq(x1[i] * exp(Coef1[0] - Coef1[1] / (z + Coef1[2])) * g1[i]- P*w, 0), Eq(x2[i] * exp(Coef2[0] - Coef2[1] / (z + Coef2[2])) * g2[i]- P*(1-w), 0)], [w, z], [0.5, 77])
#DewxP(x1,101.3, [1054.01695409, 231.91745538], Coef, Coef2)
#x, gama1, gama2, gibbs = experimental(t, x1, y1, Coef, Coef2, 101.3)

    return x1, y1, T, g1, g2, Ge

