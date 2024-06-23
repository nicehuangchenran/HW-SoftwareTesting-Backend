import numpy as np

def conv2d(input_matrix, kernel, stride=1, pad=1):
    # Add padding to the input matrix
    input_padded = np.pad(input_matrix, pad, mode='constant', constant_values=0)
    
    # Dimensions of the input and kernel
    input_height, input_width = input_padded.shape
    kernel_height, kernel_width = kernel.shape
    
    # Calculate the dimensions of the output
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1
    
    # Initialize the output matrix
    output_matrix = np.zeros((output_height, output_width))
    
    # Perform the convolution operation
    for i in range(0, output_height):
        for j in range(0, output_width):
            # Extract the region of interest
            region = input_padded[i*stride:i*stride+kernel_height, j*stride:j*stride+kernel_width]
            # Perform element-wise multiplication and sum the result
            output_matrix[i, j] = np.sum(region * kernel)
    
    return output_matrix

# Example input and kernel
input_matrix = np.array([
    [1, 2, 3, 0],
    [0, 1, 2, 3],
    [3, 0, 1, 2],
    [2, 3, 0, 1]
])

kernel = np.array([
    [2, 0, 1],
    [0, 1, 2],
    [1, 0, 2]
])

output_matrix = conv2d(input_matrix, kernel)
print("Input Matrix:\n", input_matrix)
print("Kernel:\n", kernel)
print("Output Matrix:\n", output_matrix)
