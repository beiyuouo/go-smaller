import random
import os
import logging
import copy
import queue
from pygame.math import Vector2
from .bbot import BBot


class BaseSubmission:
    def __init__(self, team_name, player_names):
        self.team_name = team_name
        self.player_names = player_names

    def get_actions(self, obs):
        '''
        Overview:
            You must implement this function.
        '''
        raise NotImplementedError


class MySubmission(BaseSubmission):
    def __init__(self, team_name, player_names):
        super(MySubmission, self).__init__(team_name, player_names)
        self.agents = {}
        for player_name in self.player_names:
            self.agents[player_name] = BBot(name=player_name)

    def get_actions(self, obs):
        global_state, player_states = obs
        actions = {}
        for player_name, agent in self.agents.items():
            action = agent.step(player_states[player_name])
            actions[player_name] = action
        return actions