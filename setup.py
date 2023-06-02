from distutils.core import setup, Extension

def main():
    setup(name="spotter",
          version="1.0.0",
          description="Library to spot a keyword as a function inside python stdlib",
          author="Prince Roshan",
          author_email="princekrroshan01@gmail.com",
          ext_modules=[Extension("spotter", ["spotter.c"])])

if __name__ == "__main__":
    main()
