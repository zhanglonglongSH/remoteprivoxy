import os
import shutil
import subprocess

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="fastvpn")

def ping(host,port,auth):
  ret = subprocess.run(
    ['curl', '-x', f'{auth}@{host}:{port}', 'https://ipinfo.io'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
  )
  return ret.returncode == 0

def write_config(appendinfo):
  wpath = os.getcwd()
  config_file = f'{wpath}/privoxy_config'
  source = f'{wpath}/privoxy_config_example'
  shutil.copy(source, config_file)
  with open(config_file,"a") as variable_name:
    variable_name.write(appendinfo)



@app.get("/hostapi")
async def say_hello(host: str,port:str,auth:str):
  is_connect = ping(host,port,auth);
  if is_connect:
    write_config(f"forward-socks5   /               {auth}@{host}:{port}  .")
    # 重启
    path = os.getcwd()
    kill_status = os.system(" ps -ef|grep privoxy| grep -v grep |awk '{print $2}' |xargs kill -9 ")
    start_privoxy= os.system(f"/usr/sbin/privoxy  {path}/privoxy_config")
    # start_privoxy= os.system(f"/usr/local/sbin/privoxy  {path}/privoxy_config")
    return  ping(host);
  else:
    return is_connect;


if __name__ == '__main__':
  """
  """
  uvicorn.run(app='main:app',host="0.0.0.0",port=8090,reload=True)
