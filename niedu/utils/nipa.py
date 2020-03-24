import os.path as op


def sorted_fix(paths, prefix='tstat'):
    return sorted(paths, key=lambda x: int(op.basename(x).split('.')[0].split(prefix)[1]))


def return_some_objects():

    obj1 = (5, 3, 2)
    obj2 = True
    obj3 = 5.3216
    return(obj1, obj2, obj3)
