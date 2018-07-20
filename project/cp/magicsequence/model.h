
#include <gecode/driver.hh>
#include <gecode/int.hh>
#include <gecode/minimodel.hh>

using namespace Gecode;

#define HOME *this

class Model : public Script{
protected:
	IntVarArray x;
public:
	Model(const SizeOptions& opt):
		Script(opt),
		x(HOME, opt.size(), 0, opt.size() - 1){
			
		for(int i=0; i<x.size(); i++)
			count(HOME, x, i, IRT_EQ, x[i]);
		
		branch(HOME, x, INT_VAR_NONE(), INT_VAL_MAX());
	}
	
	Model(Model& model):Script(model){
		x.update(HOME, model.x);
	}
	
	virtual Space* copy(void){
		return new Model(HOME);
	}
};

class ImpliedModel : public Script{
protected:
	IntVarArray x;
public:
	ImpliedModel(const SizeOptions& opt):
		Script(opt),
		x(HOME, opt.size(), 0, opt.size() - 1){
			
		for(int i=0; i<x.size(); i++)
			count(HOME, x, i, IRT_EQ, x[i]);

		//Begin implication
		linear(HOME, x, IRT_EQ, opt.size());
		linear(HOME, IntArgs::create(opt.size(), -1, 1), x , IRT_EQ, 0);
		//End implication
		
		branch(HOME, x, INT_VAR_NONE(), INT_VAL_MAX());
	}
	
	ImpliedModel(ImpliedModel& model):Script(model){
		x.update(HOME, model.x);
	}
	
	virtual Space* copy(void){
		return new ImpliedModel(HOME);
	}
};