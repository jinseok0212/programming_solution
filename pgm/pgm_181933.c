#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

int solution(int a, int b, bool flag){

    if(flag == true){
        return a + b;
    }
    else{
        return a - b;
    }
}