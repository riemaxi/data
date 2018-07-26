#include "model.h"
#include "parameter.h"

 void print(IntVarArray x, int size){
	std::cout << std::endl;
	for(int i = 0; i<size; i++){
		std::cout << (x[i].val() == 0) ? 1 : 0;
		for(int j = 1; j<size; j++)
			std::cout << " " << (x[i].val() == j) ? 1 : 0;
		std::cout << std::endl;

	}
		
};

void standard(Parameter p){
 
	SizeOptions opt("Queens-standard");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	opt.size(p.i("size"));
	
	Script::run<Model,DFS,SizeOptions>(opt);	
};


void distinct(Parameter p){
	SizeOptions opt("Queens-distinct");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	opt.size(p.i("size"));
	
	Script::run<DistinctModel,DFS,SizeOptions>(opt);	
};

void mixed(Parameter p){
	SizeOptions opt("Queens-mixed");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	opt.size(p.i("size"));
	
	Script::run<MixedModel,DFS,SizeOptions>(opt);	
};

void matrix(Parameter p){
	SizeOptions opt("Queens-matrix");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	opt.size(p.i("size"));

	if (p.i("print"))
		if (p.b("break"))
			Script::run<SBMatrixPrinterModel,DFS,SizeOptions>(opt);
		else
			Script::run<MatrixPrinterModel,DFS,SizeOptions>(opt);
	else
		if (p.b("break"))
			Script::run<SBMatrixModel,DFS,SizeOptions>(opt);
		else
			Script::run<MatrixModel,DFS,SizeOptions>(opt);
	
};


#define STANDARD 0
#define DISTINCT 1
#define MIXED 2
#define MATRIX 3

int main(int argc, char* argv[]){
 Parameter p;
  
 switch (p.i("mode")){
	 case STANDARD : standard(p); break;
	 case DISTINCT : distinct(p); break;
	 case MIXED : mixed(p); break;
	 case MATRIX : matrix(p);
 }

 return 0;
}