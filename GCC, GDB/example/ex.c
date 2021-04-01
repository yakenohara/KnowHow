#include <stdio.h>

int main(int argc, char* argv[]){
    
    int i;
    
    printf("number of argments %d\n", argc);
    for (i = 0; i < argc; i++) {
        printf("argment %d:\"%s\"\n", i, argv[i]);
    }
    
    return 0;
}