import numpy as np

def main():
    a = np.array([1,2,3],dtype = np.uint32)
    a = np.appned*(a,4294967295)
    print(a)
