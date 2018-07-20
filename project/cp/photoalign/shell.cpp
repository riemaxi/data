#include "relation.h"
#include "model.h"
#include "parameter.h"


void run(Parameter p){
	Options opt("Photo align");
	opt.solutions(p.i("solutions",0));
	
	IntMinimizeScript::run<Model,BAB,Options>(opt);
};


int main(int argc, char* argv[]){
 Parameter p;
 run(p);
}