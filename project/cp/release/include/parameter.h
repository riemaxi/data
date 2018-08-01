#include <iostream>
#include <fstream>
#include <string>
#include <map>

#define PARAMETER "model.par"
#define SEPARATOR ":"
#define COMMENT "#"

using namespace std;

class Pair{
public:
 string key;
 string value;
};

class Parameter{
protected:
 map<string,string> data;

 int pairpos(string line, string ctx, string comment){
  if (line.length() == 0)
   return -1;

  int pos = line.find(comment);
  if (pos == 0)
   return -1;

  pos = line.find(ctx);
  if (pos == string::npos)
   return -1;

  return pos;
  
 }
public:
 Parameter(string app = "", string ctx = "", string sep = SEPARATOR, string comment = COMMENT){
  ifstream file( (app + PARAMETER).c_str());
  if (file.is_open()){
   string line;
   while (getline(file,line)){
    line = trim(line);
    int pos = pairpos(line,ctx, comment);
	if (pos != -1){
     add(line.substr(pos + ctx.length()), sep);
    }
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

 void add(string line, string sep = SEPARATOR){
  int pos = line.find(sep);

  string key =  line.substr(0,pos);
  string value = trim(line.substr(pos+1));

  data[key] = value;
 }

 string get(string key, string defval = ""){
  try{
   return data.at(key);
  }catch(...){
   return defval;
  }
 }

 string operator[](string key){
  return get(key);
 }

 std::string operator()(std::string key, std::string defval = ""){
  return get(key,defval);
 }

 int i(std::string key, int defval = 0){
  string val = get(key);
  return val != "" ? std::atoi(val.c_str()) : defval;
 }

 bool b(std::string key){
  return i(key) != 0;
 }

 float f(string key, float defval = 0.0){
  const char* val = get(key).c_str();
  return val != "" ? std::atof(val) : defval;
 }

};
