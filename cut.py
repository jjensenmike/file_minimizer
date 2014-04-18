import subprocess
pipe = subprocess.Popen(['cut', '-f', '1,22,26-29,76-84,86', '<file_name>'], stdout=subprocess.PIPE)
with open('<output_file>', 'w') as f:
    f.writelines(pipe.stdout)
