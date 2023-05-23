from __future__ import annotations
from typing import Callable, TypeVar, Generic
from tech import Tech, techs, TechInfo
from player_functions import PlayerFunctions
from functools import reduce

T = TypeVar('T')
E = TypeVar('E')
class Tree(Generic[T]):
    def __init__(self, value: T, subs: list[Tree[T]]):
        self.value = value
        self.subs = subs
        
    def fmap(self, func: Callable[[T], E]) -> Tree[E]:
        return Tree(func(self.value), list(map(lambda sub : sub.fmap(func), self.subs)))
    
class TechTree:
    """
    Represents a single player's tech tree

    Contains all functionality for researching and tech effects

    [Note]: This class does not handle cost validation or taking research points away from the player
    """
    def __init__(self, player_functions: PlayerFunctions):
        self.tree = self.build_tree(player_functions)
        self.research('Mining Robotics')
        
    def tech_names(self) -> list[str]:
        """
        Returns a list of all techs that are in the tech tree regardless of whether or not they are
        researched in no particular order
        """
        def tree_names(tree: Tree[tuple[Tech, bool]]) -> list[str]:
            return [tree.value[0].name] + reduce(lambda x, y : x + y, map(tree_names, tree.subs), [])
        return tree_names(self.tree)
    
    def researched_techs(self) -> list[str]:
        """
        Returns a list of all of the techs that are researched in this tech tree
        """
        def tree_researched(tree: Tree[tuple[Tech, bool]]) -> list[str]:
            sub_researched = reduce(lambda x, y : x + y, list(map(tree_researched, tree.subs)), [])
            return [tree.value[0].name] + sub_researched if tree.value[1] else sub_researched
        return tree_researched(self.tree)
    
    def is_researched(self, tech_name: str) -> bool:
        """
        Returns whether or not the tech with the given name is researched
        """
        return tech_name in self.researched_techs()
    
    def research(self, tech_name: str) -> bool:
        """
        Takes the name of the tech to research and returns whether or not it was successfully researched
        """
        # Don't allow EMPs and Trap Detection to both be researched
        if tech_name == 'EMPs' and self.is_researched('Trap Detection') or tech_name == 'Trap Detection' and self.is_researched('EMPs'):
            return False
        
        def research_tree(tree: Tree[tuple[Tech, bool]]) -> bool:
            if tree.value[1]:
                return any(map(research_tree, tree.subs))
            else:
                if tree.value[0].name == tech_name:
                    tree.value = (tree.value[0], True)
                    return True
                return False
        return research_tree(self.tree)
    
    def tech_info(self, tech_name: str) -> TechInfo | None:
        """
        Returns a TechInfo object about the tech with the given name if the tech is found in the tree.
        Returns None if the tech isn't found
        """
        def search_tree(tree: Tree[tuple[Tech, bool]]) -> TechInfo | None:
            if tree.value[0].name == tech_name:
                return TechInfo(name=tree.value[0].name, cost=tree.value[0].cost, point_value=tree.value[0].point_value)
            return reduce(lambda acc, x : x if x is not None else acc, map(search_tree, tree.subs), None)
        return search_tree(self.tree)
    
    def score(self) -> int:
        """
        Returns the total score of the tree. This is done by summing the point values of all of the techs
        that are researched
        """
        def tree_score(tree: Tree[tuple[Tech, bool]]) -> int:
            return (tree.value[0].point_value if tree.value[1] else 0) + sum(map(tree_score, tree.subs))
        return tree_score(self.tree)
        
    def build_tree(self, player_functions: PlayerFunctions) -> Tree[tuple[Tech, bool]]:
        """
        This handles putting the techs together into the proper tree structure
        """
        this_techs = techs(player_functions=player_functions)
        
        tree: Tree[tuple[Tech, bool]] = Tree(
            value=this_techs['Mining Robotics'],
            subs=[
                Tree(
                    value=this_techs['Better Drivetrains'],
                    subs=[
                        Tree(
                            value=this_techs['Unnamed Drivetrain Tech'],
                            subs=[
                                Tree(
                                    value=this_techs['Overdrive Movement'],
                                    subs=[]
                                )
                            ]
                        )
                    ]
                ),
                Tree(
                    value=this_techs['High Yield Drilling'],
                    subs=[
                        Tree(
                            value=this_techs['Unnamed Mining Tech'],
                            subs=[
                                Tree(
                                    value=this_techs['Overdrive Mining'],
                                    subs=[]
                                )
                            ]
                        ),
                        Tree(
                            value=this_techs['Dynamite'],
                            subs=[
                                Tree(
                                    value=this_techs['Landmines'],
                                    subs=[
                                        Tree(
                                            value=this_techs['EMPs'],
                                            subs=[]
                                        ),
                                        Tree(
                                            value=this_techs['Trap Detection'],
                                            subs=[]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ).fmap(lambda tech : (tech, False))
        
        return tree