import numpy as np

def deriveAllocations(num_players, influence):
    ave_alloc = influence.copy()
    negatives = np.negative(ave_alloc).clip(0)
    for r in range(0,num_players):
        takes = sum(negatives[r])
        ave_alloc[r][r] -= takes
        mag = np.linalg.norm(ave_alloc[r], ord=1)
        ave_alloc[r] = ave_alloc[r] / mag
        ave_alloc[r][r] += takes / mag

    return ave_alloc


def computeSupportGraph(num_players, W1):
    ave_alloc = deriveAllocations(len(W1), W1)
    Wsum = W1.copy()
    Wmult = W1.copy()
    rate = 0.8 #1.0 - self.gameParams["alpha"]
    r = rate
    depth = 5 #self.genes["supportDepth"] / 10
    for i in range(0,int(depth)):
        Wmult = np.dot(Wmult,ave_alloc)
        Wsum += r * Wmult
        r *= rate

    # self.supportGraph = Bsum
    return Wsum


if __name__ == '__main__':          
    np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
    rate = 0.8
    # B1 = np.array([[0,2.6,1.3,0,0,0],[2.6,0,1.3,0,0,0],[1.3,1.3,0,1.3,0,0],[0,0,1.3,0,1.3,1.3],[0,0,0,1.3,0.95,1.3],[0,-1.6,0,1.3,1.3,1.6]])
    # B1 = np.array([[0,2.6,1.3,0,0,0],[2.6,1.6,0,0,0,-1.6],[1.3,0,0.95,1.3,0,0],[0,0,1.3,0,1.3,1.3],[0,0,0,1.3,0.95,1.3],[0,-1.6,0,1.3,1.3,1.6]])
    # B1 = np.array([[0.0,94.5,2.2,17.5,28.2,34.3,2.0],[92.9,0.0,8.0,2.1,7.9,60.0,1.4],[1.4,5.6,0.1,268.2,204.0,2.9,0.0],[4.0,0.7,266.0,0.1,200.7,4.6,0.0],[30.0,4.1,197.7,199.7,0.1,32.7,0.0],[30.5,59.1,6.9,9.7,27.7,0.0,1.2],[0.0,0.0,0.0,0.0,0.0,0.0,79.1]])
    influence = np.array([[0,3,2,0,0],[3,1.5,0,0,0],[2,0,0,2,1],[0,0,2,0,3],[0,-1,1,3,1]])
    print(influence)
    
    Wsum = computeSupportGraph(len(influence), influence)
    print()
    print(Wsum)


    # print(B1.sum(axis=1))
    # mx = max(B1.sum(axis=1))
    # B1 = B1 / mx
    # print()
    # print(B1)
    # print(B1.sum(axis=1))

    # B2 = np.dot(B1,B1)
    # B3 = np.dot(B2,B1)
    # B4 = np.dot(B3,B1)
    # B5 = np.dot(B4,B1)
    # B6 = np.dot(B5,B1)
    # mag1 = sum(sum(np.absolute(B1)))
    # mag2 = sum(sum(np.absolute(B2)))
    # mag3 = sum(sum(np.absolute(B3)))
    # mag4 = sum(sum(np.absolute(B4)))
    # mag5 = sum(sum(np.absolute(B5)))
    # mag6 = sum(sum(np.absolute(B6)))
    # print(mag1)
    # print(mag2)
    # print(mag3)
    # print(mag4)
    # print(mag5)
    # print(mag6)
    # mag1 = mag2 = mag3 = mag4 = mag5 = mag6 = 1
    # B2prime = rate * (mag1 / mag2) * B2
    # print()
    # print(B2prime)
    # B3prime = rate * rate * (mag1 / mag3) * B3
    # print()
    # print(B3prime)
    # B4prime = rate * rate * rate * (mag1 / mag4) * B4
    # print()
    # print(B4prime)
    # B5prime = rate * rate * rate * rate * (mag1 / mag5) * B5
    # print()
    # print(B5prime)
    # # B6prime = rate * rate * rate * rate * rate * (mag1 / mag6) * B6
    # # print()
    # # print(B6prime)

    # Bsum = B1+B2prime+B3prime+B4prime+B5prime#+B6prime
    # print()
    # print(Bsum)
    # print()
    # print(Bsum.sum(axis=0))