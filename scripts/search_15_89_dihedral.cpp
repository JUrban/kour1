// Exact bounded search for a constant nonzero determinant in a dihedral
// Cayley adjacency matrix [[p(z),q(z)],[q(z^-1),p(z)]].
// p has coefficients 0/1 at signed exponents +-1,...,+-R, includes +-R,
// and has zero constant term. q has coefficients 0/1 on 0,...,2R with
// both endpoints present. Exact vector keys avoid hash-collision claims.
#include <algorithm>
#include <bit>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct Candidate { uint64_t p; int k; }; // lambda=-k/2

int main(int argc, char** argv) {
    int maxr = argc > 1 ? std::stoi(argv[1]) : 10;
    if (maxr < 1 || maxr > 15) return 2;
    uint64_t totalq=0, totalmatches=0, totalhits=0;
    for (int r=1;r<=maxr;++r) {
        auto start=std::chrono::steady_clock::now();
        std::map<std::string,std::vector<Candidate>> targets;
        for (uint64_t lo=0;lo<(uint64_t(1)<<(r-1));++lo) {
            uint64_t p=(uint64_t(1)<<(2*r))|1;
            for (int j=1;j<r;++j) if (lo&(uint64_t(1)<<(j-1))) {
                p|=(uint64_t(1)<<(r+j))|(uint64_t(1)<<(r-j));
            }
            for (int k=-2*r;k<=2*r+1;++k) {
                std::string key; bool valid=true;
                for (int h=1;h<=2*r;++h) {
                    int c=std::popcount(p&(p>>h));
                    if (h<=r && (p&(uint64_t(1)<<(r+h)))) c+=k;
                    if (c<0 || c>2*r+1-h) {valid=false;break;}
                    key.push_back(char(c));
                }
                if (valid) targets[key].push_back({p,k});
            }
        }
        uint64_t qcount=0,matches=0,hits=0;
        const uint64_t bound=uint64_t(1)<<(2*r-1);
        for (uint64_t mid=0;mid<bound;++mid) {
            uint64_t q=(mid<<1)|1|(uint64_t(1)<<(2*r));
            std::string key;
            for (int h=1;h<=2*r;++h)
                key.push_back(char(std::popcount(q&(q>>h))));
            ++qcount;
            auto found=targets.find(key);
            if (found==targets.end()) continue;
            for (auto c:found->second) {
                ++matches;
                int det4=4*(std::popcount(c.p)-std::popcount(q))+c.k*c.k;
                if (det4) {
                    ++hits;
                    std::cout<<"HIT R="<<r<<" p_mask="<<c.p<<" q_mask="<<q
                             <<" lambda_numerator="<<-c.k<<" denominator=2"
                             <<" determinant_numerator="<<det4<<" denominator=4\n";
                }
            }
        }
        totalq+=qcount;totalmatches+=matches;totalhits+=hits;
        auto ms=std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now()-start).count();
        std::cout<<"R="<<r<<" q_count="<<qcount<<" constant_determinants="<<matches
                 <<" nonzero_determinants="<<hits<<" elapsed_ms="<<ms<<std::endl;
    }
    std::cout<<"DONE total_q="<<totalq<<" constant_determinants="<<totalmatches
             <<" nonzero_determinants="<<totalhits<<std::endl;
}
