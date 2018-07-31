#include "model.h"
#include "parameter.h"

void valuemin(Parameter p){
	std::cout << "model: value min" << std::endl;		
	SizeOptions opt("hexagon");	
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<ValueMinModel,DFS,SizeOptions>(opt);
};


void valuemax(Parameter p){
	std::cout << "model: value max" << std::endl;		
	SizeOptions opt("hexagon");		
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<ValueMaxModel,DFS,SizeOptions>(opt);
};

void valuernd(Parameter p){
	std::cout << "model: value rnd" << std::endl;		
	SizeOptions opt("hexagon");	
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<ValueRndModel,DFS,SizeOptions>(opt);
};


void boundmin(Parameter p){
	std::cout << "model: bound min" << std::endl;		
	SizeOptions opt("hexagon");	
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<BoundMinModel,DFS,SizeOptions>(opt);
};

void boundmax(Parameter p){
	std::cout << "model: bound max" << std::endl;		
	SizeOptions opt("hexagon");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<BoundMaxModel,DFS,SizeOptions>(opt);
};

void boundrnd(Parameter p){
	std::cout << "model: bound rnd" << std::endl;		
	SizeOptions opt("hexagon");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<BoundRndModel,DFS,SizeOptions>(opt);
};


void domainmin(Parameter p){
	std::cout << "model: domain min" << std::endl;		
	SizeOptions opt("hexagon");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<DomainMinModel,DFS,SizeOptions>(opt);
};


void domainmax(Parameter p){
	std::cout << "model: domain max" << std::endl;		
	SizeOptions opt("hexagon");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<DomainMaxModel,DFS,SizeOptions>(opt);
};

void domainrnd(Parameter p){
	std::cout << "model: domain rnd" << std::endl;
	SizeOptions opt("hexagon");
	opt.solutions(p.i("solutions"));
	opt.time(p.i("timeout"));
	
	Script::run<DomainRndModel,DFS,SizeOptions>(opt);
};

int main(int argc, char* argv[]){
 Parameter p;

 valuemin(p); 
 valuemax(p); 
 valuernd(p); 
 
 boundmin(p);
 boundmax(p);
 boundrnd(p);
 
 domainmin(p);
 domainmax(p);
 domainrnd(p); 
 
 return 0;
}