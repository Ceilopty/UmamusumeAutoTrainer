import random
from module.umamusume.context import UmamusumeContext
try:
    from module.umamusume.script.ura.team_stadium_opponent_selector import ura_select_opponent
except ImportError:
    def ura_select_opponent(ctx: UmamusumeContext):
        return
    print("未找到URA相关组件")


def select_opponent(ctx: UmamusumeContext) -> int:
    if index := ura_select_opponent(ctx):
        return index
    index = ctx.team_stadium_detail.opponent_index
    if index is not None:
        if index:
            return index
    return random.randint(1, 3)
