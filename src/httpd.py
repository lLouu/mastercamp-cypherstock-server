

def __main__(*argv):
    from serve.lib import Runner
    Runner(80).launch()

if __name__ == "__main__":
    from sys import argv
    __main__(argv)