#include <bits/stdc++.h>
using namespace std;

class Solution{
public
    vector<int> selection_sort(vector<int>&v){
        for(int i=0;i<v.size();i++){
            int curr_min = v[i];
            for(int j=i+1; j<v.size();j++){
                curr_min = min(curr_min, v[j]);
            }
            v[i] = curr_min;
        }
        return v;
    }
};

sol = new Solution();
print(sol.selection_sort({3,8,1,5,2}));