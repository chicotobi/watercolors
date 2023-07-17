import matplotlib.pyplot as plt
import matplotlib.patches
import graphviz

from model import is_solved
from problems import MAX_HEIGHT, COLORS

def get_color(char):
  col = COLORS[char]
  if col == 'egrey':
    col = 'grey'
  if col == 'hblue':
    col = '#ADD8E6'
  if col == 'muddygreen':
    col = '#657220'
  if col == 'violet':
    col = '#893AFF'
  if col == 'wbrown':
    col = '#654321'
  return col

def plot_state(idx,dct):
  s = dct["state"]
  fig, ax = plt.subplots()
  ax.set_xlim(0,15*len(s))
  ax.set_ylim(-1,41)
  ax.set_axis_off()
  fig.tight_layout()

  for (i,f) in enumerate(s):
    for j in range(MAX_HEIGHT):
      if j < len(f):
        s = f[j]
        r = matplotlib.patches.Rectangle((i*15, j*10), 10, 10,facecolor=get_color(f[j]),edgecolor="k")
      else:
        r = matplotlib.patches.Rectangle((i*15, j*10), 10, 10,fill=None,edgecolor="k")
      ax.add_patch(r)
  plt.savefig("img/tmp"+str(idx)+".png")
  plt.close()

def plot_full(states,transitions):
  G = graphviz.Digraph('example')
  for (i,dct) in states:
    plot_state(i,dct)
    G.node(str(i),label=str(dct["path_length"]),fixedsize="true",image="img/tmp"+str(i)+".png",imagescale="True")
  for x,y in transitions:
    G.edge(str(x),str(y))
  G.view()
  
def plot_solution(states,transitions,flask_flask):
  i0 = [i for (i,x) in states if is_solved(x["state"])][0]
  states_solution = [states[i0]]
  transitions_solution = []
  while i0 != 0:
    i1 = [i for (i,j) in transitions if j == i0][0]
    transitions_solution += [(i1,i0)]
    states_solution += [states[i1]]
    i0 = i1   
  
  G = graphviz.Digraph('example')
  for (i,dct) in states_solution:
    plot_state(i,dct)
    G.node(str(i),label=str(dct["path_length"]),fixedsize="true",image="img/tmp"+str(i)+".png",imagescale="True")
  for x,y in transitions_solution:
    ffrom, fto = flask_flask[(x,y)]
    lbl = str(ffrom)+"->"+str(fto)    
    G.edge(str(x),str(y),label=lbl)
  G.view()
  