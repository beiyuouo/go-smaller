exp_config = {
    'env': {
        'manager': {
            'episode_num': float("inf"),
            'max_retry': 5,
            'step_timeout': 60,
            'auto_reset': True,
            'reset_timeout': 60,
            'retry_waiting_time': 0.1,
            'shared_memory': False,
            'context': 'spawn',
            'wait_num': float("inf"),
            'step_wait_timeout': None,
            'connect_timeout': 60,
            'force_reproducibility': False,
            'cfg_type': 'SyncSubprocessEnvManagerDict'
        },
        'collector_env_num': 8,
        'evaluator_env_num': 3,
        'n_evaluator_episode': 3,
        'stop_value': 10000000000.0,
        'player_num_per_team': 3,
        'team_num': 4,
        'match_time': 200,
        'map_height': 1000,
        'map_width': 1000,
        'resize_height': 160,
        'resize_width': 160,
        'spatial': False,
        'speed': False,
        'all_vision': False,
        'train': True
    },
    'policy': {
        'model': {
            'scalar_shape': 50,
            'per_unit_shape': 31,
            'action_type_shape': 16,
            'rnn': False
        },
        'learn': {
            'learner': {
                'train_iterations': 1000000000,
                'dataloader': {
                    'num_workers': 0
                },
                'hook': {
                    'load_ckpt_before_run': '',
                    'log_show_after_iter': 100,
                    'save_ckpt_after_iter': 10000,
                    'save_ckpt_after_run': True
                },
                'cfg_type': 'BaseLearnerDict'
            },
            'multi_gpu': False,
            'update_per_collect': 4,
            'batch_size': 128,
            'learning_rate': 0.0003,
            'target_update_freq': 100,
            'ignore_done': True
        },
        'collect': {
            'collector': {
                'deepcopy_obs': False,
                'transform_obs': False,
                'collect_print_freq': 100,
                'cfg_type': 'BattleSampleSerialCollectorDict'
            },
            'unroll_len': 1,
            'n_sample': 128
        },
        'eval': {
            'evaluator': {
                'eval_freq': 1000,
                'cfg_type': 'BattleInteractionSerialEvaluatorDict',
                'stop_value': 10000000000.0,
                'n_episode': 3
            }
        },
        'other': {
            'replay_buffer': {
                'type': 'naive',
                'replay_buffer_size': 20000,
                'deepcopy': False,
                'enable_track_used_data': False,
                'periodic_thruput_seconds': 60,
                'cfg_type': 'NaiveReplayBufferDict'
            },
            'eps': {
                'type': 'exp',
                'start': 0.95,
                'end': 0.1,
                'decay': 100000
            }
        },
        'type': 'dqn',
        'cuda': True,
        'on_policy': False,
        'priority': False,
        'priority_IS_weight': False,
        'discount_factor': 0.99,
        'nstep': 3,
        'cfg_type': 'DQNPolicyDict'
    },
    'exp_name': 'gobigger_no_spatial_baseline_dqn',
    'seed': 0
}
