"""
Bot using Monte Carlo Tree Search

Algorithm:
- Score each legal move using heuristic
- Sample 3 ~ 5 moves at each node with either: thompson sampling (better score moves more likely) or PUCT
- Repeat until certain depth
- Back-propagate (how?)
"""