import os
import numpy as np
import matlab.engine

eng = matlab.engine.start_matlab()
img_dir = '../../data/lowlight/enhance/'
vars = {'dehz': [], 'dslr': [], 'enlighten_gan': [], 'fusion1': [],
        'kind_pp': [], 'lime': [], 'zero_dce': []}
ents = {'dehz': [], 'dslr': [], 'enlighten_gan': [], 'fusion1': [],
        'kind_pp': [], 'lime': [], 'zero_dce': []}
cons = {'dehz': [], 'dslr': [], 'enlighten_gan': [], 'fusion1': [],
        'kind_pp': [], 'lime': [], 'zero_dce': []}
mgs = {'dehz': [], 'dslr': [], 'enlighten_gan': [], 'fusion1': [],
        'kind_pp': [], 'lime': [], 'zero_dce': []}
smds = {'dehz': [], 'dslr': [], 'enlighten_gan': [], 'fusion1': [],
        'kind_pp': [], 'lime': [], 'zero_dce': []}


def iqa():
    for file in os.listdir(img_dir):
        path = img_dir + file
        print(file)
        if file.find('dehz') != -1:
            vars['dehz'].append(eng.Variance(path))
            ents['dehz'].append(eng.Entropy(path))
            cons['dehz'].append(eng.Con_(path))
            mgs['dehz'].append(eng.MeanGradient(path))
            smds['dehz'].append(eng.SMD(path))
        elif file.find('dslr') != -1:
            vars['dslr'].append(eng.Variance(path))
            ents['dslr'].append(eng.Entropy(path))
            cons['dslr'].append(eng.Con_(path))
            mgs['dslr'].append(eng.MeanGradient(path))
            smds['dslr'].append(eng.SMD(path))
        elif file.find('enlighten_gan') != -1:
            vars['enlighten_gan'].append(eng.Variance(path))
            ents['enlighten_gan'].append(eng.Entropy(path))
            cons['enlighten_gan'].append(eng.Con_(path))
            mgs['enlighten_gan'].append(eng.MeanGradient(path))
            smds['enlighten_gan'].append(eng.SMD(path))
        elif file.find('fusion1') != -1:
            vars['fusion1'].append(eng.Variance(path))
            ents['fusion1'].append(eng.Entropy(path))
            cons['fusion1'].append(eng.Con_(path))
            mgs['fusion1'].append(eng.MeanGradient(path))
            smds['fusion1'].append(eng.SMD(path))
        elif file.find('kind_pp') != -1:
            vars['kind_pp'].append(eng.Variance(path))
            ents['kind_pp'].append(eng.Entropy(path))
            cons['kind_pp'].append(eng.Con_(path))
            mgs['kind_pp'].append(eng.MeanGradient(path))
            smds['kind_pp'].append(eng.SMD(path))
        elif file.find('lime') != -1:
            vars['lime'].append(eng.Variance(path))
            ents['lime'].append(eng.Entropy(path))
            cons['lime'].append(eng.Con_(path))
            mgs['lime'].append(eng.MeanGradient(path))
            smds['lime'].append(eng.SMD(path))
        elif file.find('zero_dce') != -1:
            vars['zero_dce'].append(eng.Variance(path))
            ents['zero_dce'].append(eng.Entropy(path))
            cons['zero_dce'].append(eng.Con_(path))
            mgs['zero_dce'].append(eng.MeanGradient(path))
            smds['zero_dce'].append(eng.SMD(path))
    # print(vars)
    for key in vars.keys():
        print(key, np.mean(vars[key]), np.mean(ents[key]), np.mean(cons[key]), np.mean(mgs[key]), np.mean(smds[key]))

iqa()