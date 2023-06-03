from setuptools import setup, Extension

def main():
    setup(
        name="pylibfinder",
        version="0.1.0",
        description="Library to spot a keyword as a function inside python stdlib",
        author="Prince Roshan",
        author_email="princekrroshan01@gmail.com",
        ext_modules=[Extension("funcfinder", ["funcfinder.c"])],
        keywords=[
            "C-extension"
        ],
        python_requires=">=3.10",
        classifiers=[
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX",
        ],
    )

if __name__ == "__main__":
    main()