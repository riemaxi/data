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

class DistinctModel : public Script{
protected:
 IntVarArray x;
 
public:
 DistinctModel(const SizeOptions& opt):Script(opt), x(*this, opt.size(), 0, opt.size()-1){
	const int size = opt.size();
	distinct(*this, IntArgs::create(size,0,1), x);
	distinct(*this, IntArgs::create(size,0,-1), x);
	distinct(*this, x);
	
	branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN());
  }
 
  DistinctModel(DistinctModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new DistinctModel(*this);
  }
  
  IntVarArray solution(){
	   return x;
   }
};

class MixedModel : public Script{
protected:
 IntVarArray x;
 
public:
 MixedModel(const SizeOptions& opt):Script(opt),x(*this, opt.size(), 0, opt.size()-1){
	const int size = opt.size();
	for (int i = 0; i<size; i++)
		for (int j = i+1; j<size; j++) {
			rel(*this, x[i]+i != x[j]+j);
			rel(*this, x[i]-i != x[j]-j);
	};
	distinct(*this, x);
	
	branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN());
  }
 
  MixedModel(MixedModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new MixedModel(*this);
  }
  
  IntVarArray solution(){
	   return x;
   }
};

class MatrixModel : public Script{
protected:
 IntVarArray x;
 
public:
  MatrixModel(const SizeOptions& opt):Script(opt),x(*this, opt.size() * opt.size(), 0, 1){
	const int size = opt.size();
	
  Matrix<IntVarArgs> m(x, size, size);

  for(int p=0; p<size-1; p++){
   IntVarArgs piv = m.row(p);

   //Only one 1 in the row
   linear(*this, piv, IRT_EQ, 1);

   for(int r=p+1; r<size; r++){
    IntVarArgs row = m.row(r);

    //Only one 1 in the row
    linear(*this, row, IRT_EQ, 1);

    //position in piv between 0 and 2^(size-1)
    IntVar pp(*this,0,1 << (size-1));

    //position in pr between 0 and 2^(size-1)
    IntVar pr(*this,0,1 << (size-1));

    //avoid the right triangle
    IntVar diff = expr(*this, abs(pp - pr) );
    rel(*this, expr(*this, diff != 0 && diff != r-p), IRT_EQ, 1);

    //it must exist a 1 at pp in piv
    element(*this, piv, pp, 1);
    //it must exist a 1 at pr in row
    element(*this, row, pr, 1);

   }
  }
  branch(*this, x, INT_VAR_NONE(), INT_VAL_MIN());
	
  }
 
  MatrixModel(MatrixModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new MatrixModel(*this);
  }
  
  IntVarArray solution(){
	   return x;
   }
	
};