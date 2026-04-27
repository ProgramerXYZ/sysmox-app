#include <iostream>
#include <sstream>
#include <vector>
#include <iomanip>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string input;
    getline(cin, input);

    stringstream ss(input);
    vector<double> values;
    double temp;

    while (ss >> temp) {
        values.push_back(temp);
    }

    for (size_t i = 0; i < values.size(); i++) {
        cout << "core " << i << ": "
             << fixed << setprecision(2)
             << values[i] << "GHz\n";
    }

    return 0;
}


