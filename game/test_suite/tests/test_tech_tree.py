import unittest
from unittest.mock import Mock

from game.quarry_rush.avatar.avatar_functions import AvatarFunctions
from game.quarry_rush.tech.tech_tree import TechTree

class TestTechTree(unittest.TestCase):
    def setUp(self):
        self.mock_increase_movement = Mock()
        self.mock_increase_mining = Mock()
        self.mock_unlock_movement_overdrive = Mock()
        self.mock_unlock_mining_overdrive = Mock()
        self.mock_unlock_dynamite = Mock()
        self.mock_unlock_landmines = Mock()
        self.mock_unlock_emps = Mock()
        self.mock_unlock_trap_defusal = Mock()
        self.avatar_functions = AvatarFunctions(increase_movement=self.mock_increase_movement,
                                                increase_mining=self.mock_increase_mining,
                                                unlock_movement_overdrive=self.mock_unlock_movement_overdrive,
                                                unlock_mining_overdrive=self.mock_unlock_mining_overdrive,
                                                unlock_dynamite=self.mock_unlock_dynamite,
                                                unlock_landmines=self.mock_unlock_landmines,
                                                unlock_emps=self.mock_unlock_emps,
                                                unlock_trap_defusal=self.mock_unlock_trap_defusal)
        
        self.tech_tree = TechTree(self.avatar_functions)
        
    def test_tech_names(self):
        names = self.tech_tree.tech_names()
        self.assertEqual(names, ['Mining Robotics', 'Better Drivetrains', 'Unnamed Drivetrain Tech', 'Overdrive Movement', 'High Yield Drilling', 'Unnamed Mining Tech', 'Overdrive Mining', 'Dynamite', 'Landmines', 'EMPs', 'Trap Defusal'])
        
    def test_researched_techs(self):
        names = self.tech_tree.researched_techs()
        self.assertEqual(names, ['Mining Robotics'])
        
    def test_research(self):
        result1 = self.tech_tree.research('Better Drivetrains')
        result2 = self.tech_tree.research('Invalid Tech Name')
        names = self.tech_tree.researched_techs()
        self.assert_(result1)
        self.assertFalse(result2)
        self.assertEqual(names, ['Mining Robotics', 'Better Drivetrains'])
        self.mock_increase_movement.assert_called_once_with(1)
        
    def test_illegal_research(self):
        result = self.tech_tree.research('EMPs')
        names = self.tech_tree.researched_techs()
        self.assertFalse(result)
        self.assertEqual(names, ['Mining Robotics'])
        self.mock_unlock_emps.assert_not_called()
        
    def test_research_emp_with_detection(self):
        self.tech_tree.research('High Yield Drilling')
        self.tech_tree.research('Dynamite')
        self.tech_tree.research('Landmines')
        self.tech_tree.research('Trap Defusal')
        result = self.tech_tree.research('EMPs')
        names = self.tech_tree.researched_techs()
        self.assertFalse(result)
        self.assertEqual(names, ['Mining Robotics', 'High Yield Drilling', 'Dynamite', 'Landmines', 'Trap Defusal'])
        self.mock_unlock_trap_defusal.assert_called_once()
        self.mock_unlock_emps.assert_not_called()
        
    def test_research_detection_with_emp(self):
        self.tech_tree.research('High Yield Drilling')
        self.tech_tree.research('Dynamite')
        self.tech_tree.research('Landmines')
        self.tech_tree.research('EMPs')
        result = self.tech_tree.research('Trap Defusal')
        names = self.tech_tree.researched_techs()
        self.assertFalse(result)
        self.assertEqual(names, ['Mining Robotics', 'High Yield Drilling', 'Dynamite', 'Landmines', 'EMPs'])
        self.mock_unlock_emps.assert_called_once()
        self.mock_unlock_trap_defusal.assert_not_called()
        
    def test_is_researched(self):
        self.tech_tree.research('Better Drivetrains')
        result1 = self.tech_tree.is_researched('Better Drivetrains')
        result2 = self.tech_tree.is_researched('EMPs')
        result3 = self.tech_tree.is_researched('Invalid Tech Name')
        self.assert_(result1)
        self.assertFalse(result2)
        self.assertFalse(result3)
        
    def test_tech_info(self):
        better_drivetrain_info = {'name': 'Better Drivetrains', 'cost': 0, 'point_value': 1}
        result1 = self.tech_tree.tech_info('Better Drivetrains')
        result2 = self.tech_tree.tech_info('Invalid Tech Name')
        self.assertEqual(better_drivetrain_info['name'], result1.name)
        self.assertEqual(better_drivetrain_info['cost'], result1.cost)
        self.assertEqual(better_drivetrain_info['point_value'], result1.point_value)
        self.assertIsNone(result2)
        
    def test_score(self):
        self.tech_tree.research('Better Drivetrains')
        self.tech_tree.research('High Yield Drilling')
        self.tech_tree.research('Dynamite')
        result = self.tech_tree.score()
        self.assertEqual(result, 3)

    def test_tech_tree_json(self):
        self.tech_tree.research('High Yield Drilling')
        self.tech_tree.research('Unnamed Mining Tech')
        result = self.tech_tree.to_json()
        for tech in self.tech_tree.tech_names():
            self.assertEqual(result[tech], self.tech_tree.is_researched(tech))
        # self.assertEqual(self.avatar_functions, result['avatar_functions'])
