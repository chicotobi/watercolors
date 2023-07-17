MAX_HEIGHT = 4
COLORS = ['blue','orange','red','green','pink','egrey','hblue','violet','muddygreen','darkgreen','wbrown','yellow','x']

from collections import Counter

def niveau(n):
  x = None
  empty_flasks = 2
  if n == 1:
    x = 'ooo o'
    empty_flasks = 0
  if n == 2:
    x = 'bobo obob'
    empty_flasks = 1
  if n == 3:
    x = 'borb oorb rbor'
  if n == 4:
    x = 'broo brbr obro'
  if n == 5:
    x = 'xxxp xxxp xxxr xxxb xxxb'
  if n == 6:
    x = 'rggg orpg poro bpop bbbr'
  if n == 7:
    x = 'goro bbro ppbo gprb grgp'
  if n == 8:
    x = 'xxxb xxxo xxxr xxxp xxxo'
  if n == 9:
    x = 'prbp rggo roop prgb gobb'
  if n == 10:
    x = 'pbgb oepr bhhg poog eegr brhh rpoe'
  if n == 11:
    x = 'xxxh xxxh xxxo xxxo xxxe xxxr xxxg'
  if n == 12:
    x = 'bpgg obpb borg ogrp rorp'
  if n == 13:
    x = 'bpgr oggh peor grbh hpeh pobe erbo'
  if n == 15:
    x = 'bggo pbrp pbpo rrob ogrg'
  if n == 31:
    x = 'bgpv hvmb bego pooh errp bomg grvh emrm phev'
  if n == 33:
    x = 'rggr hbop eepb hgho gohb peer pbor'
  if n == 74:
    x = 'xxxh xxxo xxxp xxxb xxxr xxxp xxxr xxxo xxxb'
  if n == 113:
    x = 'xxxy xxxm xxxb xxxe xxxm xxxo xxxd xxxg xxxm xxxw xxxe xxxh'
  if n == 114:
    x = 'rvgb mrmp vooh ervb hhpg vbop empg brgo emeh'
  if n == 115:
    x = 'wwro wppm bmgv ower mgbr vghv mdrh eyhy oeyd oyrg vbde pphd'
  if n == 119:
    x = 'xxxo xxxp xxxr xxxy xxxh xxxg xxxb xxxo xxxw xxxd xxxe xxxm'
  if n == 121:
    x = 'ydmw vrwd veop ermh ebdr hemg pvpy gvyp dooh bwgb gmry whob'
  if n == 122:
    x = 'xxxg xxxo xxxb xxxv xxxo xxxm xxxh xxxb xxxp'
  if n == 128:
    x = 'xxxm xxxm xxxo xxxb xxxr xxxb xxxp xxxb xxxh'
  if n == 129:
    x = 'dprv dorm odwe pyvp eobm bmyh hbgw hrbe wogv mghp dyye vgrw'

  if x is None:
      raise ValueError(n)

  c = dict(zip([i[0] for i in COLORS],range(len(COLORS))))
  with_unknown = 'x' in x
  
  # Consistency check
  if not with_unknown:
      dct = dict(Counter([i for i in x if i!=' ']))
      test = [(k,v) for (k,v) in dct.items() if v!=4]
      if len(test) > 0:
          print(dct)
          raise ValueError(x)
  d = tuple(tuple(c[j] for j in tuple(i)) for i in x.split(' ')) + ((),) * empty_flasks
  
  return d, with_unknown

