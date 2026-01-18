import time
from module.umamusume.task import UmamusumeTaskType
from module.umamusume.context import UmamusumeContext
import bot.base.log as logger

log = logger.get_logger(__name__)


def on_task(ctx: UmamusumeContext, task_type: UmamusumeTaskType):
    return ctx.task.task_type == task_type


def set_timestamp(ctx: UmamusumeContext, name: str, offset=None):
    offset = offset or 0
    ctx.task.detail.timestamp[name][ctx.task.device_name or "default"] = time.time() + offset


def get_timestamp(ctx: UmamusumeContext, name: str):
    return ctx.task.detail.timestamp[name].get(ctx.task.device_name or "default")


def script_common_not_found_ui(ctx: UmamusumeContext):
    ctx.ctrl.click(719, 1, "")
    time.sleep(0.2)
    ts = get_timestamp(ctx, 'not_found_ui')
    if not ts or time.time() - ts > 3:
        ctx.task.detail.not_found_ui = 1
    else:
        ctx.task.detail.not_found_ui += 1
    set_timestamp(ctx, 'not_found_ui')
    if ctx.task.detail.not_found_ui > 20:
        from bot.base.manifest import APP_MANIFEST_LIST
        manifest = APP_MANIFEST_LIST[ctx.task.app_name]
        ctx.ctrl.stop_app(manifest.app_package_name)
        time.sleep(5)
        ctx.ctrl.start_app(manifest.app_package_name)
        ctx.task.detail.not_found_ui = 0


def script_common_not_found_script(ctx: UmamusumeContext):
    log.error("未找到此界面对应的默认脚本:%s", ctx.current_ui.ui_name)
    time.sleep(0.2)
    ts = get_timestamp(ctx, 'not_found_script')
    if not ts or time.time() - ts > 3:
        ctx.task.detail.not_found_script = 1
    else:
        ctx.task.detail.not_found_script += 1
    set_timestamp(ctx, 'not_found_script')
    if ctx.task.detail.not_found_script > 20:
        from bot.base.manifest import APP_MANIFEST_LIST
        manifest = APP_MANIFEST_LIST[ctx.task.app_name]
        ctx.ctrl.stop_app(manifest.app_package_name)
        time.sleep(5)
        ctx.ctrl.start_app(manifest.app_package_name)
        ctx.task.detail.not_found_script = 0
