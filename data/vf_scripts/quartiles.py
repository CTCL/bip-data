

def quartiles(lis):
    if len(lis) == 0:
        return 0,0,0,0,0
    if len(lis) == 1:
        return lis[0],lis[0],lis[0],lis[0],lis[0]
    slist = list(lis)
    slist.sort()
    lower = slist[:len(slist)/2]
    if len(slist) % 2 == 0:
        upper = slist[len(slist)/2:]
    else:
        upper = slist[len(slist)/2+1:]
    return min(slist), median(lower), median(slist), median(upper), max(slist)

def median(lis):
    slist = list(lis)
    slist.sort()
    if len(slist) % 2 == 0:
        median = (slist[len(slist)/2 - 1] + slist[len(slist)/2])/2.0
    else:
        median = slist[len(slist)/2]
    return median
