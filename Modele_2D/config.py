import sys
from Substitut import *

lower = 1600.
seuil_Q_1=3000.
seuil_Q_2=6000.
upper = 9900.

corner_default = ([17.,1600.],[45.,9900.])
corner_gamme0 = ([17.,1600.],[45.,seuil_Q_1])
corner_gamme1 = ([17.,seuil_Q_1],[45.,seuil_Q_2])
corner_gamme2 = ([17.,seuil_Q_2],[45.,9900.])

degree_default = 6*0+4
# degree_default = 6
nb_pts_generation_distrib = 10000
list_x=np.array([22., 36., 62.])

### Parametres d'affichage
maxSizeScatter = 2000.
nPtsRespSurf = 20
dpi_plot = 200