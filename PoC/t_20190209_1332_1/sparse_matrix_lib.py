
"""
Defines a class SparseMatrix which implements the efficient memory storage and supports both sum and multiply 
"""

import copy

class SparseMatrix: 
    def __init__(self, r, c): 
        self.r = r
        self.c = c 
        
        # Main Storage is a dict 
        self.db = dict()
        
    def __sc_in_bounds__(self, r, c): 
        if((r<0) or (c<0) or (r>=self.r) or (c>=self.c)): 
            raise Exception("Out of bound")
            
    
    def __sc_matrix_sum__(self, m): 
        if( (self.r != m.r) or (self.c != m.c) ): 
            raise Exception("Matrix Dim do not match")
    
    def __sc_matrix_mul__(self, m): 
        if( self.c != m.r ): 
            raise Exception("Matrix dim do not match")
    
    # Logic defining the hashable key 
    def __get_key__(self, r, c): 
        return str(r) + "," + str(c)
        
    def set(self, r, c, val): 
        self.__sc_in_bounds__(r,c)
        key = self.__get_key__(r,c)
        self.db[key] = val
        
    # Sparsity Representation: each missing key is zero 
    def get(self, r,c): 
        self.__sc_in_bounds__(r,c)
        key = self.__get_key__(r,c)
        if(key in self.db): 
            return self.db[key]
        else: 
            return 0
    
    def clone(self): 
        res = SparseMatrix(self.r, self.c)
        # Make an independent one 
        res.db = copy.deepcopy(self.db)
        return res
    
    def sum(self, m): 
        self.__sc_matrix_sum__(m)
        res = self.clone()
        for k in m.db: 
            if(k in res.db): 
                res.db[k] += m.db[k]
            else: 
                res.db[k] = m.db[k]
        return res
    
    
    def mul(self, m): 
        self.__sc_matrix_mul__(m)
        res = SparseMatrix(self.r, m.c)
        for k1 in self.db: 
            for k2 in m.db: 
                _k1 = k1.split(",")
                _k2 = k2.split(",")
                # NOTE: Get only meaningful combinatoins 
                if(_k2[0]==_k1[1]): 
                    k = self.__get_key__(_k1[0], _k2[1])
                    val = self.db[k1] * m.db[k2]
                    #print("Processing " + k1 + ", " + k2 + ", " + k + " give " + str(self.db[k1]) + " * " + str(m.db[k2]) + " = " + str(val))
                    if(k in res.db): 
                        res.db[k] += val
                    else: 
                        res.db[k] = val
        return res 

    
    def to_str_compact(self): 
        # NOTE: Empty Dict evaluate to False 
        if(not self.db): 
            return "(Empty)"
        
        res = ""
        for k in self.db: 
            res += "Key=(" + k + ") Val=(" + str(self.db[k]) + ")\n"
        return res
    
    def to_str_full(self): 
        res = ""
        for i in range(self.r): 
            for j in range(self.c): 
                key = self.__get_key__(i,j)
                if(key in self.db): 
                    res += str(self.db[key])
                else: 
                    res += "0"
                res += " "
            res += "\n"
        return res

