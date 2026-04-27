#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <iomanip>
#include <cctype>
#include <algorithm>
using namespace std;

string formatTime(double seconds) {
    int hrs = seconds / 3600;
    int mins = ((int)seconds % 3600) / 60;
    int secs = (int)seconds % 60;

    ostringstream out;
    if(hrs > 0) out << hrs << "h ";
    if(mins > 0) out << mins << "m ";
    out << secs << "s";
    return out.str();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string input;
    getline(cin, input);

    // Remove spaces
    input.erase(remove_if(input.begin(), input.end(), ::isspace), input.end());

    vector<double> values;

    // Check if it's a list (starts with '[')
    if(!input.empty() && input.front() == '[') {
        input.erase(remove(input.begin(), input.end(), '['), input.end());
        input.erase(remove(input.begin(), input.end(), ']'), input.end());

        stringstream ss(input);
        string num;

        while(getline(ss, num, ',')) {
            try {
                values.push_back(stod(num));
            } catch(...) {}
        }
    } else {
        try {
            values.push_back(stod(input));
        } catch(...) {}
    }

    if(values.empty()) {
        cerr << "Invalid input!\n";
        return 1;
    }

    ostringstream result;
    for(size_t i = 0; i < values.size(); ++i) {
        result << "CPU" << (i + 1) << ": " << formatTime(values[i]);
        if(i < values.size() - 1)
            result << " ";
    }

    cout << result.str() << endl;
    return 0;
}
