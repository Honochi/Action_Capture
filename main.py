from pynput import mouse, keyboard
from time import time, sleep
import threading
import json
import os
import cmd

# 全局变量
events = []
start_time = None
mouse_listener = None
keyboard_listener = None
recording = False
path = './commands.json'

def on_move(x, y):
    current_time = time() - start_time
    events.append({'time': current_time, 'type': 'mouse_move', 'x': x, 'y': y})
def on_click(x, y, button, pressed):
    current_time = time() - start_time
    action = 'press' if pressed else 'release'
    events.append({
        'time': current_time,
        'type': 'mouse_click',
        'x': x,
        'y': y,
        'button': button.name,
        'action': action
    })
def on_scroll(x, y, dx, dy):
    current_time = time() - start_time
    events.append({
        'time': current_time,
        'type': 'mouse_scroll',
        'x': x,
        'y': y,
        'dx': dx,
        'dy': dy
    })
# 键盘事件处理
def on_press(key):
    current_time = time() - start_time
    try:
        key_name = key.name
    except AttributeError:
        if key.char is not None:
            key_name = key.char
        else:
            key_name = f'vkc_{key.vk}'
    events.append({
        'time': current_time,
        'type': 'keyboard',
        'action': 'press',
        'key': key_name
    })
def on_release(key):
    current_time = time() - start_time
    try:
        key_name = key.name
    except AttributeError:
        if key.char is not None:
            key_name = key.char
        else:
            key_name = f'vkc_{key.vk}'
    events.append({
        'time': current_time,
        'type': 'keyboard',
        'action': 'release',
        'key': key_name
    })
    if key == keyboard.Key.esc:
        return False  # 停止键盘监听器
# 开始录制
def start_recording():
    global start_time,events,recording
    events = []
    start_time = time()
    recording = True

    # 启动鼠标监听器
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )
    mouse_listener.start()

    # 启动键盘监听器
    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    keyboard_listener.start()

    print("Recording started. Press Esc to stop.")
    keyboard_listener.join()  # 等待键盘监听器停止
    mouse_listener.stop()     # 停止鼠标监听器
    recording = False

    # 按时间排序事件
    events.sort(key=lambda x: x['time'])
    print(f"Recording stopped. Captured {len(events)} events.")
    with open(path,'w') as file:
        file.write(json.dumps(events))
# 回放事件
def replay(path):
    with open(path,'r') as file:
        events = json.loads(file.read())
    mouse_ctrl = mouse.Controller()
    keyboard_ctrl = keyboard.Controller()
    start_play_time = time()
    print("Replaying...")
    for event in events:
        # 等待到事件发生的时间
        while time() - start_play_time < event['time']:
            sleep(0.001)

        # 处理鼠标移动
        if event['type'] == 'mouse_move':
            mouse_ctrl.position = (event['x'], event['y'])

        # 处理鼠标点击
        elif event['type'] == 'mouse_click':
            button = getattr(mouse.Button, event['button'])
            if event['action'] == 'press':
                mouse_ctrl.press(button)
            else:
                mouse_ctrl.release(button)

        # 处理鼠标滚轮
        elif event['type'] == 'mouse_scroll':
            mouse_ctrl.scroll(event['dx'], event['dy'])

        # 处理键盘事件
        elif event['type'] == 'keyboard':
            key_info = event['key']
            try:
                # 尝试解析为特殊按键（如ctrl）
                key = getattr(keyboard.Key, key_info)
            except AttributeError:
                # 解析为虚拟键码或普通字符
                if key_info.startswith('vkc_'):
                    vk_code = int(key_info.split('_')[1])
                    key = keyboard.KeyCode.from_vk(vk_code)
                else:
                    try:
                        key = keyboard.KeyCode.from_char(key_info)
                    except:
                        print(f"无法解析按键: {key_info}")
                        continue
            # 执行按键动作
            if event['action'] == 'press':
                keyboard_ctrl.press(key)
            else:
                keyboard_ctrl.release(key)

    print("Replay completed.")

class ActionCapture(cmd.Cmd):
    prompt = '>> '
    intro = "欢迎使用动作录制回放系统！\n输入 help 查看可用命令"

    def do_record(self, arg):
        """开始录制鼠标和键盘操作"""
        global recording
        if recording:
            print("当前已在录制中！")
            return
        
        print("即将开始录制，按ESC键停止...")
        threading.Thread(target=start_recording).start()

    def do_replay(self, arg):
        """回放录制的操作\n用法: replay 文件名"""
        if not arg:
            print("请指定要回放的JSON文件！")
            return
            
        if not os.path.exists(arg):
            print(f"文件 {arg} 不存在！")
            return
            
        print(f"开始回放 {arg}...")
        threading.Thread(target=replay, args=(arg,)).start()

    def do_list(self, arg):
        """列出当前目录的录制文件"""
        files = [f for f in os.listdir('.') if f.endswith('.json')]
        print("找到的录制文件：")
        for f in files:
            print(f"  - {f}")

    def do_exit(self, arg):
        """退出程序"""
        print("感谢使用！")
        return True

if __name__ == "__main__":
    ActionCapture().cmdloop()
