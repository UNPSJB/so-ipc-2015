
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// Recibe como argumetno la cantidad de mensajes a enviar
// por defecto son 100. El máximo son 200 y el mínumo 1
int main(int argc, char **argv) {
    int i, x, y, cantidad;
    char buffer[500];
    
    srand(getpid());
    
    if (argc < 2) {
        cantidad = 100;
    } else {
        cantidad = atoi(argv[1]);
        if ((cantidad < 1) || (cantidad > 1000)) {
            cantidad = 100;
        }
    }

    for (i=0; i<cantidad; i++) {
        x = rand() % 500;
        y = rand() % 500;
        sprintf(buffer, "{\"numero\": %d, \"x\": %d, \"y\": %d}\n", 
                1 + (rand() % 3), x, y);
        //fprintf(stderr, "Mensaje %i\n", i);
        printf("%s", buffer);
        fflush(stdout);
    }
}