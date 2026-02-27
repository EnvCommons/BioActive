from openreward.environments import Server

from bioactive import Bioactive

if __name__ == "__main__":
    server = Server([Bioactive])
    server.run()
