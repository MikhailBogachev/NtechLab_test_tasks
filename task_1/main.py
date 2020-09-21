A = [-2,1,-3,4,-1,2,1,-5,4]

def findMaxSubArray(A):
    B = sum(A)
    for i in range(len(A)):
        if i == 0:
            for j in range(2, len(A)-1):
                if sum(A[i:j]) > B:
                    B = sum(A[i:j])
                    C = A[i:j]

        else:
            for j in range(i+2, len(A)):
                if sum(A[i:j]) > B:
                    B = sum(A[i:j])
                    C = A[i:j]
    print(C)

findMaxSubArray(A)
