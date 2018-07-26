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
  MatrixModel(const SizeOptions& opt):Script(opt),
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

class SBMatrixModel : public Script{
protected:
 IntVarArray x;
 
public:
  SBMatrixModel(const SizeOptions& opt):Script(opt),
	x(*this, opt.size() * opt.size(), 0, 1){
	const int size = opt.size();
	
	//Constraint 1 per row and 1 per column
	Matrix<IntVarArgs> m(x, size, size);
	for(int i=0; i < size; i++){
		linear(*this, m.row(i), IRT_EQ, 1);
		linear(*this, m.col(i), IRT_EQ, 1);
	}
	
	//Right triangles
	for(int ra=0; ra<size; ra++)
		for(int rb=(ra+1)%size; ra!=rb; rb=(rb+1)%size)
			for(int ca=0; ca<size; ca++)
				for(int cb=(ca+1)%size; ca!=cb; cb=(cb+1)%size)
					if ( abs(ra-rb) == abs(ca-cb) )
						rel(*this, m(ra,ca) + m(rb,cb) < 2);
				
	//Symmetry breaking
	IntVarArgs rows;
	IntVarArgs cols;
	for(int i=0; i<size;i++){
		rows << m.row(i);
		cols << m.col(i);
	}
	
	Symmetries sym;
	sym << VariableSequenceSymmetry(rows, size) << VariableSequenceSymmetry(cols, size);
			
			
	branch(*this, x, INT_VAR_NONE(), INT_VAL_MIN(), sym);
	
  }
 
  SBMatrixModel(SBMatrixModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new SBMatrixModel(*this);
  }
  
  IntVarArray solution(){
	   return x;
   }
};


class MatrixPrinterModel : public Script{
protected:
 IntVarArray x;
 
public:
  MatrixPrinterModel(const SizeOptions& opt):Script(opt),
	x(*this, opt.size() * opt.size(), 0, 1){
	const int size = opt.size();
	
	//Constraint 1 per row and 1 per column
	Matrix<IntVarArgs> m(x, size, size);
	for(int i=0; i < size; i++){
		linear(*this, m.row(i), IRT_EQ, 1);
		linear(*this, m.col(i), IRT_EQ, 1);
	}
	
	//Avoid right triangles
	for(int ra=0; ra<size; ra++)
		for(int rb=(ra+1)%size; ra!=rb; rb=(rb+1)%size)
			for(int ca=0; ca<size; ca++)
				for(int cb=(ca+1)%size; ca!=cb; cb=(cb+1)%size)
					if ( abs(ra-rb) == abs(ca-cb) )
						rel(*this, m(ra,ca) + m(rb,cb) < 2);
					
			
	branch(*this, x, INT_VAR_NONE(), INT_VAL_MIN() );
	
  }
 
  MatrixPrinterModel(MatrixPrinterModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new MatrixPrinterModel(*this);
  }
   
	virtual void print(std::ostream& os) const { 
		os << "=======================" << std::endl;
		
		int size = sqrt(x.size());
		for(int i=0; i<size;i++){
			os << x[size*i];
			for(int j=1; j<size; j++)
				os << ' ' << x[size*i + j];
			os << std::endl;
		}
	}
	
};


class SBMatrixPrinterModel : public Script{
protected:
 IntVarArray x;
 
public:
  SBMatrixPrinterModel(const SizeOptions& opt):Script(opt),
	x(*this, opt.size() * opt.size(), 0, 1){
	const int size = opt.size();
	
	//Constraint 1 per row and 1 per column
	Matrix<IntVarArgs> m(x, size, size);
	for(int i=0; i < size; i++){
		linear(*this, m.row(i), IRT_EQ, 1);
		linear(*this, m.col(i), IRT_EQ, 1);
	}

	//Avoid right triangles
	for(int ra=0; ra<size; ra++)
		for(int rb=(ra+1)%size; ra!=rb; rb=(rb+1)%size)
			for(int ca=0; ca<size; ca++)
				for(int cb=(ca+1)%size; ca!=cb; cb=(cb+1)%size)
					if ( abs(ra-rb) == abs(ca-cb) )
						rel(*this, m(ra,ca) + m(rb,cb) < 2);
					
			
	//Symmetry breaking
	IntVarArgs rows;
	IntVarArgs cols;
	for(int i=0; i<size;i++){
		rows << m.row(i);
		cols << m.col(i);
	}
	
	Symmetries sym;
	sym << VariableSequenceSymmetry(rows, size) << VariableSequenceSymmetry(cols, size);
			
			
	branch(*this, x, INT_VAR_NONE(), INT_VAL_MIN(), sym);

  }
 
  SBMatrixPrinterModel(SBMatrixPrinterModel& m):Script(m){
	  x.update(*this, m.x);
  }
  
  virtual Space* copy(void){
	  return new SBMatrixPrinterModel(*this);
  }
   
	virtual void print(std::ostream& os) const { 
		os << "=======================" << std::endl;
		
		int size = sqrt(x.size());
		for(int i=0; i<size;i++){
			os << x[size*i];
			for(int j=1; j<size; j++)
				os << ' ' << x[size*i + j];
			os << std::endl;
		}
	}
	
};
