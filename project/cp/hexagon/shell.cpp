#include "model.h"
#include "parameter.h"

void symmetry(Parameter p){
	SizeOptions opt("Hexagon-symmetry");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<SBModel,DFS,SizeOptions>(opt);	
};

void standard(Parameter p){
	SizeOptions opt("Hexagon-standard");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<Model,DFS,SizeOptions>(opt);	
};


void implied(Parameter p){
	SizeOptions opt("Hexagon-implied");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	if (p.i("print"))
		Script::run<PrinterImpliedModel,DFS,SizeOptions>(opt);	
	else
		Script::run<ImpliedModel,DFS,SizeOptions>(opt);	
};


#define STANDARD 0
#define SYMMETRY 1
#define IMPLIED 2

int main(int argc, char* argv[]){
	Parameter p;
	
	switch(p.i("model")){
		case STANDARD: standard(p); break;
		case SYMMETRY: symmetry(p); break;
		case IMPLIED: implied(p); break;
	}
}