##
# Created by: Curtis Szmania
# Date: 5/31/2017
# Initial Creation.
###

from logging import getLogger
from numpy import array, load, savez_compressed
from os import chdir, kill, listdir, path
from re import split, sub
from signal import SIGTERM
from subprocess import call, PIPE, Popen

__author__ = 'szmania'

SCRIPT_DIR = path.dirname(path.realpath(__file__))

class Lib(object):
    def __init__(self, logLevel='DEBUG'):
        """
        MegaManager library.

        Args:
            logLevel (str): Logging level setting ie: "DEBUG" or "WARN"
        """

        self.__logLevel = logLevel

    def dump_list_into_file(self, itemList, filePath):
        """
        Dump list into file for each item on a new line.
    
        :param itemList: List to dump into file.
        :type itemList: list
        :param filePath: File to dump to.
        :type filePath: string
    
        :return: boolean of whether successful or not
        """
    
        logger = getLogger('MegaManager_lib.dump_list_into_file')
        logger.setLevel(self.__logLevel)
    
        logger.debug(' Dumping list into %s filePath.' % filePath)

        try:
            npList = array(itemList)
            savez_compressed(filePath, list=npList)
        except Exception as e:
            logger.debug(' Exception: %s' % str(e))
    
    def exec_cmd(self, command, workingDir=None, noWindow=False, outputFile=None):
        """
        Execute given command.

        Args:
            command (str): Command to execute.
            workingDir (str): Working directory.
            noWindow (bool): No window will be created if true.
            outputFile (str): file path to output program output to.
    
        Returns:
            subprocess object
        """
    
        logger = getLogger('Lib.exec_cmd')
        logger.setLevel(self.__logLevel)
    
        logger.debug(' Executing command: "%s"' % command)

        outFile = open(outputFile, 'a')

        if workingDir:
            chdir(workingDir)

        if noWindow:
            CREATE_NO_WINDOW = 0x08000000
            proc = call(command, stdout=outFile, stderr=outFile, creationflags=CREATE_NO_WINDOW)
        else:
            proc = call(command)
    
        while not proc.poll():
            pass

        outFile.close()
        exitCode = proc.returnCode()

        if exitCode == 0:
            logger.debug(' Successfully executed command "%s".' % command)
            return True
        else:
            logger.debug(' Error when running command "%s".' % command)
            return False

    def exec_cmd_and_return_output(self, command, workingDir=None, outputFile=None):
        """
        Execute given command and return stdout and stderr.

        Args:
            command (str): Command to execute.
            workingDir (str): Working directory.
            outputFile (str): File to pipe process output to.

        Returns:
            Tuple: of stdout and stderr.
        """

        logger = getLogger('MegaTools_Lib.exec_cmd_and_return_output')
        logger.setLevel(self.__logLevel)

        logger.debug(' Executing command: "%s"' % command)

        if workingDir:
            chdir(workingDir)

        outFile = open(outputFile, 'a')
        try:
            if outFile:
                proc = Popen(command, stdout=outputFile, stderr=outFile)
            else:
                proc = Popen(command, stdout=PIPE, shell=True)

            (out, err) = proc.communicate()
        except Exception as e:
            logger.warning(' Exception: %s' % str(e))
            return None, None
        finally:
            outFile.close()

        return out, err

    def get_mb_size_from_bytes(self, bytes):
        """
        Convert bytes to size in MegaBytes.

        Args:
            bytes (int): Size in bytes.

        Returns:
            string: Size in MegaBytes converted from bytes.
        """
    
        logger = getLogger('Lib.get_mb_size_from_bytes')
        logger.setLevel(self.__logLevel)
    
        logger.debug(' Converting kilobytes to megabytes.')
    
        result = ''
        if bytes < 1000:
            result = '%i' % bytes + 'B'
        elif 1000 <= bytes < 1000000:
            result = '%.1f' % float(bytes / 1000) + 'KB'
        elif 1000000 <= bytes < 1000000000:
            result = '%.1f' % float(bytes / 1000000) + 'MB'
        elif 1000000000 <= bytes < 1000000000000:
            result = '%.1f' % float(bytes / 1000000000) + 'GB'
        elif 1000000000000 <= bytes:
            result = '%.1f' % float(bytes / 1000000000000) + 'TB'
    
        return result

    def get_remote_path_from_local_path(self, localPath, localRoot="\\", remoteRoot="\\"):
        """
        Get remote path given local path.

        Args:
            localPath (str): Local path.
            localRoot (str): Local root
            remoteRoot (str): Remote root.
        Returns:
            string: Remote path.
        """

        logger = getLogger('Lib.get_remote_path_from_local_path')
        logger.setLevel(self.__logLevel)

        logger.debug(' Getting remote path from local path')

        localRoot_adj = sub('\\\\', '/', localRoot)
        localFilePath_adj = sub('\\\\', '/', localPath)
        postfix = split(localRoot_adj, localFilePath_adj)

        if len(postfix) > 1:
            subPath = postfix[1]

            logger.debug(' Success, could get remote path from local path.')
            return remoteRoot + subPath
        else:
            logger.debug(' Error, could NOT get remote path from local path!')
            return None

    def get_sleep_time(self):
            """
            Get time in seconds to sleep. Function is used to pace program speed during iterations.
    
            :return: Time in seconds to sleep as integer.
            """
    
            logger = getLogger('megaManager_lib.get_sleep_time')
            logger.setLevel(self.__logLevel)
    
            sleepTime = 0
    
            return sleepTime

    def get_items_in_list_with_subString(self, list, subString):
        """
        Return sub list of list that contain substring.

        :param list: List to find substrings in.
        :type list: List.
        :param subString: Substring to find.
        :type subString: String.

        :return: List of items that contain subString.
        """

        logger = getLogger('Lib.get_items_in_list_with_subString')
        logger.setLevel(self.__logLevel)

        subList = []
        for item in list:
            if subString in item:
                subList.append(item)
        return subList

    def kill_running_processes_with_name(self, procName):
        """
        Kill processes with name.
    
        :param procName: Process name.
        :type procName: String.
    
        :return:
        """
    
        logger = getLogger('megaManager_lib.kill_running_processes_with_name')
        logger.setLevel(self.__logLevel)
    
        logger.info(' Killing processes with name "%s"' % procName)
        # p = Popen(['ps', '-a'], stdout=PIPE)
        p = Popen(['tasklist', '/v'], stdout=PIPE)
        out, err = p.communicate()
    
        for line in out.splitlines():
            if line.startswith(procName):
                pid = int(line.split()[1])
                kill(pid, SIGTERM)
    
        logger.debug(' Success, all "%s" process have been killed.' % procName)

    def load_file_as_list(self, filePath):
        """
        Load file as list splitting each line into a new item.

        :param filePath: File to lead.
        :type filePath: String.

        :return: Lines in file as list.
        """

        logger = getLogger('Lib.load_file_list_as_list')
        logger.setLevel(self.__logLevel)

        logger.debug(' Loading %s filePath.' % filePath)

        items = []
        if path.isfile(filePath):
            try:
                data = load(file=filePath, allow_pickle=False)
                items = data.f.list.tolist()

            except Exception as e:
                logger.debug(' Exception: %s' % str(e))
            finally:
                return items

        else:
            logger.debug(' Error, filepath "%s" does NOT exist!' % filePath)
            return items

    def size_of_dir(self, dirPath):
        """
        Walks through the directory, getting the cumulative size of the directory
    
        :param dirPath: Directory to walk through to get size.
        :type dirPath: String.
    
        :return: Size in bytes as integer.
        """
    
        logger = getLogger('megaManager_lib.size_of_dir')
        logger.setLevel(self.__logLevel)
    
        logger.debug(' Getting size of directory "%s"' % dirPath)
    
        sum = 0
        for file in listdir(dirPath):
            sum += path.getsize(dirPath + '\\' + file)
        return sum
    

