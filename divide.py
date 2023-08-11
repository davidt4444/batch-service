import math
# https://docs.nvidia.com/cuda/pdf/CUDA_C_Best_Practices_Guide.pdf
def div (a:int, b:int, length:int):
    if(b==0):
        raise Exception("ZeroDivisionError: integer division or modulo by zero")
    neg = False
    if(a<0):
        a = math.abs(a)
        neg = not neg
    if(b<0):
        b = math.abs(b)
        neg = not neg
    result = 0
    for i in range(length, -1, -1):
        if a>=(b<<i):
            a -= b<<i
            result += 1<<i
    if neg:
        return result*-1
    return result 

def main():
    result1 = 10// 2
    result2 = div(10, 0, 32)
    print(result1)
    print(result2)

if __name__ == "__main__":
     main()
