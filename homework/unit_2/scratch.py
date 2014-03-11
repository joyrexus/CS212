import re

F = 'YOU + F == ME**2'
F = 'Y + F = M'
nonzero = re.findall('([A-Z])[A-Z]', F)
conds = ['{0} != 0'.format(z) for z in nonzero]
print ' and '.join(conds)
