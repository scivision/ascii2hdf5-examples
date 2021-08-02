// https://rosettacode.org/wiki/Burrows%E2%80%93Wheeler_transform#C

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "burrows_wheeler.h"


int compareStrings(const void *a, const void *b) {
    char *aa = *(char **)a;
    char *bb = *(char **)b;
    return strcmp(aa, bb);
}

int bwt(const char *s, char r[]) {
    int i, len = strlen(s) + 2;
    char *ss, *str;
    char **table;
    if (strchr(s, STX) || strchr(s, ETX)) return 1;
    ss = calloc(len + 1, sizeof(char));
    sprintf(ss, "%c%s%c", STX, s, ETX);
    table = malloc(len * sizeof(const char *));
    for (i = 0; i < len; ++i) {
        str = calloc(len + 1, sizeof(char));
        strcpy(str, ss + i);
        if (i > 0) strncat(str, ss, i);
        table[i] = str;
    }
    qsort(table, len, sizeof(const char *), compareStrings);
    for(i = 0; i < len; ++i) {
        r[i] = table[i][len - 1];
        free(table[i]);
    }
    free(table);
    free(ss);
    return 0;
}

void ibwt(const char *r, char s[]) {
    int i, j, len = strlen(r);
    char **table = malloc(len * sizeof(const char *));
    for (i = 0; i < len; ++i) table[i] = calloc(len + 1, sizeof(char));
    for (i = 0; i < len; ++i) {
        for (j = 0; j < len; ++j) {
            memmove(table[j] + 1, table[j], len);
            table[j][0] = r[j];
        }
        qsort(table, len, sizeof(const char *), compareStrings);
    }
    for (i = 0; i < len; ++i) {
        if (table[i][len - 1] == ETX) {
            strncpy(s, table[i] + 1, len - 2);
            break;
        }
    }
    for (i = 0; i < len; ++i) free(table[i]);
    free(table);
}
