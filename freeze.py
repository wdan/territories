from flask_frozen import Freezer
from territories import territories

freezer = Freezer(territories)

if __name__ == '__main__':
    freezer.freeze()
