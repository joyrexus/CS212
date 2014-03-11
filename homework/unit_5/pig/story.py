from collections import defaultdict as dd
from main import max_wins, max_diffs

goal = 40
upto = goal + 1

states = [(0, me, you, pending)
          for me in range(upto)
          for you in range(upto)
          for pending in range(upto) if me + pending <= goal]

'''
assert len(states) == 35301

count = dd(int)
for s in states: count[max_wins(s), max_diffs(s)] += 1

differ, same = 0, 0

for actions in count:
    w, d = actions
    if w != d:
        differ += count[actions]
        print "{0:>15}".format(count[actions]), actions
    else:
        same += count[actions]

print
print 'Ratio of differing actions to same actions:'
print differ / (same * 1.0)
print
print 'Ratio of differing actions to all actions:'
print differ / (len(states) * 1.0)

'''
def story():
    r = dd(lambda: [0, 0])  # defaultdict with 2-tuple default value
    for s in states:
        w, d = max_wins(s), max_diffs(s)
        if w != d:
            _, _, _, pending = s
            i = (w == 'roll')
            r[pending][i] += 1

    for pending, (w,d) in sorted(r.items()):
        print "{0}: {1} {2}".format(pending, w, d)


story()
