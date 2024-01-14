### Installation Process

* Make a virtual environment and activate that
* install all packages in the `requirements.txt`.
* run `nohup python3 main.py > output.log 2>&1 &`. It will start main.py in the background and log everything in `output.log`.
* If you wanna stop the background process, run `ps aux | grep main.py` and find the one that's running `main.py`. It will have a `PID` associated with it, just run `kill <PID>` and the background process will be destroyed.

More details about the actual bot will be added later.