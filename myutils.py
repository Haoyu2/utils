import logging, time, os, functools, threading, yaml, multiprocessing, pickle

projectLogger = logging.getLogger('project_logger')
projectLogger.setLevel(logging.DEBUG)
if not os.path.exists('log'): os.mkdir('log')
file_handler = logging.FileHandler(os.path.join('log', 'project.log'))
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(module)s - %(lineno)d - %(threadName)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

projectLogger.addHandler(file_handler)
projectLogger.addHandler(stream_handler)


def project_logger(func):
    @functools.wraps(func)  # keep original func info instead wrapper func info
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time() - t1
        # mesg = f'{func.__name__} ran in {t2} sec(s) with {args} and {kwargs}'
        # threading.Thread(target=projectLogger.debug, args=mesg)
        projectLogger.debug(f'{func.__name__} ran in {t2} sec(s) with {args} and {kwargs}')
        # projectLogger.debug(mesg)
        return result

    return wrapper


def along_thread(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()

    return wrapper

def along_process(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        multiprocessing.Process(target=func, args=args, kwargs=kwargs).start()

    return wrapper


@along_thread
def dump2yaml(obj, file_path):
    with open(file_path, 'w') as f:
        yaml.dump(obj, f)
    projectLogger.info(f'a {type(obj)} has been dumped into {file_path}')

@along_thread
def dump2pickle(obj, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)
    projectLogger.info(f'a {type(obj)} has been dumped into {file_path}')
if __name__ == '__main__':
    a = [1, 2, 3]
    file = 'persistence/a.yml'
    dump2yaml(a, file)
    file1 = 'persistence/a.pkl'

    dump2pickle(a, file1)

    @project_logger
    def test(name, age=10):
        time.sleep(1)
        print(f'name:{name}, age:{age}')

    @project_logger
    def test(name, age=10):
        time.sleep(1)
        print(f'name:{name}, age:{age}')

    print(__name__)
    test('yes', age=12)


