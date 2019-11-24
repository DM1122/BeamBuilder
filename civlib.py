def flexStress(M, y, I):

    sigma = M * y / I

    return sigma

def flexForce(sigma, I, y, c):

    P = (sigma * I) / (c * y)

    return P


def shearStress(V, Q, I, b):

    tau  = (V * Q) / (I * b)

    return tau


def shearForce(tau, I, b, Q, c):

    P = (c * tau * I * b) / Q
    
    return P


if __name__ == '__main__':
    pass