CC=gcc

CFLAGS= -I .. 

OBJ = test.c ../countcpu.c

LIBS=-L/usr/lib/x86_64-linux-gnu/ -lssl -lcrypto -ggdb

test: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)