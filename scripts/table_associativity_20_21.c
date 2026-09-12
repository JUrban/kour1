#include <stdint.h>
#include <stddef.h>

/* Zero means associative; otherwise return one plus the first bad triple.
 * UINT64_MAX denotes invalid size or an out-of-range table entry. */
uint64_t table_associativity_2021(const uint8_t *table, uint32_t n) {
    if (n == 0 || n > 256) return UINT64_MAX;
    for (uint32_t i = 0; i < n*n; ++i)
        if (table[i] >= n) return UINT64_MAX;
    for (uint32_t a = 0; a < n; ++a) {
        const uint8_t *row_a = table + a*n;
        for (uint32_t b = 0; b < n; ++b) {
            const uint8_t *row_ab = table + row_a[b]*n;
            const uint8_t *row_b = table + b*n;
            for (uint32_t c = 0; c < n; ++c)
                if (row_ab[c] != row_a[row_b[c]])
                    return 1 + ((uint64_t)a*n + b)*n + c;
        }
    }
    return 0;
}
