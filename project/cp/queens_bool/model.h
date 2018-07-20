#include <gecode/int.hh>
#include <gecode/minimodel.hh>

using namespace Gecode;

#define HOME *this

class Model : public Space{
protected:
 IntVarArray x;
public:
 Model(const int size)
  :x(HOME, size*size, 0, 1){

  Matrix<IntVarArgs> m(x, size, size);

  for(int p=0; p<size-1; p++){
   IntVarArgs piv = m.row(p);

   //Only one 1 in the row
   linear(HOME, piv, IRT_EQ, 1);

   for(int r=p+1; r<size; r++){
    IntVarArgs row = m.row(r);

    //Only one 1 in the row
    linear(HOME, row, IRT_EQ, 1);

    //position in piv between 0 and 2^(size-1)
    IntVar pp(HOME,0,1 << (size-1));

    //position in pr between 0 and 2^(size-1)
    IntVar pr(HOME,0,1 << (size-1));

    //avoid the right triangle
    IntVar diff = expr(HOME, abs(pp - pr) );
    rel(HOME, expr(HOME, diff != 0 && diff != r-p), IRT_EQ, 1);

    //it must exist a 1 at pp in piv
    element(HOME, piv, pp, 1);
    //it must exist a 1 at pr in row
    element(HOME, row, pr, 1);

   }
  }
  branch(HOME, x, INT_VAR_NONE(), INT_VAL_MIN());
 }

 Model(Model& s)
  :Space(s){
   x.update(HOME, s.x);
 }

 virtual Space* copy(){
  return new Model(HOME);
 }
 
  IntVarArray solution(){
	  return x;
  }
};
