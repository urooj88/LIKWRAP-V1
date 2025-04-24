//  gcc -o opmxm mxm3p.c -fopenmp -O2
//  ./opmxm 1500 8
// 1500 → Matrix size (N x N).
// 8 → Number of OpenMP threads (optional).



#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <time.h>

// Function to initialize matrices with random values
void initialize_matrix(double **matrix, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            matrix[i][j] = rand() % 100; // Random values between 0 and 99
        }
    }
}

// Matrix multiplication function
void matrix_multiply(double **A, double **B, double **C, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            C[i][j] = 0.0;
            for (int k = 0; k < size; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

// Function to display memory usage using getrusage()
void print_memory_usage() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    printf("Memory usage: %ld kilobytes\n", usage.ru_maxrss);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <matrix_size>\n", argv[0]);
        return 1;
    }
    
    int N = atoi(argv[1]);
    if (N <= 0) {
        printf("Invalid matrix size. Please enter a positive integer.\n");
        return 1;
    }
    
    // Dynamically allocate matrices
    double **A = (double **)malloc(N * sizeof(double *));
    double **B = (double **)malloc(N * sizeof(double *));
    double **C = (double **)malloc(N * sizeof(double *));
    for (int i = 0; i < N; i++) {
        A[i] = (double *)malloc(N * sizeof(double));
        B[i] = (double *)malloc(N * sizeof(double));
        C[i] = (double *)malloc(N * sizeof(double));
    }
    
    // Start timing the overall execution
    double start_total_time = (double)clock() / CLOCKS_PER_SEC;
    
    // Initialize matrices A and B with random values
    initialize_matrix(A, N);
    initialize_matrix(B, N);
    
    // End initialization time
    double end_initialization_time = (double)clock() / CLOCKS_PER_SEC;
    
    // Start timing the computation time
    double start_computation_time = (double)clock() / CLOCKS_PER_SEC;
    
    // Perform matrix multiplication
    matrix_multiply(A, B, C, N);
    
    // End computation time
    double end_computation_time = (double)clock() / CLOCKS_PER_SEC;
    
    // End total time
    double end_total_time = (double)clock() / CLOCKS_PER_SEC;
    
    // Display timing results
    printf("Total time: %f seconds\n", end_total_time - start_total_time);
    printf("Initialization time: %f seconds\n", end_initialization_time - start_total_time);
    printf("Computation time: %f seconds\n", end_computation_time - start_computation_time);
    
    // Display memory usage
    print_memory_usage();
    
    // Free allocated memory
    for (int i = 0; i < N; i++) {
        free(A[i]);
        free(B[i]);
        free(C[i]);
    }
    free(A);
    free(B);
    free(C);
    
    return 0;
}

