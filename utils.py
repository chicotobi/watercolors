from problems import COLORS

def print_state(s):
  print(' '.join(''.join(COLORS[i][0] for i in j) for j in s))