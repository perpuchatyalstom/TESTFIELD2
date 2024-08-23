from constants import *

def number2unit(inp,unit='V'):
    #unit=unit.upper()
    inp=float(inp)
    convAsc=['f','p','n','u','m','k','M','G','T','P','%']
    convNum=[1.0e-15,1e-12,1e-9,1e-6,1e-3,1e3,1e6,1e9,1e12,1e15]
    if abs(inp)>=1 and abs(inp)<1000: return str(inp) + unit
    ln=len(convNum)
    i=0
    while True:
        if inp==0:
            return '0'+ unit
        if abs(inp*convNum[i]) >= 1:
            res = str(inp*convNum[i]) + convAsc[ln-1-i] + unit
            return res
        i=i+1
        if i > ln-1:
            return str(inp*convNum[ln-1]) + convAsc[0] + unit
            break
    return res

def unit2number(inp):
    convAsc=['f','p','n','u','m','c','k','M','G','T','P','%']
    convNum=[1e-15,1e-12,1e-9,1e-6,1e-3,1e-2,1e3,1e6,1e9,1e12,1e15]
    if not isinstance(inp,(str)):
        return float(inp)  
    res=''
    mult=''
    for char in inp:
        if char.isalpha():
            mult=char
            break
        else:
            res=res+char
    if mult in convAsc:
        id=convAsc.index(mult)
        mult=convNum[id]
    else:
        mult=1
    res=float(res)*mult

    return res

def formatUnit(inp,digits):
    res=''
    unit=''
    for char in inp:
        if char.isalpha():
            unit+=char
        else:
            res+=char
    res = "%.*f" % (digits,float(res))

    # print res
    # print unit
    return res+unit

def getUnit(inp):
	if not isinstance(inp,(str)):
		return ''
	unit=''
	for char in inp:
		if char.isalpha():
			unit+=char
	return unit

def n2u(inp,unit,dig):
     if dig == -1:
          return number2unit(inp,unit)
     else:
        return formatUnit(number2unit(inp,unit),dig)

def u2n(inp):
     return unit2number(inp)