#include "model.h"
#include "parameter.h"

void run(Parameter p){
	SizeOptions opt("Hexagon");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<Model,DFS,SizeOptions>(opt);	
};

int main(int argc, char* argv[]){
	Parameter p;
	run(p);
}