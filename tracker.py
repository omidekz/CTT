import pickle
import os.path

from arger import parser
from argshandler import CustomHandler
import core
from filer import Manager

if __name__ == '__main__':
    if not os.path.exists('./settings.d'):
        file = open('./settings.d', 'wb')
        pickle.dump({"db": "main.d"}, file)
        file.close()

    file = open('settings.d', 'rb')
    settings = pickle.load(file)
    file.close()
    args = parser.parse_args()
    if args.db:
        file = open('./settings.d', 'wb')
        settings['db'] = args.db
        pickle.dump(settings)
    else:
        args.db = settings['db']

    core.Tracker(Manager(args.db), CustomHandler(args)).done()
