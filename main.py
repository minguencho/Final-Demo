import subprocess

fastapi_process = subprocess.Popen(['python', '-m','uvicorn', 'app:app', '--reload', '--host=0.0.0.0', '--port=8888'])
mongo_process = subprocess.Popen(['python', 'result.py'])


fastapi_process.wait()
mongo_process.wait()

