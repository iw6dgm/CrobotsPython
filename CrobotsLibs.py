import imp
import os
import re
import subprocess

config = {
    'user': 'crobots',
    'passwd': '',
    'host': '127.0.0.1',
    'db': 'crobots',
    'compress': True,
}

DATABASE_ENABLE = os.environ.has_key("CROBOTS_MYSQL")

if DATABASE_ENABLE:
    import MySQLdb as mysql

    print "MySQL database enabled"

P_SETUPUP = "call pSetupResults%s()"
P_CLEANUP = "TRUNCATE TABLE results_%s"
UPDATE_SQL = "UPDATE results_%s SET games=%s, wins=%s, ties=%s, points=%s WHERE robot='%s'"

cnx = None


def check_stop_file_exist():
    """check the stop file existance"""
    if os.path.exists('Crobots.stop'):
        return True
    return False


def clean_up_log_file(filepath):
    """remove log file"""
    try:
        os.remove(filepath)
    except:
        pass


def load_from_file(filepath):
    """Load configuration py file with tournament parameters"""
    class_inst = None
    expected_class = 'Configuration'

    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)
    elif file_ext.lower() == '.pyc' or file_ext.lower() == '.pyo':
        py_mod = imp.load_compiled(mod_name, filepath)
    else:
        return class_inst

    if hasattr(py_mod, expected_class):
        class_inst = py_mod.Configuration()

    return class_inst


def test_connection():
    global DATABASE_ENABLE, config, cnx
    if DATABASE_ENABLE:
        try:
            mysql.threadsafety = 0
            cnx = mysql.connect(**config)
        except mysql.Error as err:
            print "A database error has occurred: switching remote database enabled to False..."
            DATABASE_ENABLE = False
            print(err)
        else:
            print "Database Connection OK"


def update_results(ptype, robot, games, win, tie, points):
    global cnx, DATABASE_ENABLE
    try:
        cursor = cnx.cursor()
        cursor.execute(UPDATE_SQL % (ptype, games, win, tie, points, robot))
        cnx.commit()
        cursor.close()
    except mysql.Error as err:
        print "A database error has occurred: switching remote database enabled to False..."
        close_connection()
        DATABASE_ENABLE = False
        print(err)


def close_connection():
    global DATABASE_ENABLE, cnx
    if DATABASE_ENABLE and None != cnx:
        try:
            print "Closing remote database connection..."
            cnx.close()
        except mysql.Error as err:
            print "A database error has occurred on closing connection..."
            print(err)
        finally:
            cnx = None


def set_up(ptype):
    global DATABASE_ENABLE
    if DATABASE_ENABLE:
        try:
            print("Set up remote database for %s" % ptype.upper())
            cnx = mysql.connect(**config)
            cursor = cnx.cursor()
            cursor.execute(P_SETUPUP % ptype.upper())
            cnx.commit()
            cursor.close()
            cnx.close()
        except mysql.Error as err:
            print "A database error has occurred: switching remote database enabled to False..."
            DATABASE_ENABLE = False
            print(err)


def clean_up(ptype):
    global DATABASE_ENABLE
    if DATABASE_ENABLE:
        try:
            print("Clean up remote database for %s" % ptype.upper())
            cnx = mysql.connect(**config)
            cursor = cnx.cursor()
            cursor.execute(P_CLEANUP % ptype)
            # cnx.commit()
            cursor.close()
            cnx.close()
        except mysql.Error as err:
            print "A database error has occurred: switching remote database enabled to False..."
            DATABASE_ENABLE = False
            print(err)


def available_cpu_count():
    """ Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    # try:
    # m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
    # open('/proc/self/status').read())
    #     if m:
    #         res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
    #         if res > 0:
    #             return res
    # except IOError:
    #     pass

    # Python 2.6+
    try:
        import multiprocessing

        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # http://code.google.com/p/psutil/
    try:
        import psutil

        return psutil.cpu_count()  # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

    # POSIX
    try:
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ['NUMBER_OF_PROCESSORS'])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime

        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                  stdout=subprocess.PIPE)
        scStdout = sysctl.communicate()[0]
        res = int(scStdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open('/proc/cpuinfo').read().count('processor\t:')

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudoDevices = os.listdir('/devices/pseudo/')
        res = 0
        for pd in pseudoDevices:
            if re.match(r'^cpuid@[0-9]+$', pd):
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open('/var/run/dmesg.boot').read()
        except IOError:
            dmesgProcess = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
            dmesg = dmesgProcess.communicate()[0]

        res = 0
        while '\ncpu' + str(res) + ':' in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception('Can not determine number of CPUs on this system')
