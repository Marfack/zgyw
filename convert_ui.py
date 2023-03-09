import os

os.chdir(os.getcwd())

PREFIX = 'resources/'

def convert(path):
    if os.path.exists(PREFIX + path):
        if os.path.isfile(PREFIX + path):
            if not os.path.exists(f'src/{path.split(".")[0]}.py'):
                os.system(f'pyuic6 -o src/{path.split(".")[0]}.py {PREFIX + path}')
                print(f'convert {PREFIX + path} to src/{path}')
        else:
            for f in os.listdir(PREFIX + path):
                convert(f'{path}/{f}')

convert('ui')