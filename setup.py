from setuptools import setup, find_packages

setup(
    name='console-animation',
    version='0.1.1',
    description='An easy to use decorator to show a console spinner during function execution.',
    author='Koushik',
    author_email='koushikla115@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
