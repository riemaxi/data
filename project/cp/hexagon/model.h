#include <gecode/int.hh>
#include <gecode/driver.hh>
#include <gecode/minimodel.hh>

using namespace Gecode;

#define ROWS 5
#define COLS 9
#define MIN 1
#define MAX 19
#define UPPER 5*MAX - 10
#define LOWER 3*MIN + 3
#define TOTAL MAX*(MAX+1)/2
#define THIRTY_EIGHT 38


class Hexagon{
private:
	int start[6];
	int diag[19];
	int adiag[19];
protected:
	IntVarArray x;
public:
	Hexagon(IntVarArray& source):
		x(source),
		start{0,3,7,12,16,19},
		diag{2,6,11,1,5,10,15,0,4,9,14,18,3,8,13,17,7,12,16},
		adiag{0,3,7,1,4,8,12,2,5,9,13,16,6,10,14,17,11,15,18}{
	}
	
	int rowc(){
		return 5;
	}
	
	IntVarArgs row(int r){
			IntVarArgs v;
			for(int c=start[r]; c<start[r+1]; v << x[c++]);
			
			return v;
	}
	
	IntVarArgs diagonal(int r){
		IntVarArgs v;
		for(int c = start[r]; c<start[r+1]; v << x[diag[c++]] );
		
		return v;
	}
	
	IntVarArgs adiagonal(int r){
		IntVarArgs v;
		for(int c = start[r]; c<start[r+1]; v << x[adiag[c++]] );
		
		return v;
	}
	
};

class HexagonPrinter{
public:
	static void print(IntVarArray x, std::ostream& os){
		os << "=======================" << std::endl;

		Hexagon h(x);
		for(int r=0; r<h.rowc(); r++){
			IntVarArgs row = h.row(r);
			for(int c=0;c<row.size(); c++)
				os << row[c] << " ";
			
			os << std::endl;
		}
	}
};


class Model : public Script{
protected:
	IntVarArray x;
public:
	Model(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){
		
		Hexagon hxgn(x);

		//Constraint on rows		
		for(int i=0; i<hxgn.rowc(); i++)
			linear(*this, hxgn.row(i), IRT_EQ, THIRTY_EIGHT);
		

		//Constraint on diagonals
		for(int i=0; i<hxgn.rowc(); i++)
			linear(*this, hxgn.diagonal(i), IRT_EQ, THIRTY_EIGHT);
		
		
		//Constraint on anti diagonals
		for(int i=0; i<hxgn.rowc(); i++)
			linear(*this, hxgn.adiagonal(i), IRT_EQ, THIRTY_EIGHT);
		
		distinct(*this, x);
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN() );
	}
	
	Model(Model& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new Model(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::print(x,  os);
	}
	
};

class SBModel : public Script{
protected:
	IntVarArray x;
public:
	SBModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){
		
		Hexagon hxgn(x);

		//Constraint on rows		
		for(int i=0; i<hxgn.rowc(); i++)
			linear(*this, hxgn.row(i), IRT_EQ, THIRTY_EIGHT);
		

		//Constraint on diagonals
		for(int i=0; i<hxgn.rowc(); i++)
			linear(*this, hxgn.diagonal(i), IRT_EQ, THIRTY_EIGHT);
		
		
		//Constraint on anti diagonals
		for(int i=0; i<hxgn.rowc(); i++)
			linear(*this, hxgn.adiagonal(i), IRT_EQ, THIRTY_EIGHT);
		
		distinct(*this, x);
		
		//Symmetry breaking
		
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN() );
	}
	
	SBModel(SBModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new SBModel(*this);
	}

};