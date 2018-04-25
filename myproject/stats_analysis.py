from __future__ import division
import math

class Stats(object):
    def __init__(self, *args, **kwargs):
        self.data_copy = kwargs['tabledata']
        self.rows_list =  self.data_copy.keys()
        self.tps_backup = []
    def return_degradation_values(self):
        if not self._get_relative_tps_values():
            return False
        degradation_vals = self._calculate_relative_degradation()
        return degradation_vals

    def _get_relative_tps_values(self):
        rows_list = sorted([str(d) for d in self.rows_list])
        for row in rows_list:
            row_data = [str(d) for d in self.data_copy[row]]
            self.tps_backup.append(int(row_data[1]))
            row_data[1] = int(int(row_data[1]) * 100 / int(row_data[2]))
            self.data_copy[row][1] = row_data[1]
        return True

    def _calculate_relative_degradation(self):
        degradation_vals = []
        baseline = 0
        rows_list = sorted([str(d) for d in self.rows_list])
        for row in rows_list:
            row_data = [str(d) for d in self.data_copy[row]]
            if row_data[3] == 'baseline':
                baseline = int(row_data[1])
                degradation_vals.append(0)
                continue
            degradation = int((int(row_data[1])/int(baseline) * 100))
            degradation_vals.append(100 - degradation)
        return degradation_vals
