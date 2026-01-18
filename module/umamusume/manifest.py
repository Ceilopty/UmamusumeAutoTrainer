from typing import Dict

from bot.base.manifest import AppManifest
from bot.base.resource import NOT_FOUND_UI
from bot.server.handler import server
from module.umamusume.asset.ui import *
from module.umamusume.context import build_context
from module.umamusume.hook import after_hook, before_hook
from module.umamusume.script.cultivate_task.cultivate import *
from module.umamusume.script.cultivate_task.info import script_info
from module.umamusume.script.team_stadium_task.race import (ts_script_main_menu,
                                                            ts_script_race_home,
                                                            script_team_stadium_home,
                                                            script_team_stadium_home_na,
                                                            script_team_stadium_select_opponent,
                                                            script_team_stadium_before_race,
                                                            script_team_stadium_check_all_results,
                                                            script_team_stadium_check_result,
                                                            script_team_stadium_results,
                                                            script_team_stadium_reward,
                                                            script_team_stadium_before_reward,
                                                            script_team_stadium_end,
                                                            script_team_stadium_high_score,
                                                            script_team_stadium_level_result,
                                                            )
from module.umamusume.script.time_sale.time_sale import (script_shop_main,
                                                         script_time_sale_main,
                                                         )
from module.umamusume.script.team_stadium_task.info import ts_script_info
from module.umamusume.script.donate_task.donate import (d_script_main_menu, script_guild_home,
                                                        script_circle_ranking_result,
                                                        )
from module.umamusume.script.donate_task.info import d_script_info
from module.umamusume.script.daily_schedule_task.race import (dr_script_main_menu,
                                                              dr_script_race_home,
                                                              dr_script_daily_schedule,
                                                              script_daily_race_dr_home,
                                                              script_daily_race_select_racer,
                                                              )
from module.umamusume.script.daily_schedule_task.info import dr_script_info
from module.umamusume.script.common.common import script_common_not_found_ui, script_common_not_found_script
from module.umamusume.protocol.preset import AddPresetRequest
from module.umamusume.task import UmamusumeTaskType, build_task
from module.umamusume.user_data import read_presets, write_preset

script_dicts: Dict[UmamusumeTaskType, dict] = {
    UmamusumeTaskType.UMAMUSUME_TASK_TYPE_CULTIVATE: {
        INFO: script_info,
        MAIN_MENU: script_main_menu,
        MAIN_MENU_CONTINUE: script_main_menu,
        CULTIVATE_SCENARIO_SELECT: script_scenario_select,
        CULTIVATE_UMAMUSUME_SELECT: script_umamusume_select,
        CULTIVATE_EXTEND_UMAMUSUME_SELECT: script_extend_umamusume_select,
        CULTIVATE_SUPPORT_CARD_SELECT: script_support_card_select,
        CULTIVATE_FOLLOW_SUPPORT_CARD_SELECT: script_follow_support_card_select,
        CULTIVATE_MAIN_MENU: script_cultivate_main_menu,
        CULTIVATE_TRAINING_SELECT: script_cultivate_training_select,
        CULTIVATE_FINAL_CHECK: script_cultivate_final_check,
        CULTIVATE_EVENT_UMAMUSUME: script_cultivate_event,
        CULTIVATE_EVENT_SUPPORT_CARD: script_cultivate_event,
        CULTIVATE_EVENT_SCENARIO: script_cultivate_event,
        AOHARUHAI_RACE_FINAL_START: script_aoharuhai_race_final_start,
        AOHARUHAI_RACE_SELECT_OPPONENT: script_aoharuhai_race_select_opponent,
        AOHARUHAI_RACE: script_aoharuhai_race,
        AOHARUHAI_RACE_INRACE: script_aoharuhai_race_inrace,
        AOHARUHAI_RACE_END: script_aoharuhai_race_end,
        AOHARUHAI_RACE_SCHEDULE: script_aoharuhai_race_schedule,
        CULTIVATE_GOAL_RACE: script_cultivate_goal_race,
        CULTIVATE_RACE_LIST: script_cultivate_race_list,
        BEFORE_RACE: script_cultivate_before_race,
        IN_RACE_UMA_LIST: script_cultivate_in_race_uma_list,
        IN_RACE: script_in_race,
        RACE_RESULT: script_cultivate_race_result,
        RACE_REWARD: script_cultivate_race_reward,
        GOAL_ACHIEVED: script_cultivate_goal_achieved,
        ALL_GOAL_ACHIEVED: script_cultivate_goal_achieved,
        NEXT_GOAL: script_cultivate_next_goal,
        CULTIVATE_EXTEND: script_cultivate_extend,
        CULTIVATE_RESULT: script_cultivate_result,
        CULTIVATE_RESULT_1: script_cultivate_result,
        CULTIVATE_RESULT_2: script_cultivate_result,
        CULTIVATE_CATCH_DOLL_GAME: script_cultivate_catch_doll,
        CULTIVATE_CATCH_DOLL_GAME_RESULT: script_cultivate_catch_doll_result,
        CULTIVATE_LEARN_SKILL: script_cultivate_learn_skill,
        CULTIVATE_FINISH: script_cultivate_finish,
        NOT_FOUND_UI: script_common_not_found_ui,
        RECEIVE_CUP: script_receive_cup,
        GOAL_FAILED: script_cultivate_goal_failed,
        CULTIVATE_LEVEL_RESULT: script_cultivate_level_result,
        FACTOR_RECEIVE: script_factor_receive,
        HISTORICAL_RATING_UPDATE: script_historical_rating_update,
        SCENARIO_RATING_UPDATE: script_scenario_rating_update,
        CULTIVATE_URA_RACE_1: script_cultivate_goal_race,
        CULTIVATE_URA_RACE_2: script_cultivate_goal_race,
        CULTIVATE_URA_RACE_3: script_cultivate_goal_race,
        ACTIVITY_RESULT: script_cultivate_result,
        ACTIVITY_REWARD: script_cultivate_result,
        FUJIKISEKI_SHOW_MODE_RESULT_1: script_fujikiseki_show_result_1,
        FUJIKISEKI_SHOW_MODE_RESULT_2: script_fujikiseki_show_result_2,
    },
    UmamusumeTaskType.UMAMUSUME_TASK_TYPE_TEAM_STADIUM: {
        MAIN_MENU: ts_script_main_menu,
        MAIN_MENU_CONTINUE: ts_script_main_menu,
        RACE_HOME: ts_script_race_home,
        TEAM_STADIUM_HOME: script_team_stadium_home,
        TEAM_STADIUM_HOME_NA: script_team_stadium_home_na,
        TEAM_STADIUM_SELECT_OPPONENT: script_team_stadium_select_opponent,
        TEAM_STADIUM_BEFORE_RACE: script_team_stadium_before_race,
        TEAM_STADIUM_CHECK_ALL_RESULTS: script_team_stadium_check_all_results,
        TEAM_STADIUM_CHECK_RESULT: script_team_stadium_check_result,
        AOHARUHAI_RACE_END: script_team_stadium_results,
        TEAM_STADIUM_RESULTS: script_team_stadium_results,
        TEAM_STADIUM_REWARD: script_team_stadium_reward,
        TEAM_STADIUM_BEFORE_REWARD: script_team_stadium_before_reward,
        TEAM_STADIUM_END: script_team_stadium_end,
        TEAM_STADIUM_HIGH_SCORE: script_team_stadium_high_score,
        TEAM_STADIUM_LEVEL_RESULT: script_team_stadium_level_result,
        TIME_SALE_MAIN: script_time_sale_main,
        SHOP_MAIN: script_shop_main,
        INFO: ts_script_info,
    },
    UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DONATE: {
        MAIN_MENU: d_script_main_menu,
        MAIN_MENU_CONTINUE: d_script_main_menu,
        GUILD_MAIN: script_guild_home,
        GUILD_MAIN_2: script_guild_home,
        CIRCLE_RANKING_RESULT: script_circle_ranking_result,
        INFO: d_script_info,
    },
    UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DAILY_SCHEDULE: {
        MAIN_MENU: dr_script_main_menu,
        MAIN_MENU_CONTINUE: dr_script_main_menu,
        RACE_HOME: dr_script_race_home,
        DAILY_SCHEDULE: dr_script_daily_schedule,
        DAILY_RACE_HOME: script_daily_race_dr_home,
        DAILY_RACE_SELECT_RACER: script_daily_race_select_racer,
        TIME_SALE_MAIN: script_time_sale_main,
        SHOP_MAIN: script_shop_main,
        INFO: dr_script_info,
    },
}

default_script_dict: Dict[UI, callable] = {
    PRESS_START: lambda ctx: ctx.ctrl.click(719, 1, "Press start."),
    NOT_FOUND_UI: script_common_not_found_ui
}


def exec_script(ctx: UmamusumeContext):
    if ctx.task.task_type in script_dicts:
        if ctx.current_ui in script_dicts[ctx.task.task_type]:
            script_dicts[ctx.task.task_type][ctx.current_ui](ctx)
            return
    if ctx.current_ui in default_script_dict:
        default_script_dict[ctx.current_ui](ctx)
    else:
        print("未找到此界面对应的默认脚本")
        script_common_not_found_script(ctx)


UmamusumeManifest = AppManifest(
    app_name="umamusume",
    app_package_name="com.bilibili.umamusu",
    app_activity_name="com.uo.sdk.SplashActivity",
    build_context=build_context,
    build_task=build_task,
    ui_list=scan_ui_list,
    script=exec_script,
    before_hook=before_hook,
    after_hook=after_hook
)


@server.post("/umamusume/get-presets")
def get_presets():
    return read_presets()


@server.post("/umamusume/add-presets")
def add_preset(req: AddPresetRequest):
    write_preset(req.preset)
    return
