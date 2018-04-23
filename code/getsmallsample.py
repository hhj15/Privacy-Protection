
import numpy as np

import random

trace = list(np.load('./data/trace_merge.npy'))
tracereal = list(np.load('./data/trace.npy'))
count = list(np.load('./data/count.npy'))
pick = []
pick=random.sample(range(len(trace)),500)
test_trace=[]
test_count=[]
test_trace_merge=[]
for i in pick:
    test_count.append(count[i])
    test_trace.append(tracereal[i])
    test_trace_merge.append(trace[i])

np.save('./data/test_trace.npy',test_trace)

np.save('./data/test_trace_merge.npy',test_trace_merge)

np.save('./data/test_count.npy',test_count)
