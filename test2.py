import matplotlib.pyplot as plt

import triangle as tr

face = tr.get_data('corridor')
t = tr.triangulate(face, 'p')

tr.compare(plt, face, t)
plt.show()