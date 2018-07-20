
#include "model.h"
#include "parameter.h"

 void print(IntVarArray x, int size){
	std::cout << std::endl;
	for(int i = 0; i<size; i++){
		std::cout << x[size*i];
		for(int j = 1; j<size; j++)
			std::cout << x[size*i + j];
		std::cout << std::endl;

	}
		
 };


int main(int argc, char* argv[]){
 Parameter p;
 int size = p.i("size");
 
 Model* model = new Model(size); 
 DFS<Model> dfs(model);
 delete model;
 
 while(Model* model = dfs.next()){
   print(model->solution(), size); delete model;
 }

 return 0;
}