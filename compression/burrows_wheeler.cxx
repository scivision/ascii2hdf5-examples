// https://rosettacode.org/wiki/Burrows%E2%80%93Wheeler_transform

#include <algorithm>
#include <iostream>
#include <vector>
#include "burrows_wheeler.hpp"


void rotate(std::string &a) {
    char t = a[a.length() - 1];
    for (int i = a.length() - 1; i > 0; i--) {
        a[i] = a[i - 1];
    }
    a[0] = t;
}

std::string bwt(const std::string &s) {
    for (char c : s) {
        if (c == STX || c == ETX) {
            throw std::runtime_error("Input can't contain STX or ETX");
        }
    }

    std::string ss;
    ss += STX;
    ss += s;
    ss += ETX;

    std::vector<std::string> table;
    for (size_t i = 0; i < ss.length(); i++) {
        table.push_back(ss);
        rotate(ss);
    }
    //table.sort();
    std::sort(table.begin(), table.end());

    std::string out;
    for (auto &s : table) {
        out += s[s.length() - 1];
    }
    return out;
}

std::string ibwt(const std::string &r) {
    int len = r.length();
    std::vector<std::string> table(len);
    for (int i = 0; i < len; i++) {
        for (int j = 0; j < len; j++) {
            table[j] = r[j] + table[j];
        }
        std::sort(table.begin(), table.end());
    }
    for (auto &row : table) {
        if (row[row.length() - 1] == ETX) {
            return row.substr(1, row.length() - 2);
        }
    }
    return {};
}
