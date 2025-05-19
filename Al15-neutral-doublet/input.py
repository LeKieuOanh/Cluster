import numpy
from pyscf import gto, scf, dft, mp, cc
from pyscf.mp import uobmp2_mom_conv, dfuobmp2_mom_conv, uhf_mom
from pyscf.mp import  mp2, ump2
from pyscf.tools import molden
import os
from functools import reduce


mol = gto.Mole()
geom = os.environ.get('geom_txt')
mol.atom = geom
mol.basis = os.environ.get('basis', 'cc-pvdz')
mol.unit = 'A'
mol.charge = int(os.environ.get('charge', 0))
mol.spin = int(os.environ.get('spin', 0))
mol.verbose = 4
mol.build()

#################### Ground state using density fitting
### Hartree-Fock
a  = scf.UHF(mol).density_fit()
a.kernel()

### Ground state OBMP2 calculation
ob = dfuobmp2_mom_conv.DFUOBMP2(a)
ob.second_order = True
ob.thresh = 10e-6
ob.css = 1
ob.cos = 1
e_obmp2g = ob.kernel()

### Ground state O2BMP2 calculation
ob = dfuobmp2_mom_conv.DFUOBMP2(a)
ob.second_order = True
ob.thresh = 10e-6
ob.css = 0                             
ob.cos = 1.2                             
e_o2bmp2g = ob.kernel()  

#################### Ground state NOT using density fitting
### Hartree-Fock
a  = scf.UHF(mol)
a.kernel()

### Ground state OBMP2 calculation
ob = uobmp2_mom_conv.UOBMP2(a)
ob.second_order = True
ob.thresh = 10e-6
ob.css = 1
ob.cos = 1
#e_obmp2g = ob.kernel()

### Ground state O2BMP2 calculation
ob = uobmp2_mom_conv.UOBMP2(a)
ob.second_order = True
ob.thresh = 10e-6
ob.css = 0
ob.cos = 1.2   ## the cos can be vary ...                        	 
#e_o2bmp2g = ob.kernel()


## Results from density-fitting approximate with non-using density fitting 
## check results between df and non-df with small molecules before running the important molecules
