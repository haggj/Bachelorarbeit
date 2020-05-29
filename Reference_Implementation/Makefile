CC=gcc
PREPATH=/home/joy/Bachelorarbeit/SIDH_Implementations/SIKE/Reference_Implementation/
CFLAGS=\
-I .. \
-I . \
-I $(PREPATH)/include/ \
-I $(PREPATH)/test/ \
-I $(PREPATH)/symmetric/ \
-ggdb
# -DTARGET_OS=1 \
# -DTARGET=4 \

OBJ = \
test.c \
../countcpu.c \
$(PREPATH)/test/test_sike.c \
$(PREPATH)symmetric/rng.c\
$(PREPATH)symmetric/aes_c.c\
$(PREPATH)symmetric/fips202.c\
$(PREPATH)test/printing.c \
$(PREPATH)test/test_extras.c \
$(PREPATH)src/*.c

LIBS=-lgmp

test: $(OBJ)
	@ $(CC) -o $@ $^ $(CFLAGS) $(LIBS)


