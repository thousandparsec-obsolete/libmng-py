
_mnghelper.so: mnghelper.o
	cc -shared -o _mnghelper.so -lmng mnghelper.o

mnghelper.o: mnghelper.c
	cc -fPIC -c mnghelper.c -g -Wall

clean:
	rm *.o *.so
