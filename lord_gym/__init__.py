from gym.envs.registration import register

register(
    id='lord-v0',
    entry_point='lord_gym.envs:LordEnv',
)