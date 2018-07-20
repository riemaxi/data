#include "model.h"
#include "parameter.h"

void run(Parameter p){
	SizeOptions opt("Golomb");
	opt.size(p.i("size"));

	IntMinimizeScript::run<Model,BAB,SizeOptions>(opt);
};


int main(int argc, char* argv[]){
 Parameter p;
 run(p);

 return 0;
}