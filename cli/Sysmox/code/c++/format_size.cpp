#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double bytes_val;
    if (!(cin >> bytes_val)) return 0;  // read from stdin

    double gb = 1024.0 * 1024 * 1024;
    double mb = 1024.0 * 1024;

    cout << fixed << setprecision(2);
    if (bytes_val >= gb)
        cout << bytes_val / gb << " GB";
    else
        cout << bytes_val / mb << " MB";

    return 0;
}
