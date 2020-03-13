import os
import xml.dom.minidom
from lxml import etree
# import xlsxwriter

# Set these according to project
MTX_FILE_DIR = 'mtx_files'
# EXT_INTERFACE_FILE_DIR = ''
TYPES_MTX = 'types.mtx'

# Set these as convenience
XLS_FILENAME = 'interface_report'
OUTPUT_FILENAME = 'results.txt'

# Globals
OUT_INFO = 1
OUT_ERR = -1

output_string = []


def load_all_SA_mtx_files():
    """
    This method shall return a list with all *.mtx files found.
    :return: list()
    """
    _list = []
    for file in os.listdir(MTX_FILE_DIR):
        if file.endswith(".mtx"):
            # print(os.path.join(MTX_FILE_DIR, file))
            if '_SA' in file:
                _list.append(os.path.join(MTX_FILE_DIR, file))
    return _list


def check_not_connected_signals(filename):

    NOT_CONNECTED = "NOT_CONNECTED"

    _f_has_nc_signals = False

    out_file_lines = []

    _safe_signal_list = []
    _doc = xml.dom.minidom.parse(filename)

    _safe_signal_list = _doc.getElementsByTagName('safe-signal')

    # _str = ' -- Processing file: ' + filename
    # print(_str)
    # out_file_lines.append(_str)

    _out('Checking for non-connected signals on file: ' + filename)

    for _safe_signal in _safe_signal_list:
        _safe_conn_list = _safe_signal.getElementsByTagName('safe-connection')

        # Check for non connections
        _safe_signal_name = _safe_signal.getAttribute('variable')
        _safe_signal_type = _safe_signal.getAttribute('type')

        if _safe_signal_type == NOT_CONNECTED:
            _f_has_nc_signals = True
            # _str = '  ----  [NC Signal]: ' + _safe_signal_name
            _out('[NC]: ' + _safe_signal_name, OUT_ERR)

            #print(_str)
            #out_file_lines.append(_str + '\n')

    # _str = ' -- Finished: ' + filename
    # print(_str)
    # out_file_lines.append(_str)

    # print(str(_safe_signal_list[4]))
    # print(str(_safe_signal_list[4].getElementsByTagName('safe-connection')))
    # print(str(_safe_signal_list[4].getElementsByTagName('safe-connection')[0].getAttribute('member')))

    """
    if _f_has_nc_signals:
        _file = filename.split('\\')[1] + '_results.txt'
        _file = 'results/' + _file
        out_file = open(_file, "w+")
        out_file.writelines(out_file_lines)
        return True
    return False
    """
    return _f_has_nc_signals


def check_signal_pool_size(file_list):

    _normalized_file_list = [filename.split('\\')[1] for filename in file_list]

    # Create a mini dom for each xml file
    _doms = [xml.dom.minidom.parse(filename) for filename in file_list]

    # ### Compare signal pool Size
    # Dictionary is used just for printing purposes
    _dict_signal_pool_size = dict()
    # print(' # Counting and comparing signal pool size...')
    _out('Checking safe-signal pool size for current safe application...')
    _flag_different_pool_size_detected = False
    for i in range(0, len(_doms)-1):

        # Compare mtx files as minidoms against each other
        # _dom_signal_buffer1 = _doms[i].getElementsByTagName('safe-signal')
        # _dom_signal_buffer2 = _doms[i+1].getElementsByTagName('safe-signal')

        # Compare signal pool size
        _dom_signal_buffer1_len = _doms[i].getElementsByTagName('safe-signal').length
        _dom_signal_buffer2_len = _doms[i+1].getElementsByTagName('safe-signal').length

        # Dictionary is used just for printing purposes
        _dict_signal_pool_size[_normalized_file_list[i]] = _dom_signal_buffer1_len
        _dict_signal_pool_size[_normalized_file_list[i+1]] = _dom_signal_buffer2_len

        if _dom_signal_buffer1_len != _dom_signal_buffer2_len:
            #print(' -- Different signal pool size found!')
            #print('  ----  ' + _normalized_file_list[i] + ': ' + str(_dom_signal_buffer1_len))
            #print('  ----  ' + _normalized_file_list[i+1] + ': ' + str(_dom_signal_buffer2_len))
            _flag_different_pool_size_detected = True
    # ### For ends

    # Print signal counting results
    if _flag_different_pool_size_detected:
        _out('Different signal pool size detected!', OUT_ERR)
        for _key in _dict_signal_pool_size:
            _out(' -- ' + _key + ': ' + str(_dict_signal_pool_size[_key]) + ' signals')
    # print(str(_dict_signal_pool_size))

    """
    if _halt_exec:
        print('Process aborted...')
        return False
    return True
    """
    return _flag_different_pool_size_detected


def get_different_safe_signals(file_list):
    return check_signal_pool_integrity(file_list)


def check_signal_pool_integrity(file_list):

    _normalized_file_list = [filename.split('\\')[1] for filename in file_list]

    _xml_tree_list = [etree.parse(_file) for _file in file_list]

    """
    # Initialize excel file
    output_filename = XLS_FILENAME + '.xlsx'
    output_filepath = os.path.join(os.getcwd(), output_filename)
    workbook = xlsxwriter.Workbook(output_filepath)
    worksheet = workbook.add_worksheet('Interface_Differences')
    """

    """
    _list = _xml_tree_list[0].findall('safe-signal')
    print('ATTR: ' + str(_list[3].get('variable')))
    _safe_conn_list = _list[3].findall('safe-connection')
    print('LEN safe conn:' + str(len(_safe_conn_list)))

    """

    # _xlsx_row = 0

    _different_safe_signals = set()

    # Actually compare signals against each other
    for i in range(0, len(_xml_tree_list)-1):

        # Writes/creates a column for the current file under analysis
        # worksheet.write(0, i + 1, _normalized_file_list[i].replace('.mtx', ''))

        for j in range(i + 1, len(_xml_tree_list)):
            # print(' -- Comparing :' + _normalized_file_list[i] + ' against ' + _normalized_file_list[j])

            # Get all safe-signals from i file tree
            _safe_signal_list = _xml_tree_list[i].findall('safe-signal')
            for _safe_signal_1 in _safe_signal_list:

                # Gets all signal names from i file tree
                _safe_signal_variable_1 = _safe_signal_1.get('variable')

                # Check if signal exists in second (j) file tree (the file that i is being compared with)
                _safe_signal_filtered_list_2 = _xml_tree_list[j].findall(
                    'safe-signal[@variable="' + _safe_signal_variable_1 + '"]')
                if len(_safe_signal_filtered_list_2) > 0:
                    _safe_signal_variable_2 = _safe_signal_filtered_list_2[0].get('variable')

                    # Ok, the signal exists in the second file (j)...
                    # Check if safe-connection pool size match
                    safe_conn_list_1 = _safe_signal_1.findall('safe-connection')
                    safe_conn_list_2 = _safe_signal_filtered_list_2[0].findall('safe-connection')
                    if len(safe_conn_list_1) == len(safe_conn_list_2):
                        # print('SAFE-CONN POOL Match')

                        # For each signal pool, check if variables are the same
                        _flag_different_signals = False
                        for k in range(0, len(safe_conn_list_1)):
                            # If safe-conn pool signal names do not match:
                            if safe_conn_list_1[k].get('variable') != safe_conn_list_2[k].get('variable'):
                                _flag_different_signals = True
                                _out(' Info: Different safe-connection signals for safe-signal: '
                                     + _safe_signal_variable_1 + ' while comparing projects '
                                     + _normalized_file_list[i][:3] + '-' + _normalized_file_list[j][:3])

                                # print(' -- ' + _normalized_file_list[j])
                                # print(' [!] safe-connection does not match for signal ' + safe_conn_list_2[k].get('variable'))
                        # For safe_conn_list ends
                        if _flag_different_signals:
                            _different_safe_signals.add(_safe_signal_variable_1)
                            break
                    # If safe-conn pool size does not match:
                    else:
                        # print(' -- ' + _normalized_file_list[j])
                        # print(' [!] Connection pool size does not match for signal: ' + _safe_signal_variable_1)
                        _different_safe_signals.add(_safe_signal_variable_1)
                        _out('    Info: Different safe-connection signal pool size for safe-signal: '
                             + _safe_signal_variable_1 + ' while comparing projects '
                             + _normalized_file_list[i][:3] + '-' + _normalized_file_list[j][:3])
                        # return False
                # If the signal in file tree i is not found in file tree j:
                else:
                    _out('Signal ' + _safe_signal_variable_1 + ' not found in ' + _normalized_file_list[j], OUT_ERR)
                    _different_safe_signals.add(_safe_signal_variable_1)
                    # return False
    if len(_different_safe_signals) > 0:
        _out('Different safe-signals across all projects for the current SA: ')
        _out('   ' + '       \n       '.join(_different_safe_signals))

    return _different_safe_signals


def verify_internal_interface():
    """
    This functional will load the safe applications external interface file (types.mtx)
    For each safe application external interface a mini dom will be generated in order to gather all its members.
    The member size in bytes will be collected.
    Next it will be verified if all the members are 32-bytes aligned.
    The member structure shall obey a specific order in its ending
    :return: True if structure is valid. False otherwise
    """

    _types_mtx_file = os.path.join(MTX_FILE_DIR, TYPES_MTX)
    # print('FILE: ' + _types_mtx_file)
    _types_mtx_file_dom = xml.dom.minidom.parse(_types_mtx_file)

    _compound_list = _types_mtx_file_dom.getElementsByTagName('compound')

    for _compound in _compound_list:
        _compound_name = _compound.getAttribute('name')
        if _compound_name.find('DS_SA') != -1:
            _out('Checking alignment for : ' + _compound_name)

            _compound_member_list = _compound.getElementsByTagName('member')

            _alignment_checker = 32
            # Check for 32bits alignment
            for _compound_member in _compound_member_list:
                _compound_member_size = int(''.join([d for d in _compound_member.getAttribute('type') if d.isdigit()]))
                # print('DIGITS: ' + str(_compound_member_size))

                _alignment_checker -= _compound_member_size
                if _alignment_checker == 0:
                    _alignment_checker += 32

                if _alignment_checker < 0:
                    _out('Invalid alignment detected for ' + _compound_name +
                          ' at ' + _compound_member.getAttribute('name'), OUT_ERR)
                    break
            # FOR compound member list ends

            _ending_checker = [32, 16, 8, 8, 32, 32]
            _ending_checker.reverse()
            _flag_ending_meets_standards = True
            for i in range(0, len(_ending_checker)):
                _compound_member_size = int(''.join(
                    [d for d in _compound_member_list[len(_compound_member_list)-1 - i].getAttribute('type') if d.isdigit()]
                ))
                if _compound_member_size != _ending_checker[i]:
                    _flag_ending_meets_standards = False
            if not _flag_ending_meets_standards:
                _out('Ending of the member structure in ' + _compound_name + ' does not meet the standards.', OUT_ERR)

    # FOR compound list ends


def verify_internal_interface_non_connected_signals(mtx_file_list):
    """
    This function will load the types.mtx internal interface file,
    will look for Safe Application compounds name=DS_SA*,
    for each SA compound, look for members that do NOT contain "padding*", "Reserved*" or "ST_*" on their name.
    For each valid member check safe-signal interface for each Safe application in order to identify connected signals.
    :return: False - If any non-connected signal were found. True - If everything is connected
    """

    INVALID_MEMBER_NAME_PATTERNS = {'ST_', 'padding', 'Reserved', 'SDT_'}
    _types_mtx_file = os.path.join(MTX_FILE_DIR, TYPES_MTX)
    _types_mtx_file_dom = xml.dom.minidom.parse(_types_mtx_file)

    # Parse all the mtx files connection list
    _mtx_doms = [xml.dom.minidom.parse(_mtx_file) for _mtx_file in mtx_file_list]
    all_connections_set = set()

    # Fill a set will all the possible connections
    for _dom in _mtx_doms:
        for _safe_connection in _dom.getElementsByTagName('safe-connection'):
            all_connections_set.add(_safe_connection.getAttribute('member'))

    _out(str(len(all_connections_set)) + ' safe-connections found')

    _compound_list = _types_mtx_file_dom.getElementsByTagName('compound')
    for _compound in _compound_list:
        _compound_name = _compound.getAttribute('name')
        if 'DS_SA' in _compound_name:

            # Now, it is needed to identify the correct members
            _compound_member_list = _compound.getElementsByTagName('member')
            for _compound_member in _compound_member_list:
                _member_name = _compound_member.getAttribute('name')

                for _member_name_pattern in INVALID_MEMBER_NAME_PATTERNS:
                    if _member_name_pattern in _member_name:
                        break
                else:
                    # print('Looking for connections on member: ' + _member_name)
                    if _member_name not in all_connections_set:
                        _out('No connection found for signal: ' + _member_name)

            # FOR _COMPOUND_MEMBER_LIST ENDS
    # FOR _COMPOUND_LIST ENDS
    pass


def _out(text, _type=OUT_INFO):
    _prefix = ''
    if _type == OUT_INFO:
        _prefix = '    '
    elif _type == OUT_ERR:
        _prefix = '[!] '
    print(_prefix + text)
    output_string.append(_prefix + text + '\n')


def _write_output_to_file():
    out_file = open(OUTPUT_FILENAME, "w+")
    out_file.writelines(output_string)


def main():

    mtx_file_list = load_all_SA_mtx_files()
    _normalized_file_list = [filename.split('\\')[1] for filename in mtx_file_list]
    _out(str(len(mtx_file_list)) + ' .mtx files found')

    # if len(mtx_file_list) == 0:
    #     exit(0)

    _out('Checking for non-connected signals...')
    _flag_non_connected_signals_detected = False
    for mtx_file in mtx_file_list:
        if check_not_connected_signals(mtx_file):
            _flag_non_connected_signals_detected = True

    """
    # ESSENTIALY, DO WE NEED TO DO SOMETHING IF SIGNALS ARE DETECTED AS NON_CONNECTED?
    # Disabled while we debug
    # In order to compare signal interfaces, first fix non-connected signals
    if _flag_halt_exec:
        input()
        exit(0)
    """
    # Verifica a pool size e a integrity para cada SA
    safe_applications = dict()

    for mtx_file in _normalized_file_list:
        _sa_number = int(mtx_file[11])
        if _sa_number not in safe_applications.keys():
            safe_applications[_sa_number] = []
        safe_applications[_sa_number].append(os.path.join(MTX_FILE_DIR, mtx_file))

    for _sa_key in safe_applications:
        _file_list = safe_applications[_sa_key]
        _out(' - - - [INFO] - - - Comparing .mtx files for SA' + str(_sa_key))

        check_signal_pool_size(_file_list)
        check_signal_pool_integrity(_file_list)
    # _dif_safe_signals = get_different_safe_signals(mtx_file_list)
    # Export to xlsx (_dif_safe_signals)
    _out('OK')
    # print('\n ### MTX files comparison finished... ###')

    _out('Analysing MTX external interface alignment...')
    verify_internal_interface()
    verify_internal_interface_non_connected_signals(mtx_file_list)

    _write_output_to_file()
    _out('Finished')
    # Press any key to exit...
    print('\n Press any key to exit...')
    input()


if __name__ == "__main__":
    main()
