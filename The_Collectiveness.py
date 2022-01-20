import multiprocessing
from Hive import Bee, output_path

AMOUNT = 10**9
PRECISION = 2
THREADS = 16


try:
    with open(output_path, "r") as f:
        AMOUNT -= f.read().count(":")
except: pass


def progress_bar(progress, bar_length = 20):
    arrow   = "-" * int(progress/100 * bar_length - 1) + '>'
    spaces  = " " * (bar_length - len(arrow))
    percent = ("{:."+str(PRECISION)+"f}").format(progress)
    print(f"Progress: [{arrow}{spaces}] {percent} %", end='\r')

finished = 0


def send_unit(from_f, to_f, index):
    global finished
    last_progress = -1
    report = ""
    for i in range(int(AMOUNT*from_f), int(AMOUNT*to_f)):
        bee = Bee()
        report += bee.explore()
        #if index != finished: continue
        progress = abs(round(
            (i / AMOUNT - from_f)
            / (to_f - from_f)
            * 100
        ,PRECISION))
        if progress > last_progress:
            last_progress = progress
            progress_bar(progress)
            with open(output_path, "a") as f:
                f.write(report)
            report = ""
    with open(output_path, "a") as f:
        f.write(report)
    print(f"Thread {index} finished")
    finished += 1


if __name__ == '__main__':
    processes = []
    for i in range(THREADS):
        p = multiprocessing.Process(target=send_unit, args=(i/THREADS,(i+1)/THREADS,i))
        processes.append(p)
        p.start()
        
    for process in processes:
        process.join()
    
    print("Done")









