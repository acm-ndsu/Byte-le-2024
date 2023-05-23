from __future__ import annotations
from typing import Callable, TypeVar, Generic
from tech import Tech, techs
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
    def __init__(self, player_functions: PlayerFunctions):
        self.tree = self.build_tree(player_functions)
        self.research('Mining Robotics')
        
    def tech_names(self) -> list[str]:
        def tree_names(tree: Tree[tuple[Tech, bool]]) -> list[str]:
            return [tree.value[0].name] + reduce(lambda x, y : x + y, map(tree_names, tree.subs), [])
        return tree_names(self.tree)
    
    def researched_techs(self) -> list[str]:
        def tree_researched(tree: Tree[tuple[Tech, bool]]) -> list[str]:
            sub_researched = reduce(lambda x, y : x + y, list(map(tree_researched, tree.subs)), [])
            return [tree.value[0].name] + sub_researched if tree.value[1] else sub_researched
        return tree_researched(self.tree)
    
    def research(self, tech_name: str) -> bool:
        def research_tree(tree: Tree[tuple[Tech, bool]]) -> bool:
            if tree.value[1]:
                return any(map(research_tree, tree.subs))
            else:
                if tree.value[0].name == tech_name:
                    tree.value = (tree.value[0], True)
                    return True
                return False
        return research_tree(self.tree)
    
    def cost_of(self, tech_name: str) -> int:
        def search_tree(tree: Tree[tuple[Tech, bool]]) -> int:
            return max(tree.value[0].cost if tree.value[0].name == tech_name else -1, max([-1] + list(map(search_tree, tree.subs))))
        return search_tree(self.tree)
    
    def score(self) -> int:
        def tree_score(tree: Tree[tuple[Tech, bool]]) -> int:
            return (tree.value[0].point_value if tree.value[1] else 0) + sum(map(tree_score, tree.subs))
        return tree_score(self.tree)
        
    def build_tree(self, player_functions: PlayerFunctions) -> Tree[tuple[Tech, bool]]:
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