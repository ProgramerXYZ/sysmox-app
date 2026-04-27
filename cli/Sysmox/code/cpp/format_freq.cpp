#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double value; // value in MHz
    cin >> value;

    if (value >= 1000.0) {
        cout << fixed << setprecision(2)
             << (value / 1000.0) << "GHz";
    } else {
        cout << fixed << setprecision(0)
             << value << "MHz";
    }

    return 0;
}
