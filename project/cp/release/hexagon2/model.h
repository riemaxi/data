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

int sol_index;

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
	
	static void printstring(IntVarArray x, std::ostream& os){
		if (sol_index == 0){
			std::string LETTER = "ABCDEFGHIJKLMNOPQRS";
			os << "first: ";
			for(int i=0; i<x.size(); i++)
				os << LETTER[x[i].val()-1];
			sol_index += 1;
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
		
		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
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

class ValueMinModel : public Script{
protected:
	IntVarArray x;
public:
	ValueMinModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){
			
		sol_index = 0;
		
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
		
		distinct(*this, x, IPL_VAL);
		
		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN() );
	}
	
	ValueMinModel(ValueMinModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new ValueMinModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::printstring(x,  os);
	}
	
};

class ValueMaxModel : public Script{
protected:
	IntVarArray x;
public:
	ValueMaxModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){
			
		sol_index = 0;			
		
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
		
		distinct(*this, x, IPL_VAL);
		
		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MAX() );
	}
	
	ValueMaxModel(ValueMaxModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new ValueMaxModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::printstring(x,  os);
	}
	
};

class ValueRndModel : public Script{
protected:
	IntVarArray x;
public:
	ValueRndModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){

		sol_index = 0;
		
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
		
		distinct(*this, x, IPL_VAL);
		
		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		Rnd rgen(1U);
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_RND(rgen) );
	}
	
	ValueRndModel(ValueRndModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new ValueRndModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::printstring(x,  os);
	}
	
};


class BoundMinModel : public Script{
protected:
	IntVarArray x;
public:
	BoundMinModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){
			
		sol_index = 0;			
		
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
		
		distinct(*this, x, IPL_BND);
		
		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN() );
	}
	
	BoundMinModel(BoundMinModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new BoundMinModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::printstring(x,  os);
	}
	
};


class BoundMaxModel : public Script{
protected:
	IntVarArray x;
public:
	BoundMaxModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){
			
		sol_index = 0;			
		
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
		
		distinct(*this, x, IPL_BND);

		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MAX() );
	}
	
	BoundMaxModel(BoundMaxModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new BoundMaxModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::printstring(x,  os);
	}
	
};

class BoundRndModel : public Script{
protected:
	IntVarArray x;
public:
	BoundRndModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){
		
		sol_index = 0;		
		
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
		
		distinct(*this, x, IPL_BND);

		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		Rnd rgen(1U);
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_RND(rgen) );
	}
	
	BoundRndModel(BoundRndModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new BoundRndModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::printstring(x,  os);
	}
	
};


class DomainMinModel : public Script{
protected:
	IntVarArray x;
public:
	DomainMinModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){
		
		sol_index = 0;		
		
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
		
		distinct(*this, x, IPL_DOM);

		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MIN() );
	}
	
	DomainMinModel(DomainMinModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new DomainMinModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::printstring(x,  os);
	}
	
};

class DomainMaxModel : public Script{
protected:
	IntVarArray x;
public:
	DomainMaxModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){

		sol_index = 0;
		
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
		
		distinct(*this, x, IPL_DOM);

		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_MAX() );
	}
	
	DomainMaxModel(DomainMaxModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new DomainMaxModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::printstring(x,  os);
	}
	
};

class DomainRndModel : public Script{
protected:
	IntVarArray x;
public:
	DomainRndModel(const SizeOptions& opt): Script(opt), 
		x(*this, MAX, MIN, MAX){
		
		sol_index = 0;		
		
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
		
		distinct(*this, x, IPL_DOM);

		//Implied constraint
		rel(*this, sum(x) == TOTAL);
		
		Rnd rgen(1U);
		branch(*this, x, INT_VAR_SIZE_MIN(), INT_VAL_RND(rgen) );
	}
	
	DomainRndModel(DomainRndModel& m):Script(m){
		x.update(*this, m.x);
	}
  
	virtual Space* copy(void){
	  return new DomainRndModel(*this);
	}
	
	virtual void print(std::ostream& os) const { 
		HexagonPrinter::printstring(x,  os);
	}
	
};
