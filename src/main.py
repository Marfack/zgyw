from multiprocessing import Process, Queue, freeze_support
import os
import sys
import time
from ui.ui_app import ui_process
from service.service import doService

process = list[Process]()
data = list[list[str]]()
id_set = set[str]()
to_ui_q = Queue(10)
to_pt_q = Queue(10)
ui = Process(target=ui_process, args=(to_ui_q, to_pt_q))

def exit_handler():
    if ui.is_alive():
        ui.terminate()
    for p in process:
        if p.is_alive():
            p.terminate()
    try:
        with open('resources/data/data.csv', 'w', encoding='utf8') as f:
            f.write('id,账号,密码,总计时长\n')
            for d in data:
                if d[0] in id_set:
                    f.write(','.join(d) + '\n')
    except:
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    freeze_support()
    os.chdir(os.path.dirname(__file__))
    ui.start()
    try:
        with open('resources/data/data.csv', 'r', encoding='utf8') as f:
            for line in f:
                d = line.strip().split(',')
                if d[-1] == '总计时长' or d[0] in id_set:
                    continue
                data.append(d)
                id_set.add(d[0])
                p = Process(target=doService, args=(d[0], d[1], d[2], to_ui_q, len(process)))
                process.append(p)
                p.start()
    except:
        exit_handler()
    while ui.is_alive():
        time.sleep(1)
        if not to_pt_q.empty():
            arg = to_pt_q.get()
            if arg[0] == 1:
                if arg[1] not in id_set:
                    id_set.add(arg[1])
                    p = Process(target=doService, args=(arg[1], arg[2], arg[3], to_ui_q, len(process)))
                    process.append(p)
                    data.append([arg[1], arg[2], arg[3], 'N/A'])
                    p.start()
            elif arg[0] == 0:
                if process[arg[1]].is_alive():
                    process[arg[1]].terminate()
                    data[arg[1]][3] = arg[2]
            else:
                id_set.remove(data[arg[1]][0])
                if process[arg[1]].is_alive():
                    process[arg[1]].terminate()
    exit_handler()