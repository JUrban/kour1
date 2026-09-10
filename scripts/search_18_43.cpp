// Exact modular fingerprints of binary necklaces for Kourovka 18.43.
// Build: g++ -O3 -std=c++17 scripts/search_18_43.cpp -o bin/search_18_43
// Run: bin/search_18_43 LENGTH [DIMENSION=3]
// A collision is only a candidate identity. All emitted words are canonical
// cyclic representatives; inverses are outside this positive-word search.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

constexpr uint64_t P = 2147483647ULL;
inline uint64_t modp(uint64_t x) {
    x = (x & P) + (x >> 31);
    x = (x & P) + (x >> 31);
    return x >= P ? x - P : x;
}

template<int D> struct Matrix {
    std::array<uint64_t,D*D> v{};
    static Matrix identity() {
        Matrix m; for(int i=0;i<D;i++) m.v[i*D+i]=1; return m;
    }
    Matrix times(const Matrix& other) const {
        Matrix r;
        for(int i=0;i<D;i++) for(int j=0;j<D;j++) {
            uint64_t sum=0;
            for(int k=0;k<D;k++) sum+=v[i*D+k]*other.v[k*D+j];
            r.v[i*D+j]=modp(sum);
        }
        return r;
    }
    Matrix times_diagonal(const std::array<uint64_t,D>& d) const {
        Matrix r;
        for(int i=0;i<D;i++) for(int j=0;j<D;j++)
            r.v[i*D+j]=modp(v[i*D+j]*d[j]);
        return r;
    }
    uint64_t trace() const {
        uint64_t sum=0; for(int i=0;i<D;i++) sum+=v[i*D+i]; return modp(sum);
    }
};

struct Fingerprint { uint64_t key, word; };
uint64_t phi(uint64_t n) {
    uint64_t out=n;
    for(uint64_t p=2;p*p<=n;p++) if(n%p==0) {
        out=out/p*(p-1); while(n%p==0)n/=p;
    }
    if(n>1)out=out/n*(n-1);
    return out;
}
uint64_t necklace_count(int n) {
    uint64_t sum=0;
    for(int d=1;d<=n;d++)if(n%d==0)sum+=phi(d)*(1ULL<<(n/d));
    return sum/n;
}
std::string word_string(uint64_t bits,int n) {
    std::string s;
    for(int i=n-1;i>=0;i--)s.push_back((bits>>i)&1 ? 'b':'a');
    return s;
}

template<int D> class Search {
    int length;
    std::array<int,64> letters{};
    std::array<std::array<Matrix<D>,64>,2> prefixes;
    std::array<std::array<uint64_t,D>,2> diagonals;
    std::array<Matrix<D>,2> bs;
    std::vector<Fingerprint> records;
    bool dump;
    std::chrono::steady_clock::time_point started;

    void set_letter(int t,int value) {
        letters[t]=value;
        for(int test=0;test<2;test++)
            prefixes[test][t] = value ? prefixes[test][t-1].times(bs[test])
              : prefixes[test][t-1].times_diagonal(diagonals[test]);
    }
    void necklaces(int t,int period,uint64_t code) {
        if(t>length) {
            if(length%period==0) {
                uint64_t key=(prefixes[0][length].trace()<<31)
                             | prefixes[1][length].trace();
                records.push_back({key,code});
            }
            return;
        }
        int copied=letters[t-period];
        set_letter(t,copied);
        necklaces(t+1,period,(code<<1)|copied);
        if(copied==0) {
            set_letter(t,1);
            necklaces(t+1,t,(code<<1)|1);
        }
    }
public:
    explicit Search(int n,bool dump_values=false):length(n),dump(dump_values) {
        std::array<std::array<uint64_t,3>,2> all_diag={{{3,5,7},{11,13,17}}};
        std::array<std::array<uint64_t,9>,2> all_b={{{2,3,5,7,11,13,17,19,23},
                                                   {29,31,37,41,43,47,53,59,61}}};
        for(int test=0;test<2;test++) {
            prefixes[test][0]=Matrix<D>::identity();
            for(int i=0;i<D;i++) {
                diagonals[test][i]=all_diag[test][i];
                for(int j=0;j<D;j++)bs[test].v[i*D+j]=all_b[test][3*i+j];
            }
        }
        records.reserve(necklace_count(length));
    }
    void run() {
        started=std::chrono::steady_clock::now();
        std::cout<<"START length="<<length<<" dimension="<<D<<" modulus="<<P
                 <<" expected_necklaces="<<necklace_count(length)<<std::endl;
        necklaces(1,1,0);
        if(records.size()!=necklace_count(length))throw std::runtime_error("necklace count mismatch");
        std::cout<<"ENUMERATED count="<<records.size()<<std::endl;
        if(dump)for(auto record:records)
            std::cout<<"FINGERPRINT "<<word_string(record.word,length)<<" "<<record.key<<"\n";
        std::sort(records.begin(),records.end(),[](auto x,auto y){
            return x.key<y.key || (x.key==y.key && x.word<y.word);
        });
        uint64_t collisions=0;
        for(size_t i=1;i<records.size();i++) if(records[i].key==records[i-1].key) {
            // Print entire adjacent chain in each hash bucket, sufficient to
            // reconstruct the bucket for independent exact verification.
            std::cout<<"CANDIDATE "<<word_string(records[i-1].word,length)<<" "
                     <<word_string(records[i].word,length)<<" key="<<records[i].key<<"\n";
            collisions++;
        }
        auto ms=std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now()-started).count();
        std::cout<<"DONE length="<<length<<" dimension="<<D<<" count="<<records.size()
                 <<" candidate_adjacent_pairs="<<collisions<<" elapsed_ms="<<ms<<std::endl;
    }
};
int main(int argc,char**argv) {
    if(argc<2 || argc>4){std::cerr<<"Usage: search_18_43 LENGTH [2|3] [dump]\n";return 2;}
    int n=std::stoi(argv[1]),dimension=argc>=3?std::stoi(argv[2]):3;
    bool dump=argc==4 && std::string(argv[3])=="dump";
    if(n<1 || n>36 || (dimension!=2 && dimension!=3))return 2;
    if(dump && n>12)return 2;
    if(dimension==2)Search<2>(n,dump).run();else Search<3>(n,dump).run();
}
