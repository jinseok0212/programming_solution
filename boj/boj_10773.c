#include <stdio.h>
#include <stdlib.h>

typedef struct node{

    int data;
    struct node *link;

}NODE;

typedef struct{

    int count;
    NODE *top;
}stack;

stack *create(void);
void push(stack *pstack, int x);
void pop(stack *pstack);


int main(void){

    int k;
    scanf("%d", &k);
    stack *pstack = create();
    int x = 0;
    for(int i = 0; i < k; i++){
        scanf("%d", &x);
        if(x == 0){
            pop(pstack);
        }
        else{
            push(pstack, x);
        }

    }
    int sum = 0;
    NODE *cur = pstack -> top;
    for(int i = 0; i < pstack -> count; i++){
        sum += cur -> data;
        cur = cur -> link;
    }

    printf("%d", sum);

    return 0;
}

stack *create(void){
    stack *pstack = (stack *)malloc(sizeof(stack));
    if(pstack == NULL) return NULL;

    pstack -> count = 0;
    pstack -> top = NULL;

    return pstack;
}

void push(stack *pstack, int x){

    NODE *newnode = (NODE *)malloc(sizeof(NODE));
    if(newnode == NULL) return;

    newnode -> data = x;
    newnode -> link = pstack -> top;
    pstack -> top = newnode;

    pstack -> count++;
}

void pop(stack *pstack){
    NODE *dataout;
    dataout= pstack -> top;

    pstack -> top = dataout -> link;
    free(dataout);
    
    pstack -> count--;
}

