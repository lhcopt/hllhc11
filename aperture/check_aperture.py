#!/usr/bin/python

import sys
import gzip

eps=-0.1
eps=+0.0

def check_aperture(fn):
  print "Checking %s" % fn
  if fn.endswith('.gz'):
    fh=gzip.open(fn)
  else:
    fh=file(fn)

  idx={}   #associate a column name to a column index
  labels=['NAME', 'BETX', 'BETY', 'DX', 'DY', 'X', 'Y', 'N1']

  out=[]

  for l in fh:
    if l.startswith('*'):
      label_line=l.split()
      for lb in labels:
        idx[lb]=label_line.index(lb)-1
      print ('  %-15s'+'  %-5s'*8) % tuple(labels+['DN1'])
    elif l.startswith(' '):
      data=l.split()
      name,betx,bety,dx,dy,x,y,n1=[ eval(data[idx[lb]]) for lb in labels]
      if name.startswith('M'):
        if  name.startswith('MSD') and n1<7.5-eps:
          out.append([2,name,betx,bety,dx,x,y,n1,n1-7.5])
        elif 'MQW' in name or 'MQTLH' in name or '6R3' in name or '6L3' in name:
          if n1<5.5-eps:
            out.append([4,name,betx,bety,dx,dy,x,y,n1])
        elif betx>bety and n1<7-eps:
          out.append([0,name,betx,bety,dx,dy,x,y,n1,n1-7])
        elif betx<bety and n1<6.7-eps:
          out.append([1,name,betx,bety,dx,dy,x,y,n1,n1-6.7])
      elif  name.startswith('TCT') and  n1<6.5-eps:
          out.append([3,name,betx,bety,dx,dy,x,y,n1,n1-6.5])

  prefix='H V S C 3'.split()
  out.sort()

  for t,name,betx,bety,dx,dy,x,y,n1,dn1 in out:
    print ('%s %-15s'+'%7.2f'*8) % (prefix[t],name,betx,bety,dx,dy,x,y,n1,dn1)


alltblinj="""
  temp/ap_ir1b1inj.tfs
  temp/ap_ir1b2inj.tfs
  temp/ap_ir2b1inj.tfs
  temp/ap_ir2b2inj.tfs
  temp/ap_ir3b1inj.tfs
  temp/ap_ir3b2inj.tfs
  temp/ap_ir4b1inj.tfs
  temp/ap_ir4b2inj.tfs
  temp/ap_ir5b1inj.tfs
  temp/ap_ir5b2inj.tfs
  temp/ap_ir6b1inj.tfs
  temp/ap_ir6b2inj.tfs
  temp/ap_ir7b1inj.tfs
  temp/ap_ir7b2inj.tfs
  temp/ap_ir8b1inj.tfs
  temp/ap_ir8b2inj.tfs
""".split()

try:
  eps=float(sys.argv[2])
except:
  pass

if sys.argv[1]=='inj':
  for tbl in alltblinj:
    check_aperture(tbl)
else:
  check_aperture(sys.argv[1])
