#include "model.h"
#include "parameter.h"

 
void rndrnd(Parameter p){
	for(int size=8;  size <= p.i("max"); size += 5){
		std::cout << "model: rnd rnd" << std::endl;		
		std::string title = "size : " + std::to_string(size);
		SizeOptions opt(title.c_str());
		opt.size(size);
		opt.solutions(p.i("solutions"));
		opt.time(p.i("timeout"));
		
		Script::run<RndRndModel,DFS,SizeOptions>(opt);
	}
};

void rndmin(Parameter p){
	for(int size=8;  size <= p.i("max"); size += 5){
		std::cout << "model: rnd min" << std::endl;		
		std::string title = "size : " + std::to_string(size);
		SizeOptions opt(title.c_str());
		opt.size(size);
		opt.solutions(p.i("solutions"));
		opt.time(p.i("timeout"));
		
		Script::run<RndMinModel,DFS,SizeOptions>(opt);
	}
};


void minrnd(Parameter p){
	for(int size=8;  size <= p.i("max"); size += 5){
		std::cout << "model: min rnd" << std::endl;		
		std::string title = "size : " + std::to_string(size);
		SizeOptions opt(title.c_str());
		opt.size(size);
		opt.solutions(p.i("solutions"));
		opt.time(p.i("timeout"));
		
		Script::run<MinRndModel,DFS,SizeOptions>(opt);
	}
};

void rndmax(Parameter p){
	for(int size=8;  size <= p.i("max"); size += 5){
		std::cout << "model: rnd max" << std::endl;		
		std::string title = "size : " + std::to_string(size);
		SizeOptions opt(title.c_str());
		opt.size(size);
		opt.solutions(p.i("solutions"));
		opt.time(p.i("timeout"));
		
		Script::run<RndMaxModel,DFS,SizeOptions>(opt);
	}
};


void maxrnd(Parameter p){
	for(int size=8;  size <= p.i("max"); size += 5){
		std::cout << "model: max rnd" << std::endl;		
		std::string title = "size : " + std::to_string(size);
		SizeOptions opt(title.c_str());
		opt.size(size);
		opt.solutions(p.i("solutions"));
		opt.time(p.i("timeout"));
		
		Script::run<MaxRndModel,DFS,SizeOptions>(opt);
	}
};


int main(int argc, char* argv[]){
 Parameter p;
 
 rndrnd(p);
 rndmin(p);
 minrnd(p);
 rndmax(p);
 maxrnd(p);
 
 return 0;
}