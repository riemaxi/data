#include <iostream>
#include <fstream>
#include <string>
#include <list>
#include <vector>

using namespace std;  

class Record : public vector<string>{
private:
	string trim(string str){
		if (str.length()==0)
			return str;

		int pos = str.find_first_not_of(" ");
		return str.substr(pos);
	}

public:
	Record(string left, int pos, string sep){
		while (left.size()>0){
			pos = left.find(sep);
			if (pos == -1){
				push_back(left);
				left = "";
			}
			else{
				push_back(left.substr(0, pos) );
				left = trim(left.substr(pos + 1));
			}
		}
	}
	
	int i(int i){
		return std::atoi(at(i).c_str());
	}
	
	string s(int i){
		return at(i);
	}
};

class Relation{
private:
	list<Record> data;

public:
	Relation(string src, string ctx, string sep = "\t", string comment = "#"){
		ifstream file( (src).c_str());
		if (file.is_open()){
		string line;
		while (getline(file,line)){
			add(trim(line), ctx, sep);
		}
		file.close();
		}
	}
	
	void add(string line, string ctx, string sep = "\t"){
		int pos = line.find(sep);
		if (line.substr(0,pos) == ctx)
			data.push_back(Record(trim(line.substr(pos + 1)), pos, sep));
	}
	
	string trim(string str){
		if (str.length()==0)
			return str;

		int pos = str.find_first_not_of(" ");
		return str.substr(pos);
	}
	
	
	int size(){
		return data.size();
	}
	
	//Iteration
	typedef list<Record>::iterator iterator;
	typedef list<Record>::const_iterator const_iterator;
	
	iterator begin(){ return data.begin(); }
	iterator end(){ return data.end(); }
};