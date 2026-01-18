import csv
import datetime
import json
import os
import time
from bot.base.user_data import base_path,  write_file

_LOCALAPPDATA = os.environ.get('LOCALAPPDATA')
_GAME_DATA_FOLDER = os.path.join(_LOCALAPPDATA,
                                 "UmamusumeResponseAnalyzer",
                                 "GameData")
CIRCLE_DATA_FILEPATH = os.path.join(_GAME_DATA_FOLDER,
                                    "Circle")
OUTPUT = '/umamusume/circle/%s.csv'

filepath = os.path.dirname(base_path + OUTPUT)
if not os.path.exists(filepath):
    os.makedirs(filepath)


class Member:
    def __init__(self,
                 viewer_id: int,
                 name: str,
                 last_login_time: str,
                 comment: str,
                 fan: int,
                 team_stadium_win_count: int,
                 single_mode_play_count: int,
                 team_evaluation_point: int,
                 ):
        self.viewer_id = viewer_id
        self.name = name
        self.last_login_time = datetime.datetime.fromisoformat(last_login_time)
        self.comment = comment
        self.fan = fan
        self.team_stadium_win_count = team_stadium_win_count
        self.single_mode_play_count = single_mode_play_count
        self.team_evaluation_point = team_evaluation_point


class Circle:
    def __init__(self,
                 circle_id: int,
                 name: str,
                 member_num: int,
                 members: list[Member | dict],
                 ):
        self.circle_id = circle_id
        self.name = name
        self.member_num = member_num
        self.members = [member if isinstance(member, Member) else Member(**member) for member in members]


def hook(dct):
    if all(attr in dct for attr in Circle.__init__.__annotations__):
        return Circle(**dct)
    if all(attr in dct for attr in Member.__init__.__annotations__):
        return Member(**dct)
    return dct


def get_js_path():
    return [file.name for file in os.scandir(CIRCLE_DATA_FILEPATH) if file.is_file() and file.name.endswith('.json')]


def read_file(file_path):
    if not file_path.startswith("Circle_"):
        return None, None
    t = time.strptime(file_path[7:-9], "%y-%m-%d %H-%M-%S")
    file_path = os.path.join(CIRCLE_DATA_FILEPATH, file_path)
    with open(file_path, encoding='utf-8') as f:
        try:
            js = json.load(f, object_hook=hook)
        except:
            print(file_path)
            return t, None
    year = time.ctime(os.path.getctime(file_path))[-4:]
    return time.struct_time([int(year), *t[1:]]), js


def main(cap=None, com=False, same_month=False):
    """
    计算粉丝数
    cap: 取后若干条
    com: 合并同日数据
    same_month: 仅取当月数据
    """
    res = {}
    times = {}
    members = {}
    circles = {}
    for t, js in sorted([(t, js) for t, js in [read_file(x) for x in get_js_path()] if t and js]):
        members.setdefault(js.circle_id, {})
        times.setdefault(js.circle_id, [])
        res.setdefault(js.circle_id, {})
        circles.setdefault(js.circle_id, js.name)
        times[js.circle_id].append(t)
        members[js.circle_id].update({member.viewer_id: member.name for member in js.members})
        for member in js.members:
            res[js.circle_id].setdefault(member.viewer_id, {})
            res[js.circle_id][member.viewer_id][t] = member.fan / 10000
    output = []
    for circle in times:
        if same_month:
            # 仅保留上月最后一条数据（如有）和当月数据
            temp = times[circle][:1]
            for t in times[circle][1:]:
                # 非当月
                if (_date(times[circle][-1])[1] - _date(t)[1]) % 12:
                    temp.pop()
                temp.append(t)
            times[circle][:] = temp[:]
            del temp
        if com:
            # 同一日期仅取1条数据
            temp = times[circle][:1]
            for t in times[circle][1:]:
                if _date(t) == _date(temp[-1]):
                    temp.pop()
                temp.append(t)
            times[circle][:] = temp[:]
            del temp
        if cap is not None:
            # 截取后若干条数据
            if isinstance(cap, int):
                times[circle][:] = times[circle][-cap:]
            # 截取后若干条数据
            elif isinstance(cap, float):
                times[circle][:] = [t for t in times[circle][:-1]
                                    if time.mktime(times[circle][-1]) - time.mktime(t) < cap * 86400
                                    ] + times[circle][-1:]
        t = ["昵称"] + [time.strftime("'%Y-%m-%d %H:%M", t) for t in times[circle]] + ["日均", "昵称", "排名"]
        f = [(members[circle][viewer_id],
              [fan_dict.get(i, None) for i in times[circle]],
              86400 / (time.mktime(_max) - time.mktime(_min)) * (fan_dict[_max] - fan_dict[_min])
              if (_max := max(_t)) != (_min := min(_t)) else 0,
              ) for viewer_id, fan_dict in res[circle].items()
             if any(_t := set(fan_dict).intersection(set(times[circle])))]
        f = [[r[0]] + r[1] + [r[2], r[0]] for r in f]
        f.sort(key=lambda x: (-max(i for i in range(1, len(x)-2) if x[i]), -x[-2], x[-1]))
        f = map(_str, f)
        f = (list(j) + [i] for i, j in enumerate(f, start=1))
        output.append((circle, t, f))
    for circle, t, f in output:
        with open((base_path + OUTPUT) % '_'.join(map(str, (circles.get(circle, ""), cap, com, same_month))),
                  mode='w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(t)
            csv_writer.writerows(f)


def _str(fan, digit=0):
    if fan is None:
        return ""
    if isinstance(fan, (float, int)):
        return f"'%{digit}.4f" % fan
    if isinstance(fan, str):
        return fan
    return map(_str, fan)


def _date(t: time.struct_time) -> tuple[int, int, int]:
    return time.localtime(time.mktime(t) - (86400 if t[3] < 5 else 0))[:3]


if __name__ == '__main__':
    main(None, True, True)
