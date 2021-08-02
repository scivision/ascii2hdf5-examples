#include "stdlib.h"
#include "stdio.h"
#include "string.h"
#include "burrows_wheeler.h"

void makePrintable(const char *s, char t[]) {
    strcpy(t, s);
    for ( ; *t != '\0'; ++t) {
        if (*t == STX) *t = '^';
        else if (*t == ETX) *t = '|';
    }
}

int main() {
    int i, res, len;
    char *tests[6], *t, *r, *s;
    tests[0] = "banana";
    tests[1] = "appellee";
    tests[2] = "dogwood";
    tests[3] = "TO BE OR NOT TO BE OR WANT TO BE OR NOT?";
    tests[4] = "SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES",
    tests[5] = "\002ABC\003";
    for (i = 0; i < 6; ++i) {
        len = strlen(tests[i]);
        t = calloc(len + 1, sizeof(char));
        makePrintable(tests[i], t);
        printf("%s\n", t);
        printf(" --> ");
        r = calloc(len + 3, sizeof(char));
        res = bwt(tests[i], r);
        if (res == 1) {
            printf("ERROR: String can't contain STX or ETX\n");
        }
        else {
            makePrintable(r, t);
            printf("%s\n", t);
        }
        s = calloc(len + 1, sizeof(char));
        ibwt(r, s);
        makePrintable(s, t);
        printf(" --> %s\n\n", t);
        free(t);
        free(r);
        free(s);
    }
    return 0;
}
