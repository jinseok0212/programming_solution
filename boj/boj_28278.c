#include <stdio.h>
#include <stdlib.h>

typedef struct  node{
    int data;
    struct node *link;
}NODE;

typedef struct {
    int count;
    NODE *top;
}stack;

stack *create(void);

void push(stack *pstack, int x);

int pop(stack *pstack);

int size(stack *pstack);

int empty(stack *pstack);

int stacktop(stack *pstack);

int main(void){

    stack *s;
    s = create();

    int n;
    scanf("%d", &n);
    int k;// 입력 받을 번호와 정수 값. 
    int x = 0;

    int data, c, e, t;// case 안에서 변수 선언하면 오류 뜬데ㅠ 중괄호 치기는 귀찮아. 

    for(int i = 0; i < n; i++){
        scanf("%d", &k);
        if(k == 1) scanf("%d", &x);
        switch (k)
        {
        case 1:
            push(s, x);
            break;
        
        case 2:
            data = pop(s);
            printf("%d\n", data);
            break;
        
        case 3:
            c = size(s);
            printf("%d\n", c);
            break;

        case 4:
            e = empty(s);
            printf("%d\n", e);
            break;
        
        case 5:
            t = stacktop(s);
            printf("%d\n", t);
            break;
        }
        
    }

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
    
    newnode -> data = x;
    newnode -> link = pstack -> top;
    pstack -> top = newnode;

    pstack -> count++;
}

int  pop(stack *pstack){
    if(pstack -> count == 0) return -1;

    else{
        NODE *dataout = pstack -> top;

        pstack -> top = dataout -> link; // 2번째가 탑 노드 됐고  근데 만약에 1개짜리 스택이면 이거 오류 뜨지 않나.
        int result = dataout -> data;
        free(dataout);
        pstack -> count--; //숫자 줄였고

        return result; // 이거 받ㅇ사ㅓ 출력하면 되고 

    }
}

int size(stack *pstack){
    
    return pstack -> count; 
}

int empty(stack *pstack){
    if(pstack -> count == 0) return 1;
    
    else return 0;
}

int stacktop(stack *pstack){

    if(pstack -> count == 0) return -1;

    else{
        return pstack -> top -> data;
    }
}

// 1번은 push, 2번은 pop, 3번은 count 출력, 4번은 empty인지 판단 후 출력, 5번은 스택 탑 

