#include <stdint.h>

/* Exact 14-by-14 matrix multiplication over Z/3 or Z/9. */
uint32_t multiply_1961(const uint8_t *a, const uint8_t *b,
                       uint8_t *out, uint32_t modulus) {
    if (modulus != 3 && modulus != 9) return 1;
    for (uint32_t k=0;k<196;++k)
        if (a[k]>=modulus || b[k]>=modulus) return 2;
    for (uint32_t i=0;i<14;++i) {
        uint32_t row[14]={0};
        for (uint32_t k=0;k<14;++k) {
            uint32_t x=a[14*i+k];
            if (x)
                for (uint32_t j=0;j<14;++j) row[j]+=x*b[14*k+j];
        }
        for (uint32_t j=0;j<14;++j) out[14*i+j]=(uint8_t)(row[j]%modulus);
    }
    return 0;
}
