#include <iostream>
#include <fstream>
#include <string>
#include <map>

using namespace std;  

class BTable{
private:
	map<string,string> data;
	
public:
	BTable(string src, string ctx, string sep = "\t", string comment = "#"){
		ifstream file( (src).c_str());
		if (file.is_open()){
		string line;
		while (getline(file,line)){
			add(trim(line), ctx, sep);
		}
		file.close();
		}
	}
	
	string trim(string str){
		if (str.length()==0)
			return str;

		int pos = str.find_first_not_of(" ");
		return str.substr(pos);
	}

	void add(string line, string ctx, string sep = "\t"){
		int pos = line.find(sep);
		string ctx =  line.substr(0,pos);
		string pair = trim(line.substr(pos+1));
		
		pos = pair.find(sep);
		string id = pair.substr(0,pos);
		string value = trim(pair.substr(pos+1));
		
		data[ctx + id] = value;
	}
	
	string get(string ctx, string id, string defval = ""){
		try{
			return data.at(ctx + id);
		}catch(...){
			return defval;
		}
	}

	string get(string ctx, int id, string defval = ""){
		try{
			return get(ctx, std::to_string(id));
		}catch(...){
			return defval;
		}
	}
	
	int size(string ctx){
		int count = 0;
		for(map<string,string>::iterator it = data.begin(); it!=data.end(); ++it){
			count += (it->first.compare(0, ctx.length(), ctx) == 0) ? 1 : 0;
		}
		return count;
	}
	
	//Iteration
	typedef map<string, string>::iterator iterator;
	typedef map<string, string>::const_iterator const_iterator;
	
	iterator begin(){ return data.begin(); }
	iterator end(){ return data.end(); }
	
};