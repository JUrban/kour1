// Exploratory monomial consequences only. A failed target is not a counterexample.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

constexpr int ROOTS=12,INF=64;
using Values=std::array<std::array<uint8_t,2>,ROOTS>;
struct Rule {int r,s,k,i,j,c,index;};
struct Edge {int rule=-1,left=0,right=0;};
int valuation(int n,int p) {int v=0;while(n%p==0){n/=p;++v;}return v;}

std::array<int,2> derive(const std::vector<Rule>&rules,int root,
                        const std::vector<std::pair<int,int>>&variables,
                        int case_index,std::ostream &certificate) {
    int n=static_cast<int>(variables.size()),count=1;
    std::vector<int> stride(n),bounds(n);
    for(int d=0;d<n;++d){stride[d]=count;bounds[d]=variables[d].second;count*=bounds[d]+1;}
    std::vector<Values> values(count);
    std::vector<std::array<std::array<Edge,2>,ROOTS>> witness(count);
    for(auto &row:values)for(auto &cell:row)cell={INF,INF};
    std::map<std::pair<int,int>,std::vector<Rule>> groups;
    for(auto r:rules)groups[{r.i,r.j}].push_back(r);
    for(int code=1;code<count;++code){
        std::vector<int> exponent(n);int degree=0;
        for(int d=0;d<n;++d){exponent[d]=(code/stride[d])%(bounds[d]+1);degree+=exponent[d];}
        if(degree>=INF)throw std::runtime_error("coefficient bound insufficient");
        if(degree==1)for(int d=0;d<n;++d)if(exponent[d])values[code][variables[d].first]={0,0};
        for(const auto &entry:groups){
            int i=entry.first.first,j=entry.first.second;
            std::function<void(int,int,int)> split=[&](int d,int a,int b){
                if(d==n){
                    if(a==0||b==0)return;
                    if(a>=code||b>=code)throw std::runtime_error("nondecreasing derivation");
                    for(auto r:entry.second){
                        for(int prime=0;prime<2;++prime){
                            int cost=valuation(r.c,prime==0?2:3)+i*values[a][r.r][prime]+j*values[b][r.s][prime];
                            if(cost<values[code][r.k][prime]){
                                values[code][r.k][prime]=static_cast<uint8_t>(cost);
                                witness[code][r.k][prime]={r.index,a*ROOTS+r.r,b*ROOTS+r.s};
                            }
                        }
                    }
                    return;
                }
                for(int x=0;i*x<=exponent[d];++x){
                    int remain=exponent[d]-i*x;
                    if(remain%j==0)split(d+1,a+x*stride[d],b+(remain/j)*stride[d]);
                }
            };
            split(0,0,0);
        }
    }
    std::set<int> nodes;std::vector<int> pending={(count-1)*ROOTS+root};
    auto variable_index=[&](int code,int r){
        for(int d=0;d<n;++d)if(code==stride[d]&&r==variables[d].first)return d;
        return -1;
    };
    while(!pending.empty()){
        int key=pending.back();pending.pop_back();
        if(!nodes.insert(key).second)continue;
        int code=key/ROOTS,r=key%ROOTS;
        if(variable_index(code,r)>=0)continue;
        for(auto edge:witness[code][r]){
            if(edge.rule<0)throw std::runtime_error("uncertified node");
            pending.push_back(edge.left);pending.push_back(edge.right);
        }
    }
    certificate<<'['<<case_index<<",[";bool first_node=true;
    for(int key:nodes){
        if(!first_node)certificate<<',';
        first_node=false;
        int code=key/ROOTS,r=key%ROOTS,v=variable_index(code,r);
        certificate<<'['<<key<<','<<static_cast<int>(values[code][r][0])<<','
                   <<static_cast<int>(values[code][r][1])<<','<<v;
        for(auto edge:witness[code][r]){
            certificate<<",[";
            if(v<0)certificate<<edge.rule<<','<<edge.left<<','<<edge.right;
            certificate<<']';
        }
        certificate<<']';
    }
    certificate<<"]]\n";
    return {values.back()[root][0],values.back()[root][1]};
}

int main(int argc,char **argv){
    if(argc!=5)throw std::runtime_error("input first last certificate required");
    std::ifstream in(argv[1]);int nr;in>>nr;std::vector<Rule>rules(nr);
    for(int k=0;k<nr;++k){auto &r=rules[k];in>>r.r>>r.s>>r.k>>r.i>>r.j>>r.c;r.index=k;}
    std::ofstream certificate(argv[4]);if(!certificate)throw std::runtime_error("certificate open failed");
    int cases;in>>cases;int first=std::stoi(argv[2]),last=std::stoi(argv[3]);
    if(first<1||last>cases||first>last)throw std::runtime_error("invalid interval");
    int pass=0,fail=0;
    for(int index=1;index<=cases;++index){
        int root,c,n;in>>root>>c>>n;std::vector<std::pair<int,int>>variables(n);
        for(auto &v:variables)in>>v.first>>v.second;
        if(!in)throw std::runtime_error("truncated input");
        if(index<first||index>last)continue;
        auto v=derive(rules,root,variables,index,certificate);int a=valuation(c,2),b=valuation(c,3);
        bool ok=v[0]<=a&&v[1]<=b;if(ok)++pass;else ++fail;
        std::cout<<"TARGET "<<index<<' '<<ok<<' '<<v[0]<<' '<<v[1]<<' '<<a<<' '<<b<<'\n';
        if(index%100==0)std::cout<<std::flush;
    }
    std::cout<<"PASS_1962_MONOMIAL_INTERVAL "<<first<<' '<<last<<' '<<pass<<' '<<fail<<std::endl;
}
