#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double seconds;
    if (!(cin >> seconds)) return 0;

    double minute = 60.0;
    double hour = 3600.0;
    double day = 86400.0;

    cout << fixed << setprecision(2);

    if (seconds < minute)
        cout << seconds << " sec";
    else if (seconds < hour)
        cout << seconds / minute << " min";
    else if (seconds < day)
        cout << seconds / hour << " hr";
    else
        cout << seconds / day << " days";

    return 0;
}
