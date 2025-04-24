#!/bin/bash

# Check if the C source code file exists
if [ ! -f pmxm.c ]; then
    echo "Error: pmxm.c not found!"
    exit 1
fi

# Compile the C source code with OpenMP enabled
echo "Compiling pmxm.c with OpenMP support..."
gcc -o epmxm pmxm.c -fopenmp -O2

# Check if the compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful."
else
    echo "Compilation failed."
    exit 1
fi

# Set the number of threads and problem size
export OMP_NUM_THREADS=8
problemSize=2024

# Run the compiled executable with the fixed problem size
echo "Running the matrix multiplication program with problem size $problemSize and threads $OMP_NUM_THREADS..."
./epmxm $problemSize

