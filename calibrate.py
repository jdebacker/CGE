#import packages
import scipy.optimize as opt
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


def read_sam(sam):
    '''
    This function reads the SAM file and initializes variables using
    these data.

    Args:
        sam (DataFrame): DataFrame containing social and economic data

    Returns:
        model_data (dictionary): Data used in the model
    '''
    Sf0 = DataFrame(sam, index=['INV'], columns=['EXT']) #foreign saving
    Sp0 = DataFrame(sam, index=['INV'], columns=['HOH']) #private saving'
    Sg0 = DataFrame(sam, index=['INV'], columns=['GOV']) #government saving/budget balance

    Fsh0 = DataFrame(sam, index=['EXT'], columns=['HOH']) #repatriation of profits
    Kk0 = 10510 #capital stock
    Kf0 = 6414.35 #foreign-owned capital stock
    Kd0 = Kk0 - Kf0 #domestically-owned capital stock

    Td0 = DataFrame(sam, index=['DTX'], columns=['HOH']) #direct tax
    Trf0 = DataFrame(sam, index=['HOH'], columns=['GOV']) #transfers
    Tz0 = DataFrame(sam, index=['ACT'], columns=list(ind)) #production tax
    Tm0 = DataFrame(sam, index=['IDT'], columns=list(ind)) #import tariff

    F0 = DataFrame(sam, index=list(h), columns=list(ind)) #the h-th factor input by the i-th firm
    Ff0 = F0.sum(axis=1) #factor endowment of the h-th factor
    Y0 = F0.sum(axis=0) #composite factor (value added)
    X0 = DataFrame(sam, index=list(ind), columns=list(ind)) #intermediate input
    Xx0 = X0.sum(axis=0)#total intermediate input by the j-th sector
    Z0 = Y0 + Xx0 #output of the j-th good

    Xp0 = DataFrame(sam, index=list(ind), columns=['HOH']) #household consumption of the i-th good
    Xg0 = DataFrame(sam, index=list(ind), columns=['GOV']) #government consumption
    Xv0 = DataFrame(sam, index=list(ind), columns=['INV']) #investment demand
    E0 = DataFrame(sam, index=list(ind), columns=['EXT']) #exports
    E0 = E0['EXT']
    M0 = DataFrame(sam, index=['EXT'], columns=list(ind)) #imports
    M0 = M0.loc['EXT']

    tauz = Tz0/Z0 #production tax rate
    tauz = tauz.loc['ACT']
    taum = Tm0/M0 #import tariff rate
    taum = taum.loc['IDT']

    Q0 = Xp0['HOH'] + Xg0['GOV'] + Xv0['INV'] + X0.sum(axis=1) #domestic supply/Armington composite good
    D0 = (1 + tauz) * Z0 - E0 #domestic
    #D0 = D0.loc['ACT']

    Yy0 = Y0.sum()
    XXp0 = Xp0.sum()
    XXv0 = Xv0.sum()
    XXg0 = Xg0.sum()
    Mm0 = M0.sum()
    Ee0 = E0.sum()
    Gdp0 = XXp0 + XXv0 + XXg0 + Ee0 - Mm0

    g = XXv0/Kk0
    R0 = Ff0['CAP']/Kk0

    pWe = np.ones(len(ind)) #export price index
    pWe = Series(pWe, index=list(ind))
    pWm = np.ones(len(ind)) #import price index
    pWm = Series(pWm, index=list(ind))

    return model_data


def set_params():
    '''
    This function sets the values of parameters used in the model.

    Args:

    Returns:
        p (class): Class of parameters for use in CGE model.
    '''
    class parameters():

        def __init__(self):

            self.sigma = ([3, 1.2, 3, 3]) #elasticity of substitution
            self.sigma = Series(sigma, index=list(ind))
            self.eta = (sigma - 1) / sigma #substitution elasticity parameter

            self.psi = ([3, 1.2, 3, 3]) #elasticity of transformation
            self.psi = Series(psi, index=list(ind))
            self.phi = (psi + 1) / psi #transformation elasticity parameter

            self.alpha = Xp0 / XXp0 #share parameter in utility function
            self.alpha = alpha ['HOH']
            self.beta = F0 / Y0 #share parameter in production function
            self.temp = F0 ** beta
            self.b = Y0 / temp.prod(axis=0)#scale parameter in production function

            self.ax = X0 / Z0 #intermediate input requirement coefficient
            self.ay = Y0 / Z0 #composite factor input requirement coefficient
            self.mu = Xg0 / XXg0 #government consumption share
            self.mu = mu['GOV']
            self.lam = Xv0 / XXv0 #investment demand share
            self.lam = lam['INV']

            #share parameter in Armington function
            self.deltam = ((1 + taum) * M0 ** (1 - eta) /
                           ((1 + taum) * M0 ** (1 - eta) + D0 ** (1 - eta)))
            self.deltad = (D0 ** (1 - eta) /
                           ((1 + taum) * M0 ** (1 - eta) + D0 ** (1 - eta)))

            #scale parameter in Armington function
            self.gamma = Q0 / ( deltam * M0 ** eta + deltad *D0 ** eta ) ** (1 / eta)

            #share parameter in transformation function
            self.xie = E0 ** (1 - phi) / (E0 ** (1 - phi) + D0 ** (1 - phi) )
            self.xie = xie.iloc[0]
            self.xid = D0 ** (1 - phi) / (E0 ** (1 - phi) + D0 ** (1 - phi) )
            self.xid = xid.iloc[0]

            #scale parameter in transformation function
            self.theta = Z0 / (xie * E0 ** phi + xid * D0 ** phi) ** (1 / phi)
            self.theta = theta.iloc[0]

            self.ssp = Sp0.values / (Ff0.sum() - Fsh0.values + Trf0.values) #average propensity to save
            self.ssp = np.asscalar(ssp)
            self.taud = Td0.values / Ff0.sum() #direct tax rate
            self.taud = np.asscalar(taud)
            self.tautr = Trf0.values / Ff0['LAB'] #transfer rate
            self.tautr = np.asscalar(tautr)
            self.ginc = Td0 + Tz0.sum() + Tm0.sum()   #government revenue
            self.hinc = Ff0.sum() #household income

    return parameters