import subprocess
import sys
import sysconfig
import random,time

# 获取当前解释器路径（就是 PyCharm 正在使用的那个）
python_exe = sys.executable
#
subprocess.run([python_exe, "for_cookie.py"])
duration = random.uniform(1.0, 5.5)
time.sleep(duration)
# input('杀戮中绽放,黎明时的花朵')
# #
subprocess.run([python_exe, "search.py"])
# # # duration = random.uniform(1.0, 5.5)
# time.sleep(duration)
# input('澜只是代号')

subprocess.run([python_exe, "reward.py"])