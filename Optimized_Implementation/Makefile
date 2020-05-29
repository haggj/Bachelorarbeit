CC=gcc
PREPATH=/home/joy/Bachelorarbeit/SIDH_Implementations/SIKE/Optimized_Implementation/portable/SIKEp434/

CFLAGS=\
-I .. \
-I $(PREPATH)/P434/ \
-O3 \
-D __LINUX__ \
-D _AMD64_  \
-D _GENERIC_

OBJ = \
test.c \
../countcpu.c \
$(PREPATH)/P434/P434.c \
$(PREPATH)/P434/generic/fp_generic.c \
$(PREPATH)/random/random.c \
$(PREPATH)/sha3/fips202.c 


LIBS=-lm

test: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)