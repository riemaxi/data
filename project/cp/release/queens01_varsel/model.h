
#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/driver.hh>

using namespace Gecode;

class Model: public Script{
protected:
 IntVarArray x;
 
public:
  Model(const SizeOptions& opt):Script(opt),
	x(*this, opt.size() * opt.size(), 0, 1){
	const int size = opt.size();
	
	//Constraint 1 per row and 1 per column
	Matrix<IntVarArgs> m(x, size, size);
	for(int i=0; i < size; i++){
		linear(*this, m.row(i), IRT_EQ, 1);
		linear(*this, m.col(i), IRT_EQ, 1);
	}
	
	for(int ra=0; ra<size; ra++)
		for(int rb=(ra+1)%size; ra!=rb; rb=(rb+1)%size)
			for(int ca=0; ca<size; ca++)
				for(int cb=(ca+1)%size; ca!=cb; cb=(cb+1)%size)
					if ( abs(ra-rb) == abs(ca-cb) )
						rel(*this, m(ra,ca) + m(rb,cb) < 2);

	branch(*this, x, INT_VAR_NONE(), INT_VAL_MIN());
	
  }
 
  Model(Model& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new Model(*this);
  }
 };

 class RandomModel: public Script{
protected:
 IntVarArray x;
 
public:
  RandomModel(const SizeOptions& opt):Script(opt),
	x(*this, opt.size() * opt.size(), 0, 1){
	const int size = opt.size();
	
	//Constraint 1 per row and 1 per column
	Matrix<IntVarArgs> m(x, size, size);
	for(int i=0; i < size; i++){
		linear(*this, m.row(i), IRT_EQ, 1);
		linear(*this, m.col(i), IRT_EQ, 1);
	}
	
	for(int ra=0; ra<size; ra++)
		for(int rb=(ra+1)%size; ra!=rb; rb=(rb+1)%size)
			for(int ca=0; ca<size; ca++)
				for(int cb=(ca+1)%size; ca!=cb; cb=(cb+1)%size)
					if ( abs(ra-rb) == abs(ca-cb) )
						rel(*this, m(ra,ca) + m(rb,cb) < 2);
				
	Rnd rgen(1U);
	branch(*this, x, INT_VAR_RND(rgen), INT_VAL_MIN());
	
  }
 
  RandomModel(RandomModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new RandomModel(*this);
  }
 };

class MinMinModel: public Script{
protected:
 IntVarArray x;
 
public:
  MinMinModel(const SizeOptions& opt):Script(opt),
	x(*this, opt.size() * opt.size(), 0, 1){
	const int size = opt.size();
	
	//Constraint 1 per row and 1 per column
	Matrix<IntVarArgs> m(x, size, size);
	for(int i=0; i < size; i++){
		linear(*this, m.row(i), IRT_EQ, 1);
		linear(*this, m.col(i), IRT_EQ, 1);
	}
	
	for(int ra=0; ra<size; ra++)
		for(int rb=(ra+1)%size; ra!=rb; rb=(rb+1)%size)
			for(int ca=0; ca<size; ca++)
				for(int cb=(ca+1)%size; ca!=cb; cb=(cb+1)%size)
					if ( abs(ra-rb) == abs(ca-cb) )
						rel(*this, m(ra,ca) + m(rb,cb) < 2);
				
	branch(*this, x, INT_VAR_MIN_MIN(), INT_VAL_MIN());
	
  }
 
  MinMinModel(MinMinModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new MinMinModel(*this);
  }
 };

class MinMaxModel: public Script{
protected:
 IntVarArray x;
 
public:
  MinMaxModel(const SizeOptions& opt):Script(opt),
	x(*this, opt.size() * opt.size(), 0, 1){
	const int size = opt.size();
	
	//Constraint 1 per row and 1 per column
	Matrix<IntVarArgs> m(x, size, size);
	for(int i=0; i < size; i++){
		linear(*this, m.row(i), IRT_EQ, 1);
		linear(*this, m.col(i), IRT_EQ, 1);
	}
	
	for(int ra=0; ra<size; ra++)
		for(int rb=(ra+1)%size; ra!=rb; rb=(rb+1)%size)
			for(int ca=0; ca<size; ca++)
				for(int cb=(ca+1)%size; ca!=cb; cb=(cb+1)%size)
					if ( abs(ra-rb) == abs(ca-cb) )
						rel(*this, m(ra,ca) + m(rb,cb) < 2);
				
	branch(*this, x, INT_VAR_MIN_MAX(), INT_VAL_MIN());
	
  }
 
  MinMaxModel(MinMaxModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new MinMaxModel(*this);
  }
 };
