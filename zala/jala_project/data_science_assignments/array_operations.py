import numpy as np

print("Data Science Assignments - NumPy Practice")
print("========================================")

# Basic Array Operations

# 1. Create a 3x3 array filled with random integers between 0 and 10.
# Calculate the sum, mean, and standard deviation of the array.
print("1. Creating a 3x3 array with random integers between 0 and 10:")
array_3x3 = np.random.randint(0, 11, size=(3, 3))
print("Array:")
print(array_3x3)

# Calculate statistics
array_sum = np.sum(array_3x3)
array_mean = np.mean(array_3x3)
array_std = np.std(array_3x3)

print(f"Sum: {array_sum}")
print(f"Mean: {array_mean:.2f}")
print(f"Standard Deviation: {array_std:.2f}")
print()

# 2. Create a 1D array of 10 elements and compute the cumulative sum of the elements.
print("2. Creating a 1D array with 10 elements and computing cumulative sum:")
array_1d = np.random.randint(1, 11, size=10)
print(f"Array: {array_1d}")

# Calculate cumulative sum
cumulative_sum = np.cumsum(array_1d)
print(f"Cumulative Sum: {cumulative_sum}")
print()

# 3. Generate two 2x3 arrays with random integers and perform element-wise operations.
print("3. Creating two 2x3 arrays and performing element-wise operations:")
array1 = np.random.randint(1, 11, size=(2, 3))
array2 = np.random.randint(1, 11, size=(2, 3))

print("First Array:")
print(array1)
print("\nSecond Array:")
print(array2)

# Element-wise operations
addition = array1 + array2
subtraction = array1 - array2
multiplication = array1 * array2
division = array1 / array2

print("\nAddition:")
print(addition)
print("\nSubtraction:")
print(subtraction)
print("\nMultiplication:")
print(multiplication)
print("\nDivision:")
print(division)
print()

# 4. Create a 4x4 identity matrix.
print("4. Creating a 4x4 identity matrix:")
identity_matrix = np.eye(4)
print("Identity Matrix:")
print(identity_matrix)
print()

# 5. Given an array a = np.array([5, 10, 15, 20, 25]), divide each element by 5 using broadcasting.
print("5. Dividing each element by 5 using broadcasting:")
a = np.array([5, 10, 15, 20, 25])
print(f"Original Array: {a}")

# Divide each element by 5
result = a / 5
print(f"After dividing by 5: {result}")
print()

print("Array Manipulation:")
print("-" * 18)

# 6. Reshape a 1D array of 12 elements into a 3x4 matrix.
print("6. Reshaping a 1D array of 12 elements into a 3x4 matrix:")
array_12 = np.arange(1, 13)
print(f"Original 1D Array: {array_12}")

reshaped = array_12.reshape(3, 4)
print("Reshaped to 3x4:")
print(reshaped)
print()

# 7. Flatten a 3x3 matrix into a 1D array.
print("7. Flattening a 3x3 matrix into a 1D array:")
matrix_3x3 = np.random.randint(1, 11, size=(3, 3))
print("3x3 Matrix:")
print(matrix_3x3)

flattened = matrix_3x3.flatten()
print(f"Flattened to 1D: {flattened}")
print()

# 8. Stack two 3x3 matrices horizontally and vertically.
print("8. Stacking two 3x3 matrices horizontally and vertically:")
mat1 = np.random.randint(1, 6, size=(3, 3))
mat2 = np.random.randint(6, 11, size=(3, 3))

print("First Matrix:")
print(mat1)
print("\nSecond Matrix:")
print(mat2)

# Horizontal stacking
h_stacked = np.hstack((mat1, mat2))
print("\nHorizontally stacked:")
print(h_stacked)

# Vertical stacking
v_stacked = np.vstack((mat1, mat2))
print("\nVertically stacked:")
print(v_stacked)
print()

# 9. Concatenate two arrays along a new axis.
print("9. Concatenating two arrays along a new axis:")
arr1 = np.array([[1, 2, 3], [4, 5, 6]])
arr2 = np.array([[7, 8, 9], [10, 11, 12]])

print(f"First array shape: {arr1.shape}")
print(f"Second array shape: {arr2.shape}")

# Stack arrays along a new axis
stacked = np.stack((arr1, arr2), axis=0)
print("\nStacked along new axis:")
print(stacked)
print(f"New shape: {stacked.shape}")
print()

# 10. Transpose a 3x2 matrix.
print("10. Transposing a 3x2 matrix:")
matrix_3x2 = np.random.randint(1, 11, size=(3, 2))
print("Original 3x2 Matrix:")
print(matrix_3x2)

# Transpose the matrix
transposed = matrix_3x2.T
print("\nTransposed (2x3):")
print(transposed)
print()

print("Indexing and Slicing:")
print("-" * 20)

# 11. Given a 1D array of 15 elements, extract elements at positions 2 to 10 with a step of 2.
print("11. Extracting elements from a 1D array with specific step:")
arr_15 = np.arange(1, 16)
print(f"Array: {arr_15}")

# Extract elements from index 2 to 10 with step of 2
extracted = arr_15[2:11:2]
print(f"Extracted elements: {extracted}")
print()

# 12. Create a 5x5 matrix and extract the sub-matrix containing elements from rows 1 to 3 and columns 2 to 4.
print("12. Creating a 5x5 matrix and extracting a sub-matrix:")
matrix_5x5 = np.random.randint(1, 26, size=(5, 5))
print("5x5 Matrix:")
print(matrix_5x5)

# Extract sub-matrix from rows 1-3 and columns 2-4
sub_matrix = matrix_5x5[1:4, 2:5]
print("\nSub-matrix (rows 1-3, cols 2-4):")
print(sub_matrix)
print()

# 13. Replace all elements in a 1D array greater than 10 with the value 10.
print("13. Replacing elements greater than 10 with 10:")
arr_replace = np.random.randint(5, 20, size=10)
print(f"Original array: {arr_replace}")

# Replace elements greater than 10 with 10
arr_replace[arr_replace > 10] = 10
print(f"After replacement: {arr_replace}")
print()

# 14. Use fancy indexing to select elements from a 1D array at positions [0, 2, 4, 6].
print("14. Using fancy indexing to select specific elements:")
arr_fancy = np.random.randint(1, 21, size=10)
print(f"Original array: {arr_fancy}")

# Select elements at specific positions
positions = [0, 2, 4, 6]
selected = arr_fancy[positions]
print(f"Selected elements at positions {positions}: {selected}")
print()

# 15. Create a 1D array of 10 elements and reverse it using slicing.
print("15. Reversing a 1D array using slicing:")
arr_reverse = np.random.randint(1, 11, size=10)
print(f"Original array: {arr_reverse}")

# Reverse the array using slicing
reversed_arr = arr_reverse[::-1]
print(f"Reversed array: {reversed_arr}")
print()

print("Broadcasting:")
print("-" * 12)

# 16. Create a 3x3 matrix and add a 1x3 array to each row using broadcasting.
print("16. Adding a 1D array to each row of a 3x3 matrix using broadcasting:")
matrix_3x3 = np.random.randint(1, 6, size=(3, 3))
array_1x3 = np.random.randint(1, 4, size=3)

print("3x3 Matrix:")
print(matrix_3x3)
print(f"\n1D Array: {array_1x3}")

# Broadcasting addition
result = matrix_3x3 + array_1x3
print("\nResult after adding 1D array to each row:")
print(result)
print()

# 17. Multiply a 1D array of 5 elements by a scalar value using broadcasting.
print("17. Multiplying a 1D array by a scalar using broadcasting:")
arr_1d_5 = np.random.randint(1, 6, size=5)
scalar = 3

print(f"Original array: {arr_1d_5}")
print(f"Scalar value: {scalar}")

# Scalar multiplication
result = arr_1d_5 * scalar
print(f"Result: {result}")
print()

# 18. Subtract a 3x1 column vector from a 3x3 matrix using broadcasting.
print("18. Subtracting a column vector from a 3x3 matrix using broadcasting:")
matrix_3x3_new = np.random.randint(5, 11, size=(3, 3))
col_vector = np.random.randint(1, 4, size=(3, 1))

print("3x3 Matrix:")
print(matrix_3x3_new)
print("\nColumn Vector:")
print(col_vector)

# Broadcasting subtraction
result = matrix_3x3_new - col_vector
print("\nResult after subtracting column vector:")
print(result)
print()

# 19. Add a scalar to a 3D array and demonstrate how broadcasting works across all dimensions.
print("19. Adding a scalar to a 3D array using broadcasting:")
array_3d = np.random.randint(1, 6, size=(2, 3, 4))
scalar_3d = 10

print(f"3D Array shape: {array_3d.shape}")
print("\nFirst 2D slice:")
print(array_3d[0])
print(f"\nScalar value: {scalar_3d}")

# Broadcasting scalar addition
result_3d = array_3d + scalar_3d
print("\nResult after adding scalar (first 2D slice):")
print(result_3d[0])
print()

# 20. Create two arrays of shapes (4, 1) and (1, 5) and add them using broadcasting.
print("20. Adding two arrays with different shapes using broadcasting:")
arr_4x1 = np.random.randint(1, 6, size=(4, 1))
arr_1x5 = np.random.randint(1, 6, size=(1, 5))

print("Array (4, 1):")
print(arr_4x1)
print("\nArray (1, 5):")
print(arr_1x5)

# Broadcasting addition
result = arr_4x1 + arr_1x5
print(f"\nResult shape: {result.shape}")
print("Result:")
print(result)
print()

print("Vectorized Operations:")
print("-" * 22)

# 21. Compute the square root of each element
print("21. Computing the square root of each element:")
arr_sqrt = np.random.randint(1, 11, size=5)
print(f"Original array: {arr_sqrt}")

# Calculate square root of each element
sqrt_result = np.sqrt(arr_sqrt)
print(f"Square roots: {sqrt_result}")
print(f"Square roots rounded: {np.round(sqrt_result, 2)}")
print()

print("All Data Science assignments completed successfully!")