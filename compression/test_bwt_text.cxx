#include <algorithm>
#include <iostream>
#include "burrows_wheeler.hpp"


std::string makePrintable(const std::string &s) {
    auto ls = s;
    for (auto &c : ls) {
        if (c == STX) {
            c = '^';
        } else if (c == ETX) {
            c = '|';
        }
    }
    return ls;
}


int main() {
    auto tests = {
        "banana",
        "appellee",
        "dogwood",
        "TO BE OR NOT TO BE OR WANT TO BE OR NOT?",
        "SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES",
        "\u0002ABC\u0003"
    };

    for (auto &test : tests) {
        std::cout << makePrintable(test) << "\n";
        std::cout << " --> ";

        std::string t;
        try {
            t = bwt(test);
            std::cout << makePrintable(t) << "\n";
        } catch (std::runtime_error &e) {
            std::cout << "Error " << e.what() << "\n";
        }

        std::string r = ibwt(t);
        std::cout << " --> " << r << "\n\n";
    }

    return 0;
}
