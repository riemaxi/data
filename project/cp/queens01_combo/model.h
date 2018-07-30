#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/driver.hh>

using namespace Gecode;

class RndRndModel: public Script{
protected:
 IntVarArray x;
 
public:
  RndRndModel(const SizeOptions& opt):Script(opt),
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

	Rnd rgenvar(1U);
	Rnd rgenval(1U);
	branch(*this, x, INT_VAR_RND(rgenvar), INT_VAL_RND(rgenval));
	
  }
 
  RndRndModel(RndRndModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new RndRndModel(*this);
  }
};

class RndMinModel: public Script{
protected:
 IntVarArray x;
 
public:
  RndMinModel(const SizeOptions& opt):Script(opt),
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
 
  RndMinModel(RndMinModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new RndMinModel(*this);
  }
 };

 class MinRndModel: public Script{
protected:
 IntVarArray x;
 
public:
  MinRndModel(const SizeOptions& opt):Script(opt),
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
	branch(*this, x, INT_VAR_MAX_MIN(), INT_VAL_RND(rgen));
	
  }
 
  MinRndModel(MinRndModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new MinRndModel(*this);
  }
 };

class RndMaxModel: public Script{
protected:
 IntVarArray x;
 
public:
  RndMaxModel(const SizeOptions& opt):Script(opt),
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
	branch(*this, x, INT_VAR_RND(rgen), INT_VAL_MAX());
	
  }
 
  RndMaxModel(RndMaxModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new RndMaxModel(*this);
  }
 };

 class MaxRndModel: public Script{
protected:
 IntVarArray x;
 
public:
  MaxRndModel(const SizeOptions& opt):Script(opt),
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
	branch(*this, x, INT_VAR_MAX_MAX(), INT_VAL_RND(rgen));
	
  }
 
  MaxRndModel(MaxRndModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new MaxRndModel(*this);
  }
 };
 