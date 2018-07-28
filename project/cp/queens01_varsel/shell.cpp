#include "model.h"
#include "parameter.h"

 
void none(Parameter p){
	for(int size=8;  size < p.i("max"); size += 5){
		std::cout << "model: none" << std::endl;		
		std::string title = "size : " + std::to_string(size);
		SizeOptions opt(title.c_str());
		opt.size(size);
		opt.solutions(p.i("solutions"));
		opt.time(p.i("timeout"));
		
		Script::run<Model,DFS,SizeOptions>(opt);
	}
};


void random(Parameter p){
	for(int size=8;  size < p.i("max"); size += 5){
		std::cout << "model: random" << std::endl;		
		std::string title = "size : " + std::to_string(size);
		SizeOptions opt(title.c_str());
		opt.size(size);
		opt.solutions(p.i("solutions"));
		opt.time(p.i("timeout"));
		
		Script::run<RandomModel,DFS,SizeOptions>(opt);
	}
};

void minmin(Parameter p){
	for(int size=8;  size < p.i("max"); size += 5){
		std::cout << "model: min min" << std::endl;
		std::string title = "size : " + std::to_string(size);
		SizeOptions opt(title.c_str());
		opt.size(size);
		opt.solutions(p.i("solutions"));
		opt.time(p.i("timeout"));
		
		Script::run<MinMinModel,DFS,SizeOptions>(opt);
	}
};

void minmax(Parameter p){
	for(int size=8;  size < p.i("max"); size += 5){
		std::cout << "model: min max" << std::endl;
		std::string title = "size : " + std::to_string(size);
		SizeOptions opt(title.c_str());
		opt.size(size);
		opt.solutions(p.i("solutions"));
		opt.time(p.i("timeout"));
		
		Script::run<MinMaxModel,DFS,SizeOptions>(opt);
	}
};


int main(int argc, char* argv[]){
 Parameter p;
 
 none(p);
 random(p);
 minmin(p);
 minmax(p);
 
 return 0;
}