#include "model.h"
#include "parameter.h"

void model(Parameter p){
	SizeOptions opt("Magic sequence");
	opt.size(p.i("size"));

	Script::run<Model,DFS,SizeOptions>(opt);
};


void implied(Parameter p){
	SizeOptions opt("Magic sequence - implied");
	opt.size(p.i("size"));

	Script::run<ImpliedModel,DFS,SizeOptions>(opt);
};

int main(int argc, char* argv[]){
 Parameter p;
 
 switch (p.i("model")){
	 case 0: model(p); break;
	 case 1: implied(p); 
 }

 return 0;
}