// Exact GF(2) search, quotienting the input set by column permutations.
#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <stdexcept>

using Matrix=std::array<unsigned,6>;
using Clock=std::chrono::steady_clock;

unsigned apply(const Matrix& a,unsigned v) {
    unsigned result=0;
    while(v) { unsigned i=std::countr_zero(v); result^=a[i]; v&=v-1; }
    return result;
}

Matrix multiply(const Matrix& a,const Matrix& b,unsigned n) {
    Matrix result{};
    for(unsigned i=0;i<n;++i) result[i]=apply(a,b[i]);
    return result;
}

std::uint64_t flatten(const Matrix& a,unsigned n) {
    std::uint64_t result=0;
    for(unsigned i=0;i<n;++i) result|=std::uint64_t(a[i])<<(n*i);
    return result;
}

bool cyclic(const Matrix& a,unsigned n) {
    // The first dependence among powers occurs at the minimal polynomial.
    std::array<std::uint64_t,36> pivots{};
    Matrix power{};
    for(unsigned i=0;i<n;++i) power[i]=1u<<i;
    for(unsigned k=0;k<n;++k) {
        auto value=flatten(power,n);
        while(value) {
            unsigned i=std::bit_width(value)-1;
            if(pivots[i]) value^=pivots[i];
            else { pivots[i]=value; break; }
        }
        if(!value) return false;
        if(k+1<n) power=multiply(a,power,n);
    }
    return true;
}

struct Search {
    unsigned n;
    std::uint64_t bases=0,tests=0,hits=0,maxTests=0;
    Matrix chosen{};
    Clock::time_point start=Clock::now();

    void inspect() {
        ++bases;
        Matrix a{};
        std::array<unsigned,6> p{};
        std::iota(p.begin(),p.end(),0);
        bool found=false;
        std::uint64_t count=0;
        do {
            for(unsigned i=0;i<n;++i) a[i]=chosen[p[i]];
            ++tests; ++count;
            if(cyclic(a,n)) { found=true; break; }
        } while(std::next_permutation(p.begin(),p.begin()+n));
        maxTests=std::max(maxTests,count);
        if(!found) {
            ++hits;
            std::cout<<"HIT n="<<n<<" columns=";
            for(unsigned i=0;i<n;++i) std::cout<<chosen[i]<<",";
            std::cout<<" permutations="<<count<<std::endl;
        }
        if(bases%1000000==0) {
            auto ms=std::chrono::duration_cast<std::chrono::milliseconds>(Clock::now()-start).count();
            std::cout<<"PROGRESS n="<<n<<" bases="<<bases<<" tests="<<tests
                     <<" hits="<<hits<<" elapsed_ms="<<ms<<std::endl;
        }
    }

    void extend(unsigned depth,unsigned next,Matrix pivots) {
        if(depth==n) { inspect(); return; }
        const unsigned end=(1u<<n)-(n-depth)+1;
        for(unsigned v=next;v<end;++v) {
            auto reduced=v;
            while(reduced) {
                unsigned i=std::bit_width(reduced)-1;
                if(pivots[i]) reduced^=pivots[i];
                else break;
            }
            if(!reduced) continue;
            Matrix newPivots=pivots;
            newPivots[std::bit_width(reduced)-1]=reduced;
            chosen[depth]=v;
            extend(depth+1,v+1,newPivots);
        }
    }
};

int main(int argc,char** argv) {
    unsigned limit=argc>1?std::stoul(argv[1]):6;
    if(limit<1||limit>6) throw std::runtime_error("dimension outside 1..6");
    std::uint64_t total=0,totalTests=0,totalHits=0;
    for(unsigned n=1;n<=limit;++n) {
        Search search{n};
        search.extend(0,1,Matrix{});
        std::uint64_t expected=1,factorial=1;
        for(unsigned i=0;i<n;++i) { expected*=((1ull<<n)-(1ull<<i)); factorial*=i+1; }
        expected/=factorial;
        if(search.bases!=expected) throw std::runtime_error("unordered basis coverage");
        auto ms=std::chrono::duration_cast<std::chrono::milliseconds>(Clock::now()-search.start).count();
        std::cout<<"DIMENSION_DONE n="<<n<<" bases="<<search.bases
                 <<" expected="<<expected<<" tests="<<search.tests
                 <<" max_tests="<<search.maxTests<<" hits="<<search.hits
                 <<" elapsed_ms="<<ms<<" PASS"<<std::endl;
        total+=search.bases; totalTests+=search.tests; totalHits+=search.hits;
    }
    std::cout<<"DONE bases="<<total<<" tests="<<totalTests<<" hits="<<totalHits<<" PASS"<<std::endl;
    return 0;
}
