#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

std::vector<double> calc_momentum(const std::vector<double>& prices, int n) {
    std::vector<double> ret;
    for (int i = n; i < prices.size(); i++) {
        ret.push_back(prices[i] / prices[i-n] - 1.0);
    }
    return ret;
}

PYBIND11_MODULE(factor_core, m) {
    m.def("calc_momentum", &calc_momentum, "Calculate N-day return");
}