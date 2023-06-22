# colors are integers - 0,1,2,3 ...
# number of colors ncol
# number of flasks is nflask = ncol + 2
# height is four
#
# state is tuple of tuples
#  2  1  1 _ _
#  0  2  2 _ _
# -1 -1  2 _ _
# -1 -1 -1 _ _
#
# -1 is unknown

from problems import MAX_HEIGHT

def is_solved(state):
  for flask in state:
    if len(flask) == MAX_HEIGHT:
      c0 = flask[0]
      for c in flask:
        if c != c0:
          return False
    elif len(flask) > 0:
      return False
  return True


def is_unicolor(f):
  return len(set(f))<2


def get_amount_of_top_color(s):
  n = 1
  if len(s)>1:
    while n < len(s) and s[-1-n] == s[-1]:
      n += 1
  return n


def step(state,i,j):

  assert i!=j

  si = state[i]
  sj = state[j]

  assert len(si)>0
  c = si[-1]

  if len(sj)>0:
    assert si[-1] == sj[-1]

  # Unicolor amount in top of si
  n = 1
  while n < len(si) and si[-n-1] == c:
    n += 1

  # Space in sj
  n_sj = MAX_HEIGHT - len(sj)

  n_transfer = min(n,n_sj)

  si = si[0:(len(si)-n_transfer)]
  sj = sj + n_transfer * (c,)

  s_new = ()
  for k in range(len(state)):
    if k == i:
      f = si
    elif k == j:
      f = sj
    else:
      f = state[k]
    s_new = s_new + (f,)
  return s_new


def get_steps(state):
  steps = []
  n_flask = len(state)
  for i in range(n_flask):
    if len(state[i]) > 0:
      ci = state[i][-1]
      n = get_amount_of_top_color(state[i])
      for j in range(n_flask):
        if i != j:
          if len(state[j]) == 0:
            if not is_unicolor(state[i]):
              steps += [(i,j)]
          elif len(state[j]) <= MAX_HEIGHT - n:
            cj = state[j][-1]
            if ci == cj:
              steps += [(i,j)]
  return steps