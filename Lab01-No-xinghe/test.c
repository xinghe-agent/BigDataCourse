#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

int main(void)
{
    int16_t si = -1;

    uint16_t a = (uint16_t)si;
    uint32_t b = (uint32_t)si;

    printf("si = %" PRId16 "\n", si);
    printf("转换为 uint16_t：%" PRIu16 "\n", a);
    printf("转换为 uint32_t：%" PRIu32 "\n", b);

    return 0;
}