
#include <gecode/int.hh>
#include <gecode/driver.hh>
#include <gecode/minimodel.hh>

using namespace Gecode;

#define HOME *this

class Model : public IntMinimizeScript{
protected:
	IntVarArray m;
public:
	Model(const SizeOptions& opt):
		IntMinimizeScript(opt),
		m(HOME, opt.size(), 0, opt.size() < 31 ? (1 << opt.size() - 1) - 1 : Int::Limits::max){
		
		
		//Constraint on marks
		rel(HOME, m[0], IRT_EQ, 0);
		rel(HOME, m, IRT_LE);
		
		//Distance constraint
		const int n = opt.size();
		const int d_n = n*(n - 1)/2;

		IntVarArgs d(d_n);
		for(int k=0, i=0; i<n-1; i++)
			for(int j = i + 1; j<n; j++,k++){
				d[k] = expr(HOME, m[j] - m[i]);
				rel(HOME, d[k], IRT_GQ, (j-i)*(j-i+1)/2);
			}
				
			
		distinct(HOME, d, IPL_BND);
		
		//Symmetry breaking
		if (n>2)
			rel(HOME, d[0], IRT_LE, d[d_n-1]);
		
		branch(HOME, m, INT_VAR_NONE(), INT_VAL_MIN());
	}
	
	Model(Model& model):IntMinimizeScript(model){
		m.update(HOME, model.m);
	}
	
	virtual Model* copy(void){
		return new Model(HOME);
	}
	
	virtual IntVar cost(void) const{
		return m[m.size()-1];
	}
};