import cv2
import numpy as np

def compute_local_histogram(frame, partitions=(2, 2), bins=16):
    h, w = frame.shape[:2]
    histograms = []
    
    # Partition size
    ph, pw = h // partitions[0], w // partitions[1]
    
    for i in range(partitions[0]):
        for j in range(partitions[1]):
            # Define the region
            region = frame[i*ph:(i+1)*ph, j*pw:(j+1)*pw]
            
            # Calculate histogram for each color channel
            hist_b = cv2.calcHist([region], [0], None, [bins], [0, 256])
            hist_g = cv2.calcHist([region], [1], None, [bins], [0, 256])
            hist_r = cv2.calcHist([region], [2], None, [bins], [0, 256])
            
            # Normalize and flatten histograms
            hist = np.concatenate([hist_b, hist_g, hist_r]).flatten()
            histograms.append(hist)
    
    return histograms
