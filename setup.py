from distutils.core import setup, Extension

def main():
    setup(name="spotter",
          version="1.0.0",
          description="Python interface for the fputs C library function",
          author="Prince Roshan",
          author_email="princekrroshan01@gmail.com",
          ext_modules=[Extension("spotter", ["spotter.c"])])

if __name__ == "__main__":
    main()
