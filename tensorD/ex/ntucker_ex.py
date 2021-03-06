#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/26 PM11:01
# @Author  : Shiloh Leung
# @Site    :
# @File    : ntucker_ex.py
# @Software: PyCharm Community Edition

from tensorD.factorization.env import Environment
from tensorD.dataproc.provider import Provider
from tensorD.factorization.ntucker import NTUCKER_BCU
from tensorD.demo.DataGenerator import *
import sys


def ntucker_run(N1, N2, N3, gR, dR, time):
    # ntucker
    X = synthetic_data_tucker([N1, N2, N3], [gR, gR, gR], 0)
    data_provider = Provider()
    data_provider.full_tensor = lambda: X
    env = Environment(data_provider, summary_path='/tmp/ntucker_' + str(N1))
    ntucker = NTUCKER_BCU(env)
    args = NTUCKER_BCU.NTUCKER_Args(ranks=[dR, dR, dR], validation_internal=500, tol=1.0e-4)
    ntucker.build_model(args)
    print('\n\nNTucker with %dx%dx%d, gR=%d, dR=%d, time=%d' % (N1, N2, N3, gR, dR, time))
    hist = ntucker.train(10000)
    scale = str(N1) + '_' + str(gR) + '_' + str(dR)
    out_path = '/root/tensorD_f/data_out_tmp/python_out/ntucker_' + scale + '_' + str(time) + '.txt'
    with open(out_path, 'w') as out:
        for iter in hist:
            loss = iter[0]
            rel_res = iter[1]
            out.write('%.10f, %.10f\n' % (loss, rel_res))


if __name__ == '__main__':
    ntucker_run(N1=int(sys.argv[1]),
                N2=int(sys.argv[2]),
                N3=int(sys.argv[3]),
                gR=int(sys.argv[4]),
                dR=int(sys.argv[5]),
                time=int(sys.argv[6]))
