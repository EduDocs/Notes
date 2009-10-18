pmf: pmf_generator.o
	g++ pmf_generator.o -o pmf_gen
pmf_generator.o: pmf_generator.cpp
	g++ -c pmf_generator.cpp -o pmf_generator.o

cdf: cdf_generator.o
	g++ cdf_generator.o -o cdf_gen
cdf_generator.o: cdf_generator.cpp
	g++ -c cdf_generator.cpp -o cdf_generator.o

approx: poisson_approx.o
	g++ poisson_approx.o -o poisson_approx
poisson_approx.o: poisson_approx.cpp
	g++ -c poisson_approx.cpp -o poisson_approx.o

random: pran.o
	g++ pran.o -o pran
prandom.o: pran.cpp
	g++ -c pran.cpp -o pran.o

clean:
	rm *.o

cleandata:
	rm data*.csv

