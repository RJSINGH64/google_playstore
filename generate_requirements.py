# generate_requirements.py
import subprocess

def generate_requirements():
    with open('requirements.txt', 'w') as f:
        subprocess.run(['pip', 'freeze'], stdout=f)

if __name__ == '__main__':
    generate_requirements()
