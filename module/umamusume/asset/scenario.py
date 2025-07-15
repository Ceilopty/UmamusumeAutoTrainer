import csv
import os.path

from bot.base.resource import Template
from module.umamusume.define import ScenarioType

SCENARIO_DICT: dict[ScenarioType, list] = {}
UMAMUSUME_SCENARIO_TEMPLATE_PATH = "/umamusume/scenario"


def load_scenario_data():
    with open('resource/umamusume/data/scenario.csv', 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            scenario_id = int(row[0])
            scenario_type = ScenarioType(scenario_id)
            path = "resource" + UMAMUSUME_SCENARIO_TEMPLATE_PATH + "/" + str(scenario_id)+".png"
            if os.path.isfile(path):
                t = Template(str(scenario_id), UMAMUSUME_SCENARIO_TEMPLATE_PATH)
                scenario_name = row[1]
                scenario_info = [scenario_id, scenario_name, t]
                SCENARIO_DICT[scenario_type] = scenario_info


load_scenario_data()
