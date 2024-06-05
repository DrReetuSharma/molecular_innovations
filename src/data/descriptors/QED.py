# Calculating SMARTS, descriptors and weight for the molecules
#__all__ = ['weights_max', 'weights_mean', 'weights_none', 'default']


# RDKit
from rdkit.Chem import Lipinski, MolSurf, Crippen
from rdkit.Chem import rdMolDescriptors as rdmd
from rdkit import Chem

# General
from copy import deepcopy
from math import exp, log

#
AliphaticRings = Chem.MolFromSmarts('[$([A;R][!a])]')

#
AcceptorSmarts = [
  '[oH0;X2]',
  '[OH1;X2;v2]',
  '[OH0;X2;v2]',
  '[OH0;X1;v2]',
  '[O-;X1]',
  '[SH0;X2;v2]',
  '[SH0;X1;v2]',
  '[S-;X1]',
  '[nH0;X2]',
  '[NH0;X1;v3]',
  '[$([N;+0;X3;v3]);!$(N[C,S]=O)]'
  ]
Acceptors = []
for hba in AcceptorSmarts:
  Acceptors.append(Chem.MolFromSmarts(hba))

#
StructuralAlertSmarts = [
  '*1[O,S,N]*1',
  '[S,C](=[O,S])[F,Br,Cl,I]',
  '[CX4][Cl,Br,I]',
  '[C,c]S(=O)(=O)O[C,c]',
  '[$([CH]),$(CC)]#CC(=O)[C,c]',
  '[$([CH]),$(CC)]#CC(=O)O[C,c]',
  'n[OH]',
  '[$([CH]),$(CC)]#CS(=O)(=O)[C,c]',
  'C=C(C=O)C=O',
  'n1c([F,Cl,Br,I])cccc1',
  '[CH1](=O)',
  '[O,o][O,o]',
  '[C;!R]=[N;!R]',
  '[N!R]=[N!R]',
  '[#6](=O)[#6](=O)',
  '[S,s][S,s]',
  '[N,n][NH2]',
  'C(=O)N[NH2]',
  '[C,c]=S',
  '[$([CH2]),$([CH][CX4]),$(C([CX4])[CX4])]=[$([CH2]),$([CH][CX4]),$(C([CX4])[CX4])]',
  'C1(=[O,N])C=CC(=[O,N])C=C1',
  'C1(=[O,N])C(=[O,N])C=CC=C1',
  'a21aa3a(aa1aaaa2)aaaa3',
  'a31a(a2a(aa1)aaaa2)aaaa3',
  'a1aa2a3a(a1)A=AA=A3=AA=A2',
  'c1cc([NH2])ccc1',
  '[Hg,Fe,As,Sb,Zn,Se,se,Te,B,Si,Na,Ca,Ge,Ag,Mg,K,Ba,Sr,Be,Ti,Mo,Mn,Ru,Pd,Ni,Cu,Au,Cd,Al,Ga,Sn,Rh,Tl,Bi,Nb,Li,Pb,Hf,Ho]',
  'I',
  'OS(=O)(=O)[O-]',
  '[N+](=O)[O-]',
  'C(=O)N[OH]',
  'C1NC(=O)NC(=O)1',
  '[SH]',
  '[S-]',
  'c1ccc([Cl,Br,I,F])c([Cl,Br,I,F])c1[Cl,Br,I,F]',
  'c1cc([Cl,Br,I,F])cc([Cl,Br,I,F])c1[Cl,Br,I,F]',
  '[CR1]1[CR1][CR1][CR1][CR1][CR1][CR1]1',
  '[CR1]1[CR1][CR1]cc[CR1][CR1]1',
  '[CR2]1[CR2][CR2][CR2][CR2][CR2][CR2][CR2]1',
  '[CR2]1[CR2][CR2]cc[CR2][CR2][CR2]1',
  '[CH2R2]1N[CH2R2][CH2R2][CH2R2][CH2R2][CH2R2]1',
  '[CH2R2]1N[CH2R2][CH2R2][CH2R2][CH2R2][CH2R2][CH2R2]1',
  'C#C',
  '[OR2,NR2]@[CR2]@[CR2]@[OR2,NR2]@[CR2]@[CR2]@[OR2,NR2]',
  '[$([N+R]),$([n+R]),$([N+]=C)][O-]',
  '[C,c]=N[OH]',
  '[C,c]=NOC=O',
  '[C,c](=O)[CX4,CR0X3,O][C,c](=O)',
  'c1ccc2c(c1)ccc(=O)o2',
  '[O+,o+,S+,s+]',
  'N=C=O',
  '[NX3,NX4][F,Cl,Br,I]',
  'c1ccccc1OC(=O)[#6]',
  '[CR0]=[CR0][CR0]=[CR0]',
  '[C+,c+,C-,c-]',
  'N=[N+]=[N-]',
  'C12C(NC(N1)=O)CSC2',
  'c1c([OH])c([OH,NH2,NH])ccc1',
  'P',
  '[N,O,S]C#N',
  'C=C=O',
  '[Si][F,Cl,Br,I]',
  '[SX2]O',
  '[SiR0,CR0](c1ccccc1)(c2ccccc2)(c3ccccc3)',
  'O1CCCCC1OC2CCC3CCCCC3C2',
  'N=[CR0][N,n,O,S]',
  '[cR2]1[cR2][cR2]([Nv3X3,Nv4X4])[cR2][cR2][cR2]1[cR2]2[cR2][cR2][cR2]([Nv3X3,Nv4X4])[cR2][cR2]2',
  'C=[C!r]C#N',
  '[cR2]1[cR2]c([N+0X3R0,nX3R0])c([N+0X3R0,nX3R0])[cR2][cR2]1',
  '[cR2]1[cR2]c([N+0X3R0,nX3R0])[cR2]c([N+0X3R0,nX3R0])[cR2]1',
  '[cR2]1[cR2]c([N+0X3R0,nX3R0])[cR2][cR2]c1([N+0X3R0,nX3R0])',
  '[OH]c1ccc([OH,NH2,NH])cc1',
  'c1ccccc1OC(=O)O',
  '[SX2H0][N]',
  'c12ccccc1(SC(S)=N2)',
  'c12ccccc1(SC(=S)N2)',
  'c1nnnn1C=O',
  's1c(S)nnc1NC=O',
  'S1C=CSC1=S',
  'C(=O)Onnn',
  'OS(=O)(=O)C(F)(F)F',
  'N#CC[OH]',
  'N#CC(=O)',
  'S(=O)(=O)C#N',
  'N[CH2]C#N',
  'C1(=O)NCC1',
  'S(=O)(=O)[O-,OH]',
  'NC[F,Cl,Br,I]',
  'C=[C!r]O',
  '[NX2+0]=[O+0]',
  '[OR0,NR0][OR0,NR0]',
  'C(=O)O[C,H1].C(=O)O[C,H1].C(=O)O[C,H1]',
  '[CX2R0][NX3R0]',
  'c1ccccc1[C;!R]=[C;!R]c2ccccc2',
  '[NX3R0,NX4R0,OR0,SX2R0][CX4][NX3R0,NX4R0,OR0,SX2R0]',
  '[s,S,c,C,n,N,o,O]~[n+,N+](~[s,S,c,C,n,N,o,O])(~[s,S,c,C,n,N,o,O])~[s,S,c,C,n,N,o,O]',
  '[s,S,c,C,n,N,o,O]~[nX3+,NX3+](~[s,S,c,C,n,N])~[s,S,c,C,n,N]',
  '[*]=[N+]=[*]',
  '[SX3](=O)[O-,OH]',
  'N#N',
  'F.F.F.F',
  '[R0;D2][R0;D2][R0;D2][R0;D2]',
  '[cR,CR]~C(=O)NC(=O)~[cR,CR]',
  'C=!@CC=[O,S]',
  '[#6,#8,#16][C,c](=O)O[C,c]',
  'c[C;R0](=[O,S])[C,c]',
  'c[SX2][C;!R]',
  'C=C=C',
  'c1nc([F,Cl,Br,I,S])ncc1',
  'c1ncnc([F,Cl,Br,I,S])c1',
  'c1nc(c2c(n1)nc(n2)[F,Cl,Br,I])',
  '[C,c]S(=O)(=O)c1ccc(cc1)F',
  '[15N]',
  '[13C]',
  '[18O]',
  '[34S]'
  ]
StructuralAlerts = []
for smarts in StructuralAlertSmarts:
  StructuralAlerts.append(Chem.MolFromSmarts(smarts))

# ADS parameters for the 8 molecular properties: [row][column]
#   rows[8]:   MW, ALOGP, HBA, HBD, PSA, ROTB, AROM, ALERTS
#   columns[7]: A, B, C, D, E, F, DMAX
pads = [  [2.817065973, 392.5754953, 290.7489764, 2.419764353, 49.22325677, 65.37051707, 104.9805561],
      [3.172690585, 137.8624751, 2.534937431, 4.581497897, 0.822739154, 0.576295591, 131.3186604],
      [2.948620388, 160.4605972, 3.615294657, 4.435986202, 0.290141953, 1.300669958, 148.7763046],
      [1.618662227, 1010.051101, 0.985094388, 0.000000001, 0.713820843, 0.920922555, 258.1632616],
      [1.876861559, 125.2232657, 62.90773554, 87.83366614, 12.01999824, 28.51324732, 104.5686167],
      [0.010000000, 272.4121427, 2.558379970, 1.565547684, 1.271567166, 2.758063707, 105.4420403],
      [3.217788970, 957.7374108, 2.274627939, 0.000000001, 1.317690384, 0.375760881, 312.3372610],
      [0.010000000, 1199.094025, -0.09002883, 0.000000001, 0.185904477, 0.875193782, 417.7253140]    ]


def ads(x, a, b, c, d, e, f, dmax): #pylint: disable=R0913
  """ ADS function """
  return ((a + (b / (1 + exp(-1 * (x - c + d / 2) / e)) * (1 - 1 / (1 + exp(-1 * (x - c - d / 2) / f))))) / dmax)


def properties(mol):
  """
  Calculates the properties that are required to calculate the QED descriptor.
  """
  matches = []
  if (mol is None):
    raise TypeError('You need to provide a mol argument.')
  x = [0] * 8
  x[0] = rdmd._CalcMolWt(mol)                        # MW 
  x[1] = Crippen.MolLogP(mol)                        # ALOGP
  for hbaPattern in Acceptors:                            # HBA
    if (mol.HasSubstructMatch(hbaPattern)):
      matches = mol.GetSubstructMatches(hbaPattern)
      x[2] += len(matches)
  x[3] = Lipinski.NumHDonors(mol)               # HBD
  x[4] = MolSurf.TPSA(mol)                        # PSA
  x[5] = Lipinski.NumRotatableBonds(mol)         # ROTB
  x[6] = Chem.GetSSSR(Chem.DeleteSubstructs(deepcopy(mol), AliphaticRings))  # AROM
  for alert in StructuralAlerts:                        # ALERTS
    if (mol.HasSubstructMatch(alert)): x[7] += 1
  return x


def qed(m=None,w=(0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95),
        p=None):
  """ Calculate the weighted sum of ADS mapped properties

  some examples from the QED paper, reference values from Peter G's original implementation
  >>> m = Chem.MolFromSmiles('N=C(CCSCc1csc(N=C(N)N)n1)NS(N)(=O)=O')
  >>> qed(m)
  0.241...
  >>> m = Chem.MolFromSmiles('CNC(=NCCSCc1nc[nH]c1C)NC#N')
  >>> qed(m)
  0.217...
  >>> m = Chem.MolFromSmiles('CCCCCNC(=N)NN=Cc1c[nH]c2ccc(CO)cc12')
  >>> qed(m)
  0.212...
  >>> asdf
  """
  if p is None:
      p = properties(m)
  d = [0.00] * 8
  for i in range(0, 8):
    d[i] = ads(p[i], pads[i][0], pads[i][1], pads[i][2], pads[i][3], pads[i][4], pads[i][5], pads[i][6])
  t = 0.0
  for i in range(0, 8):
    t += w[i] * log(d[i])
  return (exp(t / sum(w)))
  
  
def weights_max(mol):
  """
  Calculates the QED descriptor using maximal descriptor weights.
  """
  props = properties(mol)
  return qed(mol,w=[0.50, 0.25, 0.00, 0.50, 0.00, 0.50, 0.25, 1.00])


def weights_mean(mol):
  """
  Calculates the QED descriptor using average descriptor weights.
  """
  props = properties(mol)
  return qed(mol,w=[0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95])

def weights_none(mol):
  """
  Calculates the QED descriptor using unit weights.
  """
  return qed(mol,w=[1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00])


def default(mol):
  """
  Calculates the QED descriptor using average descriptor weights.
  """
  return weights_mean(mol)



#------------------------------------
#
#  doctest boilerplate
#
def _test():
  import doctest,sys
  return doctest.testmod(sys.modules["__main__"],
                         optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE)

if __name__=='__main__':
    _test()
