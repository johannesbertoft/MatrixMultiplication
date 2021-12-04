public class Matrix {
    private int rows = 0;
    private int columns = 0;
    private double[] data = null; /* internal flat data array */
    private int firstIdx = 0; /* flat index of the first entry (top-left) */
    private int stride = 0; /* row length (i.e. how many indices must
                             * be advanced in the flat array to get to
                             * the same column in the next row) */


    
    /**
     * Constructs an empty matrix (by keeping the default values on all fields)
     */
    public Matrix() {
    }


    
    /**
     * Construct a zero-initialized matrix of a certain size.
     */
    public Matrix(int rows, int columns) {
        this.rows = rows;
        this.columns = columns;
        data = new double[rows*columns];
        stride = columns;
    }    
    
    /**
     * Initialize a matrix of certain shape from a flat array. The
     * data is *not* copied.
     */
    public Matrix(double[] data, int rows, int columns) {
        this.rows = rows;
        this.columns = columns;
        this.data = data;
        stride = columns;
    }


    
    /**
     * Initialize a submatrix view from a flat array. The
     * data is *not* copied.
     */
    public Matrix(double[] data, int rows, int columns, 
                  int rowLength, int firstIdx) {
        this.rows = rows;
        this.columns = columns;
        this.data = data;
        stride = rowLength;
        this.firstIdx = firstIdx;
    }



    /**
     * Construct a matrix from the data given as a array of arrays
     * (useful for initializing matrix from literal data).
     */
    Matrix(double[][] initialData) {
        rows = initialData.length;
        columns = initialData[0].length;
        data = new double[rows*columns];
        stride = columns;
        firstIdx = 0;
        int k = 0;
        for (int i = 0; i < rows; ++i)
            for (int j = 0; j < columns; ++j)
                data[k++] = initialData[i][j];
    }


    
    /**
     * Adds the right hand operand to the left hand matrix in-place.
     */
    public void add(Matrix that) {
        /* fill in the implementation */
    }

    

    /**
     * Returns a copy that is the sum of the two operands
     */
    public static Matrix add(Matrix A, Matrix B) {
        /* fill in the implementation */
        return null;
    }

    

    /**
     * Returns a copy that is the difference of the two operands
     */
    public static Matrix subtract(Matrix A, Matrix B) {
        /* fill in the implementation */
        return null;
    }


    
    /**
     * Subtracts the right hand operand from the left hand matrix in-place
     */
    public void subtract(Matrix that) {
        /* fill in the implementation */
    }


    
    /**
     * Returns the number of rows
     */
    public int getRows() {
        return rows;
    }


    
    /**
     * Returns the number of columns
     */
    public int getColumns() {
        return columns;
    }

    

    /**
     * Return the element at the index.
     */
    public double get(int i, int j) {
        return data[firstIdx + i*stride + j];
    }

    

    /**
     * Set the element at the index.
     */
    public void set(int i, int j, double d) {
        data[firstIdx + i*stride + j] = d;
    }



    /**
     * Construct a shallow view into a matrix. Data is not copied, but
     * the original matrix can be accessed from the new Matrix object.
     */
    public Matrix getSubmatrix(int i0, int j0, int rows,
                               int columns) {
        return new Matrix(data, rows, columns, stride,
                          firstIdx + i0*stride + j0);
    }

    

    /**
     * Equality comparison
     */
    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null)
            return false;
        if (!(o instanceof Matrix))
            return false;
        Matrix that = (Matrix)o;
        if (getRows() != that.getRows())
            return false;
        if (getColumns() != that.getColumns())
            return false;
        for (int i = 0; i < getRows(); ++i)
            for (int j = 0; j < getColumns(); ++j)
                if (get(i,j) != that.get(i,j))
                    return false;
        return true;
    }



    /**
     * Returns a nice string representation of the matrix
     */
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < getRows(); ++i) {
            if (i > 0)
                sb.append('\n');
            for (int j = 0; j < getColumns(); ++j) {
                if (j > 0)
                    sb.append(" ");
                sb.append(get(i,j));
            }
        }
        return sb.toString();
    }

    

    /**
     * Returns a deep copy of the matrix.
     */
    public Matrix copy() {
        double[] newData = new double[rows*columns];
        int k = 0;
        for (int i = 0; i < rows; ++i)
            for (int j = 0; j < columns; ++j)
                newData[k++] = data[firstIdx + i*stride + j];
        return new Matrix(newData, rows, columns);
    }


    
    /**
     * Compute C = AB with three nested loops
     */
    public static Matrix elementaryMultiplication(Matrix A, Matrix B) {
        /*
          Fill in the implementation here
         */
        return null;
    }

    

    /**
     * Transposes the matrix in-place
     */
    public static void transpose(Matrix A) {
        /*
          Fill in the implementation here
         */
    }


    
    /**
     * Compute C = AB with three nested loops, assuming transposed B
     */
    public static Matrix elementaryMultiplicationTransposed(Matrix A, Matrix B) {
        /*
          Fill in the implementation here
         */
        return null;
    }



    /**
     * Computes C=AB using (n/s)^3 multiplications of size s*s
     */
    public static Matrix tiledMultiplication(Matrix A, Matrix B, int s) {
        /*
          Fill in the implementation here
         */
        return null;
    }



    /**
     * Computes C=AB by explicitly writing all intermediate
     * results. That is, we define the following matrices in terms of
     * the operand block matrices:
     *
     * P0 = A00
     * P1 = A01
     * P2 = A00
     * P3 = A01
     * P4 = A10
     * P5 = A11
     * P6 = A10
     * P7 = A11
     * Q0 = B00
     * Q1 = B10
     * Q2 = B01
     * Q3 = B11
     * Q4 = B00
     * Q5 = B10
     * Q6 = B01
     * Q7 = B11
     *
     * Then compute Mi = Pi*Qi by a recursive application of the function
     *
     * Followed by the integration
     * C00 = M0 + M1
     * C01 = M2 + M3
     * C10 = M4 + M5
     * C11 = M6 + M7
     */
    public static Matrix recursiveMultiplicationCopying(Matrix A, Matrix B) {
        /*
          Fill in the implementation here
        */
        return null;
    }



    /**
     * An auxiliary function that computes elementary matrix
     * multiplication in place, that is, the operation is C += AB such
     * that the product of AB is added to matrix C.
     */
    public static void elementaryMultiplicationInPlace(Matrix C, Matrix A, Matrix B) {
        /*
          Fill in the implementation here
         */
    }
    


    /**
     * Computes C=AB recursively using a write-through strategy. That
     * is, no intermediate copies are created; the matrix C is
     * initialized as the function is first called, and all updates
     * are done in-place in the recursive calls.
     * 
     * The parameter m controls such that when the subproblem size
     * satisfies n <= m, * an iterative cubic algorithm is called instead.
     */
    public static Matrix recursiveMultiplicationWriteThrough(Matrix A, Matrix B, int m) {
        /*
          Fill in the implementation here
        */
        return null;
    }


    
    /**
     * Computes C=AB using Strassen's algorithm. The structure ought
     * to be similar to the copying recursive algorithm. The parameter
     * m controls when the routine falls back to a cubic algorithm, as
     * the subproblem size satisfies n <= m.
     */
    public static Matrix strassen(Matrix A, Matrix B, int m) {
        /*
          Fill in the implementation here
         */
        return null;
    }
}
