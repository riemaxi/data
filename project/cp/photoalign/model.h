#include <gecode/int.hh>
#include <gecode/driver.hh>
#include <gecode/minimodel.hh>

using namespace Gecode;

#define HOME *this

Relation names("model.dat","n");
Relation pref("model.dat","p");

class Model : public IntMinimizeScript{
protected:
	IntVarArray pos;
	IntVar violations;
public:
	Model(const Options opt):
		IntMinimizeScript(opt),
		pos(HOME, names.size(), 0, names.size()-1),
		violations(HOME, 0, pref.size()){
			
		distinct(HOME, pos, IPL_BND);
		
		BoolVarArgs viol(pref.size());
		int i = 0;
		for(Relation::iterator it = pref.begin(); it!=pref.end(); ++it, i++){
			Record r = *it;
			viol[i] = expr(HOME, abs(pos[r.i(0)] - pos[r.i(1)]) > 1);
		}
		rel(HOME, violations == sum(viol));
		
		//Symmetry breaking
		rel(HOME, pos[0] < pos[1]);
		
		branch(HOME, pos, INT_VAR_NONE(), INT_VAL_MIN());
		
		
	}
	
	virtual IntVar cost(void) const{
		return violations;
	}
	
	Model(Model& model):IntMinimizeScript(model){
		pos.update(HOME, model.pos);
		violations.update(HOME, model.violations);
	}
	
	virtual Space* copy(void){
		return new Model(HOME);
	}
	
	
};