import unittest

from game.quarry_rush.map.collectable.collectable_generator import CollectableGenerator

class TestCollectableGenerator(unittest.TestCase):
    def setUp(self):
        self.collectable_generator: CollectableGenerator = CollectableGenerator()
    
    def test_adjust(self) -> None:
        weights = [[.1, .4], [.6, .7]]
        result = self.collectable_generator.adjust(weights)
        result_flat = [x for row in result for x in row]
        self.assertEqual(max(result_flat), 1)
        self.assertEqual(min(result_flat), 0)
        
    def test_layer(self) -> None:
        weights_1 = [[0.2, 0.92, 0.05, 0.84, 0.33, 0.05, 0.15, 0.3, 0.59, 0.63, 0.12, 0.75, 0.16, 0.23, 0.99, 0.19, 0.19, 0.89, 0.31, 0.82, 0.8, 0.75], [0.92, 0.3, 0.13, 0.08, 0.79, 0.77, 0.34, 0.69, 0.31, 0.06, 0.79, 0.99, 0.44, 0.61, 0.35, 0.95, 0.75, 0.3, 0.45, 0.12, 0.51, 0.8], [0.32, 0.52, 0.48, 0.54, 0.37, 0.08, 1.0, 0.33, 0.69, 0.17, 0.29, 0.32, 0.91, 0.21, 0.52, 0.4, 0.48, 0.62, 0.86, 0.76, 0.49, 0.24], [0.59, 0.08, 0.91, 0.65, 0.36, 0.41, 0.67, 0.67, 0.55, 0.26, 0.92, 0.81, 0.75, 0.84, 0.93, 0.79, 0.11, 0.98, 0.32, 0.03, 0.43, 0.28], [0.98, 0.35, 0.97, 0.36, 0.64, 0.24, 0.73, 0.06, 0.07, 0.03, 0.48, 0.65, 0.51, 0.87, 0.83, 0.96, 0.58, 0.09, 0.39, 0.38, 0.01, 0.02], [0.5, 0.04, 0.74, 0.26, 0.21, 0.93, 0.58, 0.99, 0.43, 0.22, 0.01, 0.78, 0.29, 0.44, 0.69, 0.4, 0.75, 0.39, 0.25, 0.99, 0.74, 0.78], [0.94, 0.32, 0.09, 0.81, 0.14, 0.84, 0.52, 0.72, 0.72, 0.33, 0.57, 0.85, 0.68, 0.79, 0.28, 0.67, 0.28, 0.31, 0.69, 0.95, 0.48, 0.58], [0.66, 0.44, 0.7, 0.01, 0.22, 0.79, 0.19, 0.22, 0.81, 0.06, 0.45, 0.6, 0.87, 0.14, 0.6, 0.64, 0.16, 0.24, 0.41, 0.45, 0.75, 0.49], [0.87, 0.58, 0.73, 0.92, 0.12, 0.88, 0.64, 0.57, 0.99, 0.41, 0.18, 0.44, 0.53, 0.12, 0.68, 0.28, 0.71, 0.36, 0.94, 0.97, 0.72, 0.84], [0.05, 0.74, 0.13, 0.78, 0.51, 0.85, 0.82, 0.56, 0.89, 0.32, 0.76, 0.63, 0.12, 0.8, 0.17, 0.53, 0.8, 0.3, 0.54, 0.49, 0.61, 0.51], [0.78, 0.11, 0.12, 0.04, 0.69, 0.24, 0.11, 0.13, 0.63, 0.11, 0.36, 0.2, 0.18, 0.35, 0.87, 0.27, 0.36, 0.51, 0.61, 0.62, 0.61, 0.02], [0.25, 0.4, 0.51, 0.77, 0.13, 0.27, 0.73, 0.25, 0.03, 0.22, 0.02, 0.03, 0.04, 0.07, 0.79, 0.64, 0.32, 0.34, 0.87, 0.56, 0.88, 0.03], [0.13, 0.03, 0.34, 0.5, 0.32, 0.63, 0.35, 0.7, 0.6, 0.19, 0.31, 0.92, 0.82, 0.9, 0.22, 0.67, 0.2, 0.89, 0.21, 0.94, 0.47, 0.14], [0.88, 0.0, 0.47, 0.24, 0.6, 0.96, 0.84, 0.68, 0.77, 0.2, 0.88, 0.28, 0.11, 0.31, 0.6, 0.23, 0.72, 0.4, 0.88, 0.24, 0.28, 0.34], [0.67, 0.08, 0.45, 0.19, 0.74, 0.71, 0.23, 0.94, 0.43, 0.45, 0.23, 0.8, 0.37, 0.3, 0.53, 0.21, 0.8, 0.89, 0.09, 0.62, 0.3, 0.57], [0.1, 0.05, 0.84, 0.08, 0.18, 0.63, 0.46, 0.03, 0.41, 0.15, 0.52, 0.26, 0.68, 0.56, 0.6, 0.73, 0.04, 0.21, 0.16, 0.9, 0.93, 0.93], [0.72, 0.23, 0.29, 0.97, 0.11, 0.48, 0.39, 0.68, 0.42, 0.24, 0.44, 0.74, 0.18, 0.24, 0.54, 0.7, 0.52, 1.0, 0.55, 0.86, 0.58, 0.57], [0.51, 0.26, 0.65, 0.15, 0.94, 0.28, 0.68, 0.84, 0.84, 0.37, 0.08, 0.88, 0.42, 0.18, 0.93, 0.75, 0.47, 0.84, 0.67, 0.53, 0.67, 0.89], [0.33, 0.78, 0.05, 0.52, 0.88, 0.24, 0.54, 0.39, 0.43, 0.84, 0.06, 0.36, 0.55, 0.11, 0.89, 0.57, 0.47, 0.56, 0.26, 0.47, 0.32, 0.64], [0.57, 0.35, 0.78, 1.0, 0.51, 0.67, 0.19, 0.14, 0.1, 0.13, 0.5, 0.07, 0.5, 0.34, 0.08, 0.41, 0.78, 0.17, 0.74, 0.29, 0.14, 0.96], [0.14, 0.72, 0.0, 0.97, 0.75, 0.74, 0.36, 0.8, 0.41, 0.81, 0.78, 0.36, 0.03, 0.35, 0.13, 0.16, 0.72, 0.03, 0.62, 0.23, 0.82, 0.3], [0.04, 0.87, 0.4, 0.79, 0.82, 0.6, 0.14, 0.53, 0.0, 0.58, 0.46, 0.49, 0.61, 0.56, 0.13, 0.76, 0.96, 0.06, 0.05, 0.45, 0.11, 0.99]]
        weights_2 = [[0.47, 0.05, 0.28, 0.91, 0.7, 0.65, 0.56, 0.75, 0.38, 0.83, 1.0, 0.76, 0.68, 0.66, 0.43, 0.45, 0.51, 0.01, 0.5, 0.57, 0.21, 0.07], [0.79, 0.29, 0.82, 0.3, 0.47, 0.49, 0.68, 0.58, 0.35, 0.92, 0.51, 0.12, 0.01, 0.54, 0.42, 0.12, 0.59, 0.48, 0.27, 0.94, 0.11, 0.44], [0.08, 0.68, 0.76, 0.01, 0.83, 0.36, 0.46, 0.06, 0.68, 0.67, 0.59, 0.98, 0.03, 0.59, 0.67, 0.72, 0.3, 0.36, 0.53, 0.61, 0.4, 0.71], [0.54, 0.01, 0.58, 0.35, 0.21, 0.99, 0.89, 0.22, 0.74, 0.48, 0.93, 0.85, 0.56, 0.88, 0.0, 0.28, 0.58, 0.69, 0.04, 0.11, 0.8, 0.57], [0.37, 0.48, 0.73, 0.93, 0.54, 0.45, 0.67, 0.26, 0.85, 0.5, 0.27, 0.51, 0.91, 0.8, 0.7, 0.23, 0.62, 0.83, 0.72, 0.35, 0.16, 0.91], [0.63, 0.13, 0.01, 0.34, 0.6, 0.99, 0.94, 0.78, 0.74, 0.14, 0.63, 0.68, 0.92, 0.7, 0.87, 0.36, 0.44, 0.23, 0.76, 0.6, 0.35, 0.94], [0.13, 0.3, 0.31, 0.39, 0.65, 0.13, 0.84, 0.36, 0.35, 0.43, 0.22, 0.54, 0.02, 0.09, 0.49, 0.91, 0.3, 0.19, 0.01, 0.89, 0.01, 0.34], [0.39, 0.21, 0.27, 0.56, 0.58, 0.93, 0.36, 0.66, 0.85, 1.0, 0.95, 0.0, 0.5, 0.99, 0.79, 0.08, 0.26, 0.44, 0.16, 0.12, 0.43, 0.07], [0.49, 0.27, 0.23, 0.88, 0.74, 0.52, 0.43, 0.4, 0.09, 0.59, 0.36, 0.22, 0.75, 0.51, 0.06, 0.58, 0.3, 0.25, 0.85, 0.43, 0.83, 0.46], [0.24, 0.72, 0.56, 0.57, 0.91, 0.12, 0.98, 0.98, 0.85, 0.1, 0.99, 0.5, 0.73, 0.98, 0.29, 0.13, 0.65, 0.41, 0.99, 0.89, 0.83, 0.54], [0.69, 0.65, 0.49, 0.46, 0.2, 0.07, 0.96, 0.5, 0.98, 0.94, 1.0, 0.48, 0.71, 0.38, 0.25, 0.48, 0.53, 0.01, 0.92, 0.7, 0.6, 0.43], [0.78, 0.38, 0.2, 0.51, 0.65, 0.67, 0.41, 0.85, 0.04, 0.8, 0.82, 0.66, 0.44, 0.96, 0.72, 0.77, 0.57, 0.14, 0.47, 0.07, 0.71, 0.19], [0.65, 0.97, 0.22, 0.9, 0.37, 0.21, 0.22, 0.32, 0.02, 0.78, 0.65, 0.61, 0.79, 0.51, 0.87, 0.4, 0.89, 0.04, 0.61, 0.63, 0.18, 0.98], [0.71, 0.98, 0.96, 0.15, 0.96, 0.5, 0.76, 0.83, 0.49, 0.71, 0.88, 0.99, 0.61, 0.28, 1.0, 0.36, 0.72, 0.97, 0.28, 0.24, 0.58, 0.47], [0.45, 0.11, 0.15, 0.25, 0.15, 0.19, 0.29, 0.08, 0.32, 0.46, 0.35, 0.47, 0.6, 0.1, 0.18, 0.05, 0.45, 0.93, 0.34, 0.88, 0.18, 0.11], [0.12, 0.39, 0.76, 0.55, 0.29, 0.27, 0.67, 0.45, 0.18, 0.38, 0.71, 0.39, 0.78, 0.9, 0.53, 0.09, 0.83, 0.34, 0.37, 0.6, 0.57, 0.75], [0.94, 0.75, 0.9, 0.27, 0.28, 0.8, 0.61, 0.18, 0.81, 0.07, 0.48, 0.54, 0.87, 0.22, 0.96, 0.8, 0.01, 0.52, 0.1, 0.35, 0.56, 0.39], [0.51, 0.24, 0.5, 0.07, 0.29, 0.95, 0.78, 0.22, 0.1, 0.8, 0.85, 0.69, 0.85, 0.72, 0.6, 0.23, 0.49, 0.73, 0.58, 0.63, 0.37, 0.58], [0.72, 0.39, 0.55, 0.06, 0.52, 0.6, 0.51, 0.15, 0.08, 0.83, 0.66, 0.26, 0.77, 0.55, 0.39, 0.31, 0.08, 0.85, 0.61, 0.49, 0.05, 0.29], [0.28, 0.89, 0.77, 0.06, 0.61, 0.58, 0.9, 0.42, 0.66, 0.9, 0.39, 0.31, 0.78, 0.45, 0.81, 0.86, 0.42, 0.79, 0.72, 0.82, 0.71, 0.78], [0.34, 0.19, 0.31, 0.58, 0.48, 0.94, 0.59, 0.65, 0.75, 0.7, 0.81, 0.05, 0.36, 0.27, 0.17, 0.4, 0.27, 0.11, 0.81, 0.54, 0.93, 0.22], [0.31, 0.67, 0.67, 0.82, 0.06, 0.21, 0.63, 0.95, 0.21, 0.3, 0.92, 0.75, 0.63, 0.57, 0.18, 0.59, 0.84, 0.47, 0.98, 0.33, 0.93, 0.84]]
        expected_result = [[0.094, 0.046000000000000006, 0.014000000000000002, 0.7644, 0.23099999999999998, 0.0325, 0.084, 0.22499999999999998, 0.22419999999999998, 0.5229, 0.12, 0.5700000000000001, 0.10880000000000001, 0.15180000000000002, 0.42569999999999997, 0.0855, 0.0969, 0.0089, 0.155, 0.4673999999999999, 0.168, 0.052500000000000005], [0.7268000000000001, 0.087, 0.1066, 0.024, 0.3713, 0.3773, 0.23120000000000004, 0.40019999999999994, 0.1085, 0.0552, 0.40290000000000004, 0.11879999999999999, 0.0044, 0.3294, 0.147, 0.11399999999999999, 0.4425, 0.144, 0.12150000000000001, 0.11279999999999998, 0.056100000000000004, 0.35200000000000004], [0.0256, 0.3536, 0.3648, 0.0054, 0.3071, 0.0288, 0.46, 0.0198, 0.4692, 0.11390000000000002, 0.17109999999999997, 0.3136, 0.0273, 0.12389999999999998, 0.34840000000000004, 0.288, 0.144, 0.22319999999999998, 0.45580000000000004, 0.4636, 0.196, 0.1704], [0.3186, 0.0008, 0.5277999999999999, 0.22749999999999998, 0.0756, 0.4059, 0.5963, 0.1474, 0.40700000000000003, 0.1248, 0.8556, 0.6885, 0.42000000000000004, 0.7392, 0.0, 0.22120000000000004, 0.0638, 0.6761999999999999, 0.0128, 0.0033, 0.34400000000000003, 0.1596], [0.3626, 0.16799999999999998, 0.7081, 0.3348, 0.3456, 0.108, 0.48910000000000003, 0.0156, 0.059500000000000004, 0.015, 0.1296, 0.3315, 0.4641, 0.6960000000000001, 0.581, 0.2208, 0.3596, 0.07469999999999999, 0.2808, 0.13299999999999998, 0.0016, 0.0182], [0.315, 0.005200000000000001, 0.0074, 0.0884, 0.126, 0.9207000000000001, 0.5451999999999999, 0.7722, 0.3182, 0.030800000000000004, 0.0063, 0.5304000000000001, 0.2668, 0.308, 0.6003, 0.144, 0.33, 0.0897, 0.19, 0.594, 0.259, 0.7332], [0.1222, 0.096, 0.027899999999999998, 0.3159, 0.09100000000000001, 0.1092, 0.4368, 0.2592, 0.252, 0.1419, 0.12539999999999998, 0.459, 0.013600000000000001, 0.0711, 0.13720000000000002, 0.6097, 0.084, 0.0589, 0.0069, 0.8454999999999999, 0.0048, 0.19720000000000001], [0.2574, 0.0924, 0.189, 0.005600000000000001, 0.1276, 0.7347, 0.0684, 0.1452, 0.6885, 0.06, 0.4275, 0.0, 0.435, 0.1386, 0.474, 0.0512, 0.041600000000000005, 0.1056, 0.06559999999999999, 0.054, 0.3225, 0.034300000000000004], [0.4263, 0.1566, 0.1679, 0.8096, 0.08879999999999999, 0.4576, 0.2752, 0.22799999999999998, 0.0891, 0.24189999999999998, 0.0648, 0.0968, 0.3975, 0.0612, 0.0408, 0.16240000000000002, 0.213, 0.09, 0.7989999999999999, 0.41709999999999997, 0.5975999999999999, 0.3864], [0.012, 0.5327999999999999, 0.0728, 0.4446, 0.4641, 0.102, 0.8036, 0.5488000000000001, 0.7565, 0.032, 0.7524, 0.315, 0.0876, 0.784, 0.049300000000000004, 0.0689, 0.52, 0.12299999999999998, 0.5346000000000001, 0.4361, 0.5063, 0.27540000000000003], [0.5382, 0.07150000000000001, 0.0588, 0.0184, 0.13799999999999998, 0.016800000000000002, 0.1056, 0.065, 0.6174, 0.10339999999999999, 0.36, 0.096, 0.1278, 0.13299999999999998, 0.2175, 0.1296, 0.1908, 0.0051, 0.5612, 0.434, 0.366, 0.0086], [0.195, 0.15200000000000002, 0.10200000000000001, 0.3927, 0.0845, 0.18090000000000003, 0.29929999999999995, 0.2125, 0.0012, 0.17600000000000002, 0.016399999999999998, 0.0198, 0.0176, 0.06720000000000001, 0.5688, 0.4928, 0.18239999999999998, 0.04760000000000001, 0.4089, 0.039200000000000006, 0.6248, 0.0057], [0.0845, 0.029099999999999997, 0.0748, 0.45, 0.1184, 0.1323, 0.077, 0.22399999999999998, 0.012, 0.1482, 0.2015, 0.5612, 0.6478, 0.459, 0.1914, 0.268, 0.17800000000000002, 0.0356, 0.1281, 0.5922, 0.0846, 0.13720000000000002], [0.6248, 0.0, 0.45119999999999993, 0.036, 0.576, 0.48, 0.6384, 0.5644, 0.3773, 0.142, 0.7744, 0.2772, 0.06709999999999999, 0.0868, 0.6, 0.0828, 0.5184, 0.388, 0.24640000000000004, 0.0576, 0.16240000000000002, 0.1598], [0.30150000000000005, 0.0088, 0.0675, 0.0475, 0.111, 0.1349, 0.0667, 0.0752, 0.1376, 0.20700000000000002, 0.0805, 0.376, 0.222, 0.03, 0.0954, 0.0105, 0.36000000000000004, 0.8277000000000001, 0.030600000000000002, 0.5456, 0.054, 0.06269999999999999], [0.012, 0.019500000000000003, 0.6384, 0.044000000000000004, 0.052199999999999996, 0.1701, 0.30820000000000003, 0.0135, 0.07379999999999999, 0.056999999999999995, 0.3692, 0.1014, 0.5304000000000001, 0.5040000000000001, 0.318, 0.0657, 0.0332, 0.0714, 0.0592, 0.54, 0.5301, 0.6975], [0.6768, 0.17250000000000001, 0.261, 0.2619, 0.030800000000000004, 0.384, 0.2379, 0.12240000000000001, 0.3402, 0.016800000000000002, 0.2112, 0.3996, 0.1566, 0.0528, 0.5184, 0.5599999999999999, 0.005200000000000001, 0.52, 0.05500000000000001, 0.301, 0.32480000000000003, 0.2223], [0.2601, 0.0624, 0.325, 0.0105, 0.27259999999999995, 0.266, 0.5304000000000001, 0.1848, 0.084, 0.296, 0.068, 0.6072, 0.357, 0.1296, 0.558, 0.17250000000000001, 0.23029999999999998, 0.6132, 0.3886, 0.33390000000000003, 0.2479, 0.5162], [0.2376, 0.3042, 0.027500000000000004, 0.0312, 0.4576, 0.144, 0.27540000000000003, 0.058499999999999996, 0.0344, 0.6971999999999999, 0.0396, 0.0936, 0.42350000000000004, 0.060500000000000005, 0.3471, 0.1767, 0.0376, 0.47600000000000003, 0.1586, 0.23029999999999998, 0.016, 0.1856], [0.1596, 0.3115, 0.6006, 0.06, 0.3111, 0.3886, 0.171, 0.058800000000000005, 0.066, 0.117, 0.195, 0.0217, 0.39, 0.15300000000000002, 0.06480000000000001, 0.35259999999999997, 0.3276, 0.1343, 0.5327999999999999, 0.23779999999999996, 0.0994, 0.7488], [0.04760000000000001, 0.1368, 0.0, 0.5626, 0.36, 0.6956, 0.21239999999999998, 0.52, 0.3075, 0.567, 0.6318, 0.018, 0.010799999999999999, 0.0945, 0.0221, 0.064, 0.19440000000000002, 0.0033, 0.5022, 0.12420000000000002, 0.7626, 0.066], [0.0124, 0.5829000000000001, 0.268, 0.6478, 0.049199999999999994, 0.126, 0.08820000000000001, 0.5035, 0.0, 0.174, 0.4232, 0.3675, 0.3843, 0.3192, 0.0234, 0.44839999999999997, 0.8063999999999999, 0.028199999999999996, 0.049, 0.14850000000000002, 0.1023, 0.8316]]
        result = self.collectable_generator.layer(weights_1, weights_2)
        self.assertEqual(result, expected_result)
        
    def test_map_threshold(self) -> None:
        weights = [[.2, .4], [.5, .3]]
        expected_result = [[False, True], [True, False]]
        result = self.collectable_generator.map_threshold(.4, weights)
        self.assertEqual(result, expected_result)