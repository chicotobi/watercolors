import plot_graph

from problems import COLORS, niveau
from model import step, get_steps, is_solved
from utils import print_state

all_states = []
all_transitions = []
all_flask_flask = {}
colx = len(COLORS) - 1 

def get_index(s):
  global all_states
  s = tuple(sorted(s))
  tmp = [i for (i,dct) in enumerate(all_states) if tuple(sorted(dct["state"]))==s]
  if len(tmp) == 1:
    return tmp[0]
  else:
    return -1

def get_pathlength(s):
  global all_states
  return all_states[get_index(s)]["path_length"]

def add_state(s,pl):
  global all_states
  all_states += [{"path_length":pl, "state":s}]

def add_flask_flask(sin,sout,ffrom,fto):
  global all_flask_flask
  idxin = get_index(sin)
  idxout = get_index(sout)
  all_flask_flask[(idxin,idxout)] = (ffrom,fto)

def update_tree(sin,sout,path_length,ffrom,fto):
  global all_states, all_transitions

  # Correct the transition
  idxin = get_index(sin)
  idxout = get_index(sout)

  # Remove the transition currently leading to idx
  all_transitions = [(i,j) for (i,j) in all_transitions if j != idxout]
  # Add the transition now leading faster to idx
  all_transitions += [(idxin,idxout)]
  add_flask_flask(sin,sout,ffrom,fto)

  # Iterate over all children states that have to be corrected
  new = [idxout]
  while True:
    for i in new:
      all_states[i]["path_length"] = path_length
    if len(new) == 0:
      break
    path_length += 1
    new = [j for (i,j) in all_transitions if i in new]


def add_transition(sin,sout):
  global all_transitions
  idxin = get_index(sin)
  idxout = get_index(sout)
  all_transitions += [(idxin,idxout)]


def replace_unknown_in_a_state(s, i0, j0, cidx, n):
  return tuple(f if i!=i0 else tuple(cidx if j0-n<j<=j0 else x for (j,x) in enumerate(f)) for (i,f) in enumerate(s))


def solve_optimal(sin,path_length=1,a=[]):
  if path_length < 5:
    print(path_length*" ",sin,"steps:",len(get_steps(sin)))
  for st in get_steps(sin):
    sout = step(sin,st[0],st[1])
    if get_index(sout) == -1:
      add_state(sout,path_length)
      add_transition(sin, sout)
      add_flask_flask(sin,sout,st[0],st[1])
      solve_optimal(sout,path_length+1,a+[st])
    elif path_length < get_pathlength(sout):
      update_tree(sin,sout,path_length,st[0],st[1])

def solve_fast(sin,a=[]):
  for st in get_steps(sin):
    sout = step(sin,st[0],st[1])
    if get_index(sout) == -1:
      add_state(sout,-1)
      if is_solved(sout):
        print(a+[st])
        return True
      if solve_fast(sout,a+[st]):
          return True
  return False

def replace_unknown_in_states(i0, j0, cidx, n):
  global all_states
  for k in range(len(all_states)):
    dct = all_states[k]
    s = dct["state"]
    s = replace_unknown_in_a_state(s, i0, j0, cidx, n)
    dct["state"] = s
    all_states[k] = dct

def solve_with_unknown(sidx,path_length=1,a=[]):
  global print_path
  steps = get_steps(all_states[sidx]["state"])
  for st in steps:
    print()
    if print_path:
      print(a)
    sin = all_states[sidx]["state"]
    print_state(sin)
    sout = step(sin,st[0],st[1])
    if get_index(sout) != -1:
        continue
    print("Please pour flask",st[0],"into",st[1])
    i0 = st[0]
    j0 = len(sout[i0])-1
    if j0 >= 0 and sout[i0][j0] == colx:
      while True:
        x = input("Enter the appearing color(s): ")
        if x!='':
          break
      cidx = dict(zip([i[0] for i in COLORS],range(len(COLORS))))[x[0]]
      replace_unknown_in_states(i0, j0, cidx, len(x))
      sout = replace_unknown_in_a_state(sout, i0, j0, cidx, len(x))
    sin = all_states[sidx]["state"]
    if get_index(sout) == -1:
      add_state(sout,path_length)
      add_transition(sin, sout)
      add_flask_flask(sin,sout,st[0],st[1])
      if is_solved(sout):
        return True
      sidx2 = get_index(sout)
      if solve_with_unknown(sidx2,path_length+1,a+[st]):
        return True
      print("Restart")
      print_path = True
    elif path_length < get_pathlength(sout):
      update_tree(sin,sout,path_length,st[0],st[1])
  return False

def solve(problem_id, fast = True, plot_full = True):
    global print_path,all_states, all_transitions, all_flask_flask
    s0, with_unknown = niveau(problem_id)
    all_states = [{"path_length":0,"state":s0}]
    print_path = False
        
    if with_unknown:
        if fast or plot_full:
            print("Problem has unknown tiles. 'fast' or 'plot_full' are not supported.")
        solve_with_unknown(0)
    else:
        if fast:
            if plot_full:
                print("Fast solution. 'plot_full' is not supported.")
            solve_fast(s0)
        else:
            solve_optimal(s0)
            numbered_states = list(enumerate(all_states))
            if plot_full:
                plot_graph.plot_full(numbered_states,all_transitions)
            else:
                plot_graph.plot_solution(numbered_states,all_transitions,all_flask_flask)