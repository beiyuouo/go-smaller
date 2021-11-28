#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   my_submission\bbot.py 
@Time    :   2021-11-25 09:51:06 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

import random
import os
import logging
import copy
import queue
import numpy as np
from pygame.math import Vector2
from gobigger.agents import BotAgent
from gobigger.balls import FoodBall


class BBot(BotAgent):
    def __init__(self, name=None, level=4):
        super().__init__(name=name, level=level)

    def step(self, obs):
        if self.level == 1:
            return self.step_level_1(obs)
        if self.level == 2:
            return self.step_level_2(obs)
        if self.level == 3:
            return self.step_level_3(obs)
        if self.level == 4:
            return self.step_level_4(obs)

    def step_level_4(self, obs):
        if self.actions_queue.qsize() > 0:
            return self.actions_queue.get()
        overlap = obs['overlap']
        overlap = self.preprocess(overlap)
        food_balls = overlap['food']
        thorns_balls = overlap['thorns']
        spore_balls = overlap['spore']
        clone_balls = overlap['clone']

        my_clone_balls, others_clone_balls = self.process_clone_balls(clone_balls)

        if len(my_clone_balls) >= 9 and my_clone_balls[4]['radius'] > 14:
            self.merge_actions(my_clone_balls)
            action_ret = self.actions_queue.get()
            return action_ret

        if len(others_clone_balls
               ) > 0 and my_clone_balls[0]['radius'] < others_clone_balls[0]['radius']:
            direction = (my_clone_balls[0]['position'] -
                         others_clone_balls[0]['position']).normalize()
            action_type = -1
            self.actions_queue.put([direction.x, direction.y, 1])
        else:
            if len(others_clone_balls) > 0:
                if len(my_clone_balls) >= 9 and my_clone_balls[4]['radius'] > 10:
                    self.merge_actions(my_clone_balls)

                flag = False
                for i in range(len(others_clone_balls)):
                    if others_clone_balls[i][
                            'radius'] < my_clone_balls[0]['radius'] // 2 and self.get_distance(
                                others_clone_balls[i]['position'], my_clone_balls[0]
                                ['position']) < my_clone_balls[0]['radius'] * 2:
                        direction = (others_clone_balls[i]['position'] -
                                     my_clone_balls[0]['position']).normalize()
                        self.actions_queue.put([direction.x, direction.y, 1])
                        flag = True
                        break

                    if others_clone_balls[i][
                            'radius'] < my_clone_balls[0]['radius'] // 4 and self.get_distance(
                                others_clone_balls[i]['position'], my_clone_balls[0]
                                ['position']) < my_clone_balls[0]['radius'] * 3:
                        direction = (others_clone_balls[i]['position'] -
                                     my_clone_balls[0]['position']).normalize()
                        self.actions_queue.put([direction.x, direction.y, 1])
                        self.actions_queue.put([direction.x, direction.y, 1])
                        flag = True
                        break

                if not flag:
                    direction = (my_clone_balls[0]['position'] -
                                 others_clone_balls[0]['position']).normalize()
                    direction = self.add_noise_to_direction(direction)
                    action_type = -1
                    self.actions_queue.put([direction.x, direction.y, action_type])

            else:
                min_distance, min_thorns_ball = self.process_thorns_balls(
                    thorns_balls, my_clone_balls[0])
                if min_thorns_ball is not None:
                    direction = (min_thorns_ball['position'] -
                                 my_clone_balls[0]['position']).normalize()
                else:
                    min_distance, min_food_ball = self.process_food_balls(
                        food_balls, my_clone_balls[0])
                    if min_food_ball is not None:
                        direction = (min_food_ball['position'] -
                                     my_clone_balls[0]['position']).normalize()
                    else:
                        direction = (Vector2(0, 0) - my_clone_balls[0]['position']).normalize()
                action_random = random.random()
                if action_random < 0.02:
                    action_type = 1
                elif action_random < 0.04 and action_random > 0.02:
                    action_type = 2
                else:
                    action_type = -1
                # direction = self.add_noise_to_direction(direction)
                self.actions_queue.put([direction.x, direction.y, action_type])

        action_ret = self.actions_queue.get()
        return action_ret

    def get_centroid(self, balls):
        centroid = Vector2(0, 0)
        for ball in balls:
            centroid += ball['position']
        return centroid / len(balls)

    def get_distance(self, position1, position2):
        return (position1 - position2).length()

    def process_food_balls(self, food_balls, my_max_clone_ball):
        min_distance = 5
        min_food_ball = None
        for food_ball in food_balls:
            distance = (food_ball['position'] - my_max_clone_ball['position']).length()
            if distance < min_distance:
                min_distance = distance
                min_food_ball = copy.deepcopy(food_ball)
        if min_food_ball is not None or food_balls == []:
            return min_distance, min_food_ball

        food_ball_centroid = self.get_centroid(food_balls)
        min_distance = 10000
        min_food_ball = None
        for food_ball in food_balls:
            distance = (food_ball['position'] - food_ball_centroid).length() + (
                food_ball['position'] - my_max_clone_ball['position']).length()
            if distance < min_distance:
                min_distance = distance
                min_food_ball = copy.deepcopy(food_ball)

        return min_distance, min_food_ball

    def merge_actions(self, my_clone_balls):
        self.actions_queue.put([None, None, 2])
        self.actions_queue.put([None, None, -1])
        self.actions_queue.put([None, None, -1])
        self.actions_queue.put([None, None, -1])
        self.actions_queue.put([None, None, -1])
        self.actions_queue.put([None, None, -1])
        self.actions_queue.put([None, None, -1])
        centroid = self.get_centroid(my_clone_balls)
        direction = (centroid - my_clone_balls[0]['position']).normalize()
        self.actions_queue.put([direction.x, direction.y, 0])
        self.actions_queue.put([direction.x, direction.y, 0])
        self.actions_queue.put([direction.x, direction.y, 0])
        self.actions_queue.put([direction.x, direction.y, 0])
        self.actions_queue.put([direction.x, direction.y, 0])
        self.actions_queue.put([direction.x, direction.y, 0])
        self.actions_queue.put([direction.x, direction.y, 0])
        self.actions_queue.put([direction.x, direction.y, 0])