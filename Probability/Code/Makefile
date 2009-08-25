pmf: pmf_generator.o
	g++ pmf_generator.o -o pmf_gen
pmf_generator.o: pmf_generator.cpp
	g++ -c pmf_generator.cpp -o pmf_generator.o

approx: poisson_approx.o
	g++ poisson_approx.o -o poisson_approx
poisson_approx.o: poisson_approx.cpp
	g++ -c poisson_approx.cpp -o poisson_approx.o

clean:
	rm *.o

cleandata:
	rm data*.csv

