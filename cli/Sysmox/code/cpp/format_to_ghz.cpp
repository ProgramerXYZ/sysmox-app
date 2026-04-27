#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string input;
    getline(cin, input);

    // Remove spaces
    input.erase(remove_if(input.begin(), input.end(), ::isspace), input.end());

    if(input.empty()) {
        cerr << "Invalid input!\n";
        return 1;
    }

    double value = 0;
    try {
        value = stod(input);
    } catch(...) {
        cerr << "Invalid input!\n";
        return 1;
    }

    // If less than 1000 MHz → stay MHz
    // If ≥ 1000 MHz → convert to GHz
    if(value >= 1000.0) {
        value = value / 1000.0;
        cout << value << "GHz";
    } else {
        cout << value << "MHz";
    }

    return 0;
}
