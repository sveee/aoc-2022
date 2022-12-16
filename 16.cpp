
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;



int NOT_CALCULATED = -1;
int dp[60][60][27][1 << 15];
vector<int> pressure{0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 20, 6, 0, 0, 0, 0, 4, 0, 5, 19, 0, 0, 0, 0, 0, 0, 0, 11, 13, 0, 0, 22, 7, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 21, 0, 0, 0, 8, 0, 9};
vector<vector<int> > graph{
    vector<int>{49, 13, 26, 21, 46},
    vector<int>{53, 2},
    vector<int>{51, 1},
    vector<int>{35, 57},
    vector<int>{23, 30},
    vector<int>{57, 36},
    vector<int>{45, 59},
    vector<int>{22, 59},
    vector<int>{40, 44},
    vector<int>{36, 46},
    vector<int>{56, 20},
    vector<int>{15, 13},
    vector<int>{35, 39},
    vector<int>{11, 0},
    vector<int>{54},
    vector<int>{28, 43, 25, 11, 55},
    vector<int>{17, 32},
    vector<int>{35, 16},
    vector<int>{21, 57},
    vector<int>{32, 33},
    vector<int>{55, 10, 47, 27, 37},
    vector<int>{18, 0},
    vector<int>{7, 34, 49, 47, 43},
    vector<int>{4, 33, 40},
    vector<int>{41, 44},
    vector<int>{57, 15},
    vector<int>{0, 37},
    vector<int>{36, 20},
    vector<int>{15, 36},
    vector<int>{54, 41},
    vector<int>{4, 41},
    vector<int>{52, 56},
    vector<int>{48, 19, 16},
    vector<int>{19, 23},
    vector<int>{22, 36},
    vector<int>{17, 3, 12, 50},
    vector<int>{34, 5, 9, 27, 28},
    vector<int>{26, 20},
    vector<int>{59, 57},
    vector<int>{59, 12},
    vector<int>{23, 8},
    vector<int>{29, 52, 30, 24},
    vector<int>{48, 59},
    vector<int>{15, 22},
    vector<int>{24, 8},
    vector<int>{6, 53},
    vector<int>{0, 9},
    vector<int>{22, 20},
    vector<int>{42, 32},
    vector<int>{22, 0},
    vector<int>{35, 58},
    vector<int>{58, 2},
    vector<int>{41, 31},
    vector<int>{45, 1},
    vector<int>{29, 14},
    vector<int>{15, 20},
    vector<int>{10, 31},
    vector<int>{18, 25, 5, 38, 3},
    vector<int>{51, 50},
    vector<int>{6, 42, 39, 7, 38}
};
unordered_map<int, int> valve_map{
    {8, 0},
    {14, 1},
    {15, 2},
    {20, 3},
    {22, 4},
    {23, 5},
    {31, 6},
    {32, 7},
    {35, 8},
    {36, 9},
    {41, 10},
    {51, 11},
    {53, 12},
    {57, 13},
    {59, 14}
};




int get_mask(int node) {
    return (1 << valve_map.at(node));
}


vector<int> get_neighbours(int node, int current_valves) {
    vector<int> r = graph[node];
    if ((pressure[node] > 0) && (get_mask(node) & current_valves) == 0) {
        r.push_back(node);
    }
    return r;
}



void initialize() {

    for (int node1 = 0; node1 < 60; ++node1) {
        for (int node2 = 0; node2 < 60; ++node2) {
            for (int remaining_time = 0; remaining_time < 27; ++remaining_time) {
                for (int current_valves = 0; current_valves < (1 << 15); ++current_valves) {
                    dp[node1][node2][remaining_time][current_valves] = NOT_CALCULATED;
                }
            }
        }
    }
}


int find_most_pressure(int node1, int node2, int remaining_time, int current_valves) {

    if (dp[node1][node2][remaining_time][current_valves] != NOT_CALCULATED) {
        return dp[node1][node2][remaining_time][current_valves];
    }

    if (remaining_time == 0) {
        return 0;
    }

    int result = 0, new_result;


    vector<int> neighbors1 = get_neighbours(node1, current_valves);
    vector<int> neighbors2 = get_neighbours(node2, current_valves);

    for (int next_node1: neighbors1) {
        for (int next_node2: neighbors2) {
            if ((next_node1 == node1) && (next_node2 == node2) && (node1 == node2)) {
                continue;
            }

            int add = 0;
            int remaining_pressure = 0;
            if (next_node1 == node1) {
                remaining_pressure += pressure[node1] * (remaining_time - 1);
                add |= get_mask(node1);
            }
            if (next_node2 == node2) {
                remaining_pressure += pressure[node2] * (remaining_time - 1);
                add |= get_mask(node2);
            }


            int new_result = find_most_pressure(
                next_node1, next_node2,
                remaining_time - 1,
                current_valves | add
            ) + remaining_pressure;
            if (new_result > result) {
                result = new_result;
            }
        }
    }
    dp[node1][node2][remaining_time][current_valves] = result;
    return result;
}


void solve() {
    cout << find_most_pressure(0, 0, 26, 0) << endl;
}


int main() {
    initialize();
    solve();
}
