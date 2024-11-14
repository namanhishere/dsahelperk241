import os
import sys
import subprocess
import time
import threading
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

args = [
    "-std=c++17",
    "-pthread",
    "-Iinclude",
    "-Iinclude/ann",
    "-Iinclude/sformat",
    "-Iinclude/demo",
    "-Iinclude/tensor",
]

args_str = " ".join(args)

compile_threads = {}
process_lock = threading.Lock()


def findAllfile():
    files = []
    for root, _, filenames in os.walk("./src"):
        for filename in filenames:
            if filename.endswith(".cpp"):
                files.append(os.path.join(root, filename))
    return files


def run_command(command, key):
    global compile_threads
    with process_lock:
        # Terminate any ongoing command for this key
        if key in compile_threads and compile_threads[key].poll() is None:
            print(f"[HELPER] Terminating ongoing process for {key}")
            compile_threads[key].terminate()
            compile_threads[key].wait()

        # Start new process
        compile_threads[key] = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    # Capture output asynchronously
    stdout, stderr = compile_threads[key].communicate()
    if compile_threads[key].returncode != 0:
        if stderr.decode() != "":
            print(f"Error executing {key}: {stderr.decode()}", file=sys.stderr)
        return None
    return stdout.decode()


def compile_file(file):
    obj_file = file.replace("./src", "./obj").replace(".cpp", ".o")
    os.makedirs(os.path.dirname(obj_file), exist_ok=True)
    command = f"g++ {args_str} -c {file} -o {obj_file}"
    print(f"[HELPER] Compiling: {file}")
    run_command(command, key=file)


def compile_main():
    obj_files = ' '.join([x.replace('./src', './obj').replace('.cpp', '.o') for x in cpp_files])
    compile_command = f"g++ {args_str} {obj_files} -o run"
    print("[HELPER] Linking all files to create executable")
    run_command(compile_command, key="link")

    # Run the executable
    print("[HELPER] Running executable")
    threading.Thread(target=run_command, args=("./run > outtest.txt", "run")).start()


def handle_file_change(filePath):
    #terminate all ongoing processes
    with process_lock:
        for key in list(compile_threads.keys()):
            if key in compile_threads and compile_threads[key].poll() is None:
                print(f"[HELPER] Terminating ongoing process for {key}")
                compile_threads[key].send_signal(signal.SIGKILL)
                compile_threads[key].wait()
        compile_threads.clear()  
    # proceed with new compilation
    if filePath in cpp_files:
        os.system("echo > outtest.txt")
        compile_file(filePath)
        compile_main()

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super(MyHandler, self).__init__()
        self.last_modified = {}
        self.cooldown = 1.0  # Cooldown period in seconds
        self.lock = threading.Lock()

    def on_modified(self, event):
        if event.is_directory:
            return
        
        if not event.src_path.endswith('.cpp'):
            return

        with self.lock:
            current_time = time.time()
            file_path = event.src_path

            # Check if the file has been modified recently
            if file_path in self.last_modified:
                if current_time - self.last_modified[file_path] < self.cooldown:
                    return

            # Update the last modified time for the file
            self.last_modified[file_path] = current_time
            
            # Terminate all processes before starting new ones
            threading.Timer(0.1, handle_file_change, args=(file_path,)).start()
cpp_files = findAllfile()

if __name__ == "__main__":
    path = "./"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            command = input() #stop commands currently not working - require exit
            # if command == "s":
            #     # Stop all commands
            #     for key in compile_threads.keys():
            #         print(f"[HELPER] Terminating ongoing process for {key}")
            #         compile_threads[key].terminate()
            #         compile_threads[key].wait()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
