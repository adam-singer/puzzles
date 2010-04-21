//  - - - - - - - - 
// Program: cnr.C 
// 
// Author : Miroslaw M. Soja a.k.a. Mirek
// URL    : http://www.mirek.ca
// Written: Feb. 03, 1989 
// Updated: Mar. 25, 2004
// 
// Copyright (c) 2004 Miroslaw M. Soja
// Copyright (c) 2004 www.mirek.ca
//
// Compile and link under Linux
// $ gcc cnr.C -o cnr
//
// EXAMPLE OF USAGE
// $ ./cnr 5 2
// $ ./cnr 5 3
// $ ./cnr 7 2
// etc...
//  - - - - - - - -

#include <stdio.h>
#include <string.h>
#include <alloc.h>

enum {FALSE,TRUE};

int Cnr(int*, int, int);

int main(int argc,char **argv)
{
    int n = 6; // - - - # of elemnts in the set. 
    int r = 2; // - - - # of elements in the sub-set
  
    argv++;
    argc--;
  
    if (argc == 2) {
        n = atoi(argv[0]);
        r = atoi(argv[1]);
    } 
    else if (argc == 1) {
        n = atoi(argv[0]) ;     
    } 
  
    if (n < r) {
        int tmp = n;
        n = r;
        r = tmp;
    } 
  
    int* ar = (int*) calloc(r, sizeof(int));; 
  
    for (int i=0; i < r; ++i) {
        ar[i] = i;
    }
  
    int line = 1;
    do {
        printf("%4i)   ", line++);
        for (int i=0; i < r; ++i) {
            printf("%3i",  ar[i]+1);
            if (i < (r-1)) {
                printf(", ");
            }
            else {
                printf(".");
            }
        }
        printf(" ");
     } while (Cnr(ar,n,r));
  
    free(ar); 
    return (0);
}

int Cnr(int* s, // Subset
        int n, // N-set
        int r // R-Subset
        ) 
{
    if (s[0] == (n-r)) {
        return (FALSE);
    }
      
    int indx = (n - 1);
    int i    = (r - 1);   
  
    while (s[i] == indx && i > 0) {
        --i;
        --indx;
    }
  
    s[i] += 1;
    i++; 

    while (i<r) {
        s[i] = s[i-1] + 1;
        ++i;
    }
  
    return (TRUE);
}
