#include <gecode/int.hh>
#include <gecode/driver.hh>
#include <gecode/minimodel.hh>
#include <map>

using namespace Gecode;

#define ROWS 5
#define COLS 9
#define MIN 1
#define MAX 19
#define UPPER 5*MAX - 10
#define LOWER 3*MIN + 3
#define TOTAL MAX*(MAX+1)/2
#define THIRTY_EIGHT 38
#define THREE 3


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
	static void pad(int c, std::ostream& os, std::string pads = " "){
		for(int i=0;i<c; i++)
			os << pads;
	}
	
	static void print(IntVarArray x, std::ostream& os){
		pad(15,os, "=");
		os << std::endl;

		Hexagon h(x);
		for(int r=0, padc=2; r<h.rowc(); r++, padc = padc + (r<=2?-1:1)){
			pad(padc, os);
			IntVarArgs row = h.row(r);
			for(int c=0;c<row.size(); c++)
				os << row[c] << "  ";
			
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
};

class PrinterModel : public Script{
protected:
	IntVarArray x;
public:
	PrinterModel(const SizeOptions& opt): Script(opt), 
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
	
	PrinterModel(PrinterModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new PrinterModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::print(x,  os);
	}
	
};


class ImpliedModel : public Script{
protected:
	IntVarArray x;
public:
	ImpliedModel(const SizeOptions& opt): Script(opt), 
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
		
		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN() );
	}
	
	ImpliedModel(ImpliedModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new ImpliedModel(*this);
	}
};


class PrinterImpliedModel : public Script{
protected:
	IntVarArray x;
public:
	PrinterImpliedModel(const SizeOptions& opt): Script(opt), 
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
		
		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN() );
	}
	
	PrinterImpliedModel(PrinterImpliedModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new PrinterImpliedModel(*this);
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
		Symmetries sym;
/*		IntVarArgs rsym1;
		rsym1 << 	hxgn.row(0) << hxgn.row(4);
		sym << VariableSequenceSymmetry(rsym1,2);
		
		IntVarArgs rsym2;
		rsym2 << hxgn.row(1) << hxgn.row(3); 
		sym << VariableSequenceSymmetry(rsym2,2);


		IntVarArgs dsym1;
		dsym1 << 	hxgn.diagonal(0) << hxgn.diagonal(4);
		sym << VariableSequenceSymmetry(dsym1,2);
		
		IntVarArgs dsym2;
		dsym2 << hxgn.diagonal(1) << hxgn.diagonal(3); 
		sym << VariableSequenceSymmetry(dsym2,2);
		
		IntVarArgs adsym1;
		adsym1 << hxgn.adiagonal(0) << hxgn.adiagonal(4);
		sym << VariableSequenceSymmetry(adsym1,2);
		
		IntVarArgs adsym2;
		adsym2 << hxgn.adiagonal(1) << hxgn.adiagonal(3); 
		sym << VariableSequenceSymmetry(adsym2,2);*/
		
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN(), sym );
	}
	
	SBModel(SBModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new SBModel(*this);
	}

};

