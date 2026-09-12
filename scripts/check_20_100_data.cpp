// Check the complete certificate as literal data, without executing GAP code.
// Build: g++ -O2 -std=c++17 scripts/check_20_100_data.cpp -lz -lcrypto -o /tmp/check_20_100_data
#include <openssl/evp.h>
#include <zlib.h>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>

static void require(bool b) {
    if (!b) throw std::runtime_error("invalid certificate data");
}

struct Parser {
    std::string_view s;
    size_t pos = 0;
    bool take(char c) {
        if (pos < s.size() && s[pos] == c) { ++pos; return true; }
        return false;
    }
    void exact(std::string_view text) {
        require(s.substr(pos, text.size()) == text);
        pos += text.size();
    }
    uint64_t natural() {
        size_t begin = pos;
        uint64_t value = 0;
        while (pos < s.size() && s[pos] >= '0' && s[pos] <= '9') {
            unsigned digit = s[pos++] - '0';
            require(value <= (std::numeric_limits<uint64_t>::max()-digit)/10);
            value = 10*value + digit;
        }
        require(pos > begin && (pos == begin+1 || s[begin] != '0'));
        return value;
    }
    void value(unsigned depth) {
        require(depth < 64);
        if (pos < s.size() && s[pos] == '[') { list(depth+1); return; }
        take('-');
        natural();
        if (take('/')) require(natural() > 0);
    }
    uint64_t list(unsigned depth = 0) {
        require(depth < 64 && take('['));
        uint64_t count = 0;
        if (take(']')) return count;
        do { value(depth+1); ++count; } while (take(','));
        require(take(']'));
        return count;
    }
    void end() { require(pos == s.size()); }
};

int main(int argc, char **argv) {
    try {
        require(argc == 3);
        unsigned n = std::stoul(argv[1]);
        require(n >= 2 && n <= 100);
        gzFile input = gzopen(argv[2], "rb");
        require(input != nullptr);
        gzbuffer(input, 1<<20);
        EVP_MD_CTX *digest = EVP_MD_CTX_new();
        require(digest && EVP_DigestInit_ex(digest, EVP_sha256(), nullptr) == 1);
        uint64_t nodes = 0, leaves = 0, edges = 0, bytes = 0, lines = 0;
        bool finished = false;
        std::string pending;
        char buffer[1<<20];
        auto line = [&](std::string_view text) {
            ++lines;
            require(!finished);
            Parser p{text};
            if (lines == 1) {
                p.exact("StartProof("); require(p.natural() == n);
                p.exact(","); require(p.natural() == n+1); p.exact(");");
            } else if (text.substr(0, 12) == "FinishProof(") {
                p.exact("FinishProof("); require(p.natural() == nodes && nodes > 0);
                p.exact(");"); finished = true;
            } else {
                p.exact("CheckNode("); require(p.natural() == nodes+1);
                p.exact(","); p.list(); p.exact(",");
                uint64_t permutation = p.list(); p.exact(",");
                uint64_t children = p.list(); p.exact(");");
                require(permutation == 0 || permutation == n);
                require(children == (permutation == 0 ? 0 : uint64_t(n)*(n-1)/2));
                ++nodes; leaves += (permutation == 0); edges += children;
            }
            p.end();
        };
        int length;
        while ((length = gzread(input, buffer, sizeof(buffer))) > 0) {
            require(EVP_DigestUpdate(digest, buffer, length) == 1);
            bytes += length;
            pending.append(buffer, length);
            size_t start = 0, stop;
            while ((stop = pending.find('\n', start)) != std::string::npos) {
                line(std::string_view(pending).substr(start, stop-start));
                start = stop+1;
            }
            pending.erase(0, start);
            require(pending.size() < (1u<<24));
        }
        require(length == 0 && gzeof(input) && gzclose(input) == Z_OK);
        require(pending.empty() && finished && lines == nodes+2);
        unsigned char result[EVP_MAX_MD_SIZE]; unsigned result_length;
        require(EVP_DigestFinal_ex(digest, result, &result_length) == 1);
        EVP_MD_CTX_free(digest);
        std::ostringstream hex;
        for (unsigned i = 0; i < result_length; ++i)
            hex << std::hex << std::setw(2) << std::setfill('0') << unsigned(result[i]);
        std::cout << "{\"status\":\"PASS_DATA_ONLY\",\"n\":" << n
                  << ",\"nodes\":" << nodes << ",\"leaves\":" << leaves
                  << ",\"edges\":" << edges << ",\"uncompressed_bytes\":" << bytes
                  << ",\"uncompressed_sha256\":\"" << hex.str() << "\"}\n";
        return 0;
    } catch (const std::exception &e) {
        std::cerr << e.what() << '\n'; return 1;
    }
}
