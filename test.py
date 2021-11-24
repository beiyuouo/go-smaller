import os
import sys
import logging
import importlib
import time
import argparse
import subprocess
from tqdm import tqdm
import tarfile

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_AUDIODRIVER'] = 'dsp'

from gobigger.agents import BotAgent
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender

logging.basicConfig(level=logging.DEBUG)


def test():
    server = Server(
        dict(
            team_num=4,  # 队伍数量
            player_num_per_team=3,  # 每个队伍的玩家数量
            match_time=30,  # 每场比赛的持续时间
        ))
    render = EnvRender(server.map_width, server.map_height)
    server.set_render(render)
    server.start()
    agents = []
    team_player_names = server.get_team_names()
    team_names = list(team_player_names.keys())
    for index in range(server.team_num):
        try:
            p = importlib.import_module('my_submission.my_submission')
            agents.append(
                p.MySubmission(team_name=team_names[index],
                               player_names=team_player_names[team_names[index]]))
        except Exception as e:
            print('You must implement `MySubmission` in my_submission.py !')
            exit()

    for i in tqdm(range(30 * server.action_tick_per_second)):
        obs = server.obs()
        global_state, player_states = obs
        actions = {}
        for agent in agents:
            agent_obs = [
                global_state,
                {player_name: player_states[player_name]
                 for player_name in agent.player_names}
            ]
            actions.update(agent.get_actions(agent_obs))
        finish_flag = server.step(actions=actions)
        if finish_flag:
            logging.debug('Game Over!')
            break
    server.close()
    print('Success!')


def cache_filter(tarinfo):
    if '__pycache__' in tarinfo.name or '.pytest' in tarinfo.name:
        return None
    return tarinfo


def make_targz(output_filename, source_dir):
    try:
        with tarfile.open(output_filename, "w:gz", format=tarfile.GNU_FORMAT) as tar:
            # tar.add(source_dir, filter=cache_filter)
            for root, dir, files in os.walk(source_dir):
                for file in files:
                    tar.add(os.path.join(root, file), filter=cache_filter)

        return True
    except Exception as e:
        print(e)
        return False


def postprocess():
    # logging.debug('tar zcf my_submission.tar.gz my_submission/')
    # output = subprocess.getoutput('tar zcf my_submission.tar.gz my_submission/')
    make_targz('my_submission.tar.gz', 'my_submission')
    assert os.path.isfile('my_submission.tar.gz')
    print('###################################################################')
    print('#                                                                 #')
    print('#   Now you can upload my_submission.tar.gz as your submission.   #')
    print('#                                                                 #')
    print('###################################################################')


if __name__ == '__main__':
    test()
    postprocess()
