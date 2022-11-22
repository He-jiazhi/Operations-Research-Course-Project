# -*- coding:utf-8 -*-
"""
作者：Jiazhi He
日期：2021年12月22日
"""

import sympy as sp
from sympy import ordered, hessian
from sympy.utilities.lambdify import lambdify
from autograd import jacobian
import autograd.numpy as np


def f_test1(init):
    return 100*np.power(init[1]-np.power(init[0], 2), 2)+np.power(1-init[0], 2)+100*np.power(init[2]-np.power(init[1], 2), 2)


def f_test2(init):
    return 100*np.power(init[1]-np.power(init[0], 2), 2)+np.power(1-init[0], 2)


def f_test3(init):
    return 1+np.power(1-init[0], 2)


def f_test4(init):
    return 1+np.power(np.array([1])-np.sin(init[0]), 2)


def hessian_test1(vec):
    x_1, x_2, x_3 = sp.symbols('x_1, x_2, x_3')
    f = (1-x_1)**2 + 100*(x_2-x_1**2)**2+100*(x_3-x_2**2)**2
    v = list(ordered(f.free_symbols))
    hess = hessian(f, v)
    lam_f = lambdify(v, hess, 'numpy')
    return lam_f(vec[0], vec[1], vec[2])


def hessian_test2(vec):
    x_1, x_2 = sp.symbols('x_1, x_2')
    f = (1-x_1)**2+100*(x_2-x_1**2)**2
    v = list(ordered(f.free_symbols))
    hess = hessian(f, v)
    lam_f = lambdify(v, hess, 'numpy')
    return lam_f(vec[0], vec[1])


def hessian_test3(vec):
    x_1 = sp.symbols('x_1')
    f = 1+(1-x_1)**2
    v = list(ordered(f.free_symbols))
    hess = hessian(f, v)
    lam_f = lambdify(v, hess, 'numpy')
    return lam_f(vec[0])


def hessian_test4(vec):
    x_1 = sp.symbols('x_1')
    f = 1+(1-sp.sin(x_1))**2
    v = list(ordered(f.free_symbols))
    hess = hessian(f, v)
    lam_f = lambdify(v, hess, 'numpy')
    return lam_f(vec[0])


f_test = [f_test1, f_test2, f_test3, f_test4]
hessian_test = [hessian_test1, hessian_test2, hessian_test3, hessian_test4]
inp = [np.array([1.0001, 1.0001, 1.0001]), np.array([1.2, 1.2]), np.array([1.01]), np.array([2])]
f_str = ['(1-x1)^2+100*(x2-x1^2)^2+100*(x3-x2^2)^2', '(1-x1)^2+100*(x2-x1^2)^2', '1+(1-x1)^2', '1+(1-sin(x1))^2']


def newton(function, begin, hessianfunc, eps=0.000000001, rou=0.4, sigma=0.5):
    grad_f = jacobian(function)
    x = begin
    hess = hessianfunc(x)
    b = -grad_f(x).reshape([-1])
    d = -np.dot(np.linalg.inv(hess), -grad_f(x))
    term = 0
    while np.sum(np.power(b, 2)) > eps:
        if term % 1000 == 0:
            print('term:' + str(term))
        term += 1
        zero_grad = float(np.dot(-b, d))
        a = 1
        a1 = 0
        a2 = a
        alpha = (a1 + a2) / 2
        phi_1 = float(function(x))
        phi_1_star = zero_grad
        while True:
            phi = float(function(x + alpha * d))
            while phi > (function(x) + rou * alpha * zero_grad):
                if alpha < 0:
                    raise ValueError
                a2, alpha = alpha, a1 + 0.5 * np.power(a1 - alpha, 2) * phi_1_star / (
                            phi_1 - phi - (a1 - alpha) * phi_1_star)
                phi = float(function(x + alpha * d))
                if a1 == a2:
                    alpha = a1
                    break

            phi_star = float(np.dot(grad_f(x + alpha * d), d))
            if phi_star >= sigma * zero_grad:
                break
            else:
                a1, alpha = alpha, alpha - (a1 - alpha) * phi_star / (phi_1_star - phi_star)
                if alpha < a1:
                    alpha = (a1 + a2) / 2
                phi_1 = phi
                phi_1_star = phi_star
            if a1 == a2:
                alpha = a1
                break
        x_old = x
        x = x + alpha * d.reshape([-1])
        if term % 1000 == 0:
            print('x:' + str(x))
            print('f(x):' + str(function(x)))
        if np.sum(np.power(x - x_old, 2)) < 0.000000000000000001:
            return 'may be not convergent'
        hess = hessianfunc(x)
        b = -grad_f(x).reshape([-1])
        d = -np.dot(np.linalg.inv(hess), -grad_f(x))
    return x, function(x)


# for i in range(4):
print('function:' + f_str[0])
print('start:' + str(inp[0]))
print('f(start):' + str(f_test[0](inp[0])))
best = newton(f_test[0], inp[0], hessian_test1)
print('optimal point:' + str(best[0]))
print('f(optimal):' + str(best[1]))
