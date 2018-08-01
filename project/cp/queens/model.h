#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/driver.hh>

using namespace Gecode;

class Model : public Script{
protected:
 IntVarArray x;

public:
 Model(const SizeOptions& opt):Script(opt), x(*this, opt.size(), 0, opt.size() - 1){
	const int size = opt.size();
	for (int i = 0; i<size; i++)
		for (int j = i+1; j<size; j++) {
			rel(*this, x[i] != x[j]);
			rel(*this, x[i]+i != x[j]+j);
			rel(*this, x[i]-i != x[j]-j);
	};
	branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN());
 }
 
  Model(Model& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new Model(*this);
  }
  
  IntVarArray solution(){
	   return x;
  }
};
