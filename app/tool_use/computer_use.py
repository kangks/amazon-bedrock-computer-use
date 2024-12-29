from io import BytesIO
import logging
from botocore.exceptions import ClientError
from botocore.config import Config
from time import sleep
from datetime import datetime

import sys
import subprocess

from pprint import pformat
import Xlib.display
import pyautogui
import os
import sys
if(os.environ.get('DISPLAY')):
    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ.get('DISPLAY'))

class SaveScreenshot:
    def __init__(self):
        self.image_location = os.environ.get("LOG_OUTPUT_FOLDER", os.path.dirname(__file__) + "/logs")
        self.counter=0
        self.logger = logging.getLogger(__name__)
    
    def get_and_save_screen_shot(self):
        screenshot = pyautogui.screenshot()
        buffer = BytesIO()
        screenshot.save(buffer, format='PNG')
        screenshot_filename=f"{self.image_location}/screen_shot_{self.counter}.png"
        self.counter+=1
        self.logger.debug(f"saving screenshot to {screenshot_filename}")
        screenshot.save(screenshot_filename, format='PNG')
        image_bytes = buffer.getvalue()
        buffer.close()
        return image_bytes
    
class ComputerUse:
    def __init__(self):
        self.screenshot = SaveScreenshot()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("ComputerUse initialized")

    def execute_tool_command(self, command, input_data, tool_use_id):
        self.logger.debug(f"Executing tool commnd: {command} for tool_use_id: {tool_use_id}")

        self.logger.debug(f"command:{command}, input_data:{input_data}")
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        self.logger.debug(f"result:{result}")
        response={
            'toolResult': {
                'toolUseId': tool_use_id,
                'content':[
                    {
                        'text': {result}
                    }
                ]
            }
        }                

        return response 

    def execute_tool_action(self, action, input_data, tool_use_id):
        """Simulate executing a tool action from Bedrock."""
        # Placeholder logic for tool execution
        # Replace with actual tool execution logic
        # response = {}
        self.logger.debug(f"Executing tool action: {action} for tool_use_id: {tool_use_id}")
        match action:
            case 'screenshot':
                self.logger.debug(f"screenshot, input_data:{input_data}")
                response={
                    'toolResult': {
                        'toolUseId': tool_use_id,
                        'content':[
                            {
                                'text': 'OK'
                            },
                            {
                                'image': {
                                    'format': 'png',    
                                    'source': {
                                        'bytes': self.screenshot.get_and_save_screen_shot()
                                    }
                                }
                            }                            
                        ],
                        'status':'success'
                    }
                }                
            case 'type':
                text = input_data.get('text')
                self.logger.debug(f"type:{text}, input_data:{input_data}")
                pyautogui.write(input_data.get('text'))
                response={
                    'toolResult': {
                        'toolUseId': tool_use_id,
                        'content':[
                            {
                                'text': 'OK'
                            }
                        ]
                    }
                }                
            case 'key':
                key = input_data.get('text')
                self.logger.debug(f"key:{key}, input_data:{input_data}")
                if key.lower() == 'return':
                    key = 'enter'
                    pyautogui.press(key)
                elif '_' in key: # for example page_down
                    key = key.replace("_","").lower()
                    pyautogui.press(key)
                elif '+' in key:
                    keys = key.split('+')
                    self.logger.debug(f"keys:{keys}, using pyautogui.hotkey()")
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(input_data.get('text'))

                response={
                    'toolResult': {
                        'toolUseId': tool_use_id,
                        'content':[
                            {
                                'text': 'OK'
                            }
                        ]
                    }
                }                
            case 'left_click' | 'right_click':
                self.logger.debug(f"mouse click, input_data:{input_data}")
                pyautogui.click(button=f'{action.replace("_click","")}')
                sleep(0.25)
                response={
                    'toolResult': {
                        'toolUseId': tool_use_id,
                        'content':[
                            {
                                'text': 'OK'
                            }
                        ]
                    }
                }                
            case 'mouse_move':
                coordinate = input_data['coordinate']
                self.logger.debug(f"coordinate: {coordinate}, input_data:{input_data}")
                # coord_str = coordinate.strip('[]')
                # x, y = map(int, coord_str.split(','))
                pyautogui.moveTo(coordinate[0],coordinate[1])
                response={
                    'toolResult': {
                        'toolUseId': tool_use_id,
                        'content':[
                            {
                                'text': 'OK'
                            }
                        ]
                    }
                }                
            case _:
                self.logger.exception("Unsupported action received")
                raise ValueError(f"Unsupported action received: {action}")

        _ = self.screenshot.get_and_save_screen_shot()
        return response 

    def handle(self, toolUse):
        input_data = toolUse['input']
        tool_use_id = toolUse['toolUseId']
        if(input_data.get('action')):
            action = input_data.get('action')
            self.logger.debug(f'action:{action}')
            tool_result = self.execute_tool_action(action, input_data, tool_use_id)
            return tool_result
        elif(input_data.get('command')):
            command = input_data.get('command')
            self.logger.debug(f'command:{command}')
            tool_result = self.execute_tool_command(command, input_data, tool_use_id)
            return tool_result
        # elif(input_data.get('type')):
        #     input_data_type = input_data.get('type')
        #     if isinstance(input_data_type, dict):
        #         command = input_data_type.get('command')
        #     else:
        #         command = input_data_type
        #     logger.info(f'command:{command}')
        #     tool_result = self.execute_tool_command(command, input_data, tool_use_id)
        #     tool_result_contents.append(tool_result)
        else:            
            self.logger.exception(f"Unknown input: {input_data}")
            raise ValueError(f"Unknown input: {input_data}")
