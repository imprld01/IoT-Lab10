def lowpass(x, dt, RC):
    y = x
    alpha = dt / (RC + dt)
    
    for idx in range(1, x.shape[0]):
        y[idx] = alpha * x[idx] + (1 - alpha) * y[idx - 1]
        
    return y