#include "model.h"
#include "parameter.h"

void run(Parameter p){
	for(int size = p.i("startsize"); size <= p.i("maxsize"); size += 5){
		for(int i=1; i<=p.i("runs");i++){		
			std::cout << "run: " << i << std::endl;
			std::cout << "size: " << size << std::endl;
			SizeOptions opt("queens");
			opt.size(size);
			opt.solutions(p.i("solutions"));
			opt.time(p.i("timeout"));
			
			Script::run<Model,DFS,SizeOptions>(opt);
		}
	}
};

int main(int argc, char* argv[]){
 Parameter p;

 run(p); 
 
 return 0;
}