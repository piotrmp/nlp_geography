# Computing Gini coefficient
# Optional adjustment: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=224896

def giniCoeff(y,adjusted=False):
    y=y.copy()
    n=len(y)
    y.sort()
    inner=0
    for i in range(n):
        inner=inner+(n+1-(i+1))*y[i]
    G=1/n*(n+1-2*inner/sum(y))
    if adjusted and sum(y)>1:
        return G*sum(y)/(sum(y)-1)
    else:
        return(G)

def diversity(y):
    return 1.0-giniCoeff(y)