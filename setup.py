## contain generic info about user, and used while creating packages

'''
This is essential part for packaging and distributing 
python project. It is used by setuptools (distutils in older python version)
to define the congifuration of your projects, such as its metadata 
,dependencies and more
'''

## this finpackages , scan all folder and where it find __init__.py , it will consider it as an packages
from setuptools import find_packages,setup
from typing import List


def get_requirenments()->List[str]:
    '''
    this fn will return list of requirements
    '''
    requirement_lst:List[str]=[]

    try:
        with open('requirements.txt','r') as file:
            #read lines from file
            lines=file.readlines()
            #process each line
            for line in lines:
                requirement=line.strip()  ## ignore any empty spaces and -e .
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt nor found")

    return requirement_lst

setup(
    name="Network_Security",
    version="0.0.0.1",
    author="Vivek Chouhan",
    author_email="vivekchouhan2512@gmail.com",
    packages=find_packages(),
    install_requires=get_requirenments()  ##when packeage build , it install all library
)
