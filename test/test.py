import numpy as np

def main():
    a = 0b1001100110101010
    
    for i in range(16):
            print(bin(EXTRACT(a, i, i)))

def EXTRACT(num, low, high):
    a = num >> low
    b = (2 << (high - low)) - 1
    return a & b

if __name__ == "__main__":
    main()