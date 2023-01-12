import json
import os, sys
import sqlite3
import traceback
import datetime as datetime

from homeassistant.components.recorder import CONF_DB_URL, DEFAULT_DB_FILE, DEFAULT_URL
from homeassistant.core import Config, HomeAssistant

DOMAIN = "context_actions"

ATTR_NAME = "name"
DEFAULT_NAME = "CONTEXT ACTION"

def writeFile(filename, body):
    try:
        debug_data = body
    except:
        debug_data = "ERROR"

    debug_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename + ".txt"), "w")
    debug_file.write(str(debug_data))
    debug_file.close()


def setup(hass: HomeAssistant, config: Config):
    json_string = '{}'
    json_dict = json.loads(json_string)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "json.json"), 'w+') as json_file:
        json.dump(json_dict, json_file)
    
    # map actions
    context_actions_config = config.get('context_actions')


    context_action_items = []

    for context_action_config in context_actions_config:
        context_action_items.append(context_action_config.get('rule'))

    

    def state_into_json(call):
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        context_actions_config = config.get('context_actions')


        context_action_items = []

        for context_action_config in context_actions_config:
            context_action_items.append(context_action_config.get('rule'))

        try:
            debug_data = context_action_items
        except:
            debug_data = "ERROR"

        
        try:
            json_data = []
            context_action_id = 0

            for rule in context_action_items:
                try:
                    cond = None
                    for trigger in rule.get('trigger'):
                        c_type = trigger.get('type')
                        c_name = trigger.get('name')
                        
                        if c_type == 'light':
                            c_state = trigger.get('state')
                            if str(hass.states.get(c_name).as_dict().get("state")) == str(c_state):
                                if cond is None or cond is True:
                                    cond = True
                                else:
                                    cond = False
                            else:
                                cond = False
                        elif c_type == 'temperature':
                            c_min = trigger.get('min') or None
                            c_max = trigger.get('max') or None
                            try:
                                temperature = hass.states.get(c_name).as_dict().get("attributes").get("current_temperature") or None
                            except:
                                temperature = None
                            try:
                                con_min = temperature > c_min
                            except: 
                                if temperature is not None:
                                    con_min = True
                                else:
                                    con_min = False

                            try:
                                con_max = temperature < c_max
                            except:
                                if temperature is not None:
                                    con_max = True
                                else:
                                    con_max = False
                            
                            if con_min and con_max:
                                if cond is None or cond is True:
                                    cond = True
                                else:
                                    cond = False
                        elif c_type == 'state_if':
                            c_state = trigger.get('state')
                            if str(hass.states.get(c_name).as_dict().get("state")) == str(c_state):
                                if cond is None or cond is True:
                                    cond = True
                                else:
                                    cond = False
                            else:
                                cond = False
                        elif c_type == 'attr_if':
                            c_state = trigger.get('state')
                            c_attr = trigger.get('name_attribute')
                            if str(hass.states.get(c_name).as_dict().get("attributes").get(c_attr)) == str(c_state):
                                if cond is None or cond is True:
                                    cond = True
                                else:
                                    cond = False
                            else:
                                cond = False
                        elif c_type == 'time':
                            c_time_begin = trigger.get('begin')
                            c_time_end = trigger.get('end')
                            
                            c_time_begin_hh = c_time_begin.split(':')[0]
                            c_time_begin_mm = c_time_begin.split(':')[1]
                            c_time_end_hh = c_time_end.split(':')[0]
                            c_time_end_mm = c_time_end.split(':')[1]

                            now = datetime.datetime.now().strftime('%H:%M').split(":")

                            now_hh = now[0]
                            now_mm = now[1]

                            time_begin = int(c_time_begin_hh) + (int(c_time_begin_mm) / 60)
                            time_end = int(c_time_end_hh) + (int(c_time_end_mm) / 60)

                            time_now = int(now_hh) + (int(now_mm) / 60)

                            if time_end < time_begin:
                                if time_now > time_end:
                                    time_end = time_end + 24.0
                                elif time_now < time_begin:
                                    time_begin = time_begin - 24.0

                            if (time_begin < time_now) and (time_now < time_end):
                                if cond is None or cond is True:
                                    cond = True
                                else:
                                    cond = False
                            else:
                                cond = False

                        else:
                            cond = False
                                
                    if cond is True:
                        state_data = {}
                        context_action_data = {}
                        state_data["service"] = rule.get('action').get('service')
                        context_action_data['entitiy'] = hass.states.get(rule.get('action').get('entity')).as_dict().get('entity_id')
                        context_action_data['friendly_name'] = hass.states.get(rule.get('action').get('entity')).as_dict().get('attributes').get('friendly_name')
                        context_action_data['state_data'] = state_data
                        context_action_data['action_id'] = context_action_id
                        context_action_id = context_action_id + 1
                        json_data.append(context_action_data)
                    
                except Exception as e:
                    writeFile("except", str(traceback.format_exc()))

            json_path = f'/config/www/'
            with open(json_path + "json.json", "w") as json_file:
                json.dump(json_data, json_file)
            
        except:
            try:
                exception_string = traceback.format_exc()
                data_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt"), "w")
                data_file.write(str(exception_string))
                data_file.close()
            except:
                raise
        

    hass.services.register(DOMAIN, "update_json", state_into_json)

    # Return boolean to indicate that initialization was successful.
    return True
