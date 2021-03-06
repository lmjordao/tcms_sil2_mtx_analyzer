import os
import xml.dom.minidom
from lxml import etree
import xlwings

# Set these according to project
MTX_FILE_DIR = 'mtx_files'
# EXT_INTERFACE_FILE_DIR = ''
TYPES_MTX = 'types.mtx'

# Set these as convenience
XLS_FILENAME = 'interface_report.xlsx'
OUTPUT_FILENAME = 'results.txt'

# Globals
OUT_INFO = 1
OUT_ERR = -1

output_string = []
list_signals_global = []
list_sa_global = []
list_project_global = []
list_status_global = []
list_comparison_global = []
list_signals_comparison_global = []
list_nc_type_global = []
list_proj_nc_type_global = []
safe_signals_global = []


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
    list_signals = []
    list_project = []
    list_sa = []
    list_connected = []
    for _safe_signal in _safe_signal_list:
        _safe_conn_list = _safe_signal.getElementsByTagName('safe-connection')
        # Check for non connections
        _safe_signal_name = _safe_signal.getAttribute('variable')
        _safe_signal_type = _safe_signal.getAttribute('type')

        # se o nome dos ficheiros for mudado, tem que se mudar aqui tambem os [] ou deixa de funcionar
        list_signals.append(_safe_signal_name)
        filename_split = filename.partition("\\")[2]
        list_project.append(filename_split.split("_")[0])
        list_sa.append(filename_split.split("_")[2])
        list_connected.append(_safe_signal_type)

        if _safe_signal_type == NOT_CONNECTED:
            _f_has_nc_signals = True
            # _str = '  ----  [NC Signal]: ' + _safe_signal_name
            _out('[NC]: ' + _safe_signal_name, OUT_ERR)
            # print(_str)
            # out_file_lines.append(_str + '\n')

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
    list_signals_global.append(list_signals)
    list_project_global.append(list_project)
    list_sa_global.append(list_sa)
    list_status_global.append(list_connected)

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
    for i in range(0, len(_doms) - 1):

        # Compare mtx files as minidoms against each other
        # _dom_signal_buffer1 = _doms[i].getElementsByTagName('safe-signal')
        # _dom_signal_buffer2 = _doms[i+1].getElementsByTagName('safe-signal')

        # Compare signal pool size
        _dom_signal_buffer1_len = _doms[i].getElementsByTagName('safe-signal').length
        _dom_signal_buffer2_len = _doms[i + 1].getElementsByTagName('safe-signal').length

        # Dictionary is used just for printing purposes
        _dict_signal_pool_size[_normalized_file_list[i]] = _dom_signal_buffer1_len
        _dict_signal_pool_size[_normalized_file_list[i + 1]] = _dom_signal_buffer2_len

        if _dom_signal_buffer1_len != _dom_signal_buffer2_len:
            # print(' -- Different signal pool size found!')
            # print('  ----  ' + _normalized_file_list[i] + ': ' + str(_dom_signal_buffer1_len))
            # print('  ----  ' + _normalized_file_list[i+1] + ': ' + str(_dom_signal_buffer2_len))
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
    projects_used = []
    for i in _normalized_file_list:
        projects_used.append(i.split('_')[0])
    sa_used = i.split('CCUS_')[1].split('_')[0]

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
    num_saf_con = [[] for _ in range(0, len(_xml_tree_list))]
    name_safe_signals = []
    # index_safe_signal = 0
    is_first_round = True
    is_first_add = True

    # Actually compare signals against each other
    for i in range(0, len(_xml_tree_list) - 1):
        # Writes/creates a column for the current file under analysis
        # worksheet.write(0, i + 1, _normalized_file_list[i].replace('.mtx', ''))
        for j in range(i + 1, len(_xml_tree_list)):
            print('primeiro for')
            print(' -- Comparing :' + _normalized_file_list[i] + ' against ' + _normalized_file_list[j])
            #input('cjreck')
            # Get all safe-signals from i file tree
            _safe_signal_list = _xml_tree_list[i].findall('safe-signal')
            for _safe_signal_1 in _safe_signal_list:
                print('segundo for')
                # Gets all signal names from i file tree
                _safe_signal_variable_1 = _safe_signal_1.get('variable')
                print(_safe_signal_variable_1)
                #print(index_safe_signal)
                # aux = index_safe_signal
                if _safe_signal_variable_1 in name_safe_signals:
                    index_safe_signal = name_safe_signals.index(_safe_signal_variable_1)
                    print('if1 index', index_safe_signal)
                    # aux = aux -1
                    # print(aux)
                else:
                    print('new')
                    name_safe_signals.append(_safe_signal_variable_1)
                    for cur_list in num_saf_con:
                        cur_list.append(0)
                    index_safe_signal = len(name_safe_signals) - 1
                    print('if2 index', index_safe_signal)
                # Check if signal exists in second (j) file tree (the file that i is being compared with)
                _safe_signal_filtered_list_2 = _xml_tree_list[j].findall(
                    'safe-signal[@variable="' + _safe_signal_variable_1 + '"]')
                if len(_safe_signal_filtered_list_2) > 0:
                    _safe_signal_variable_2 = _safe_signal_filtered_list_2[0].get('variable')
                    print(_safe_signal_variable_2)
                    print(_safe_signal_variable_2)
                    # Ok, the signal exists in the second file (j)...
                    # Check if safe-connection pool size match
                    safe_conn_list_1 = _safe_signal_1.findall('safe-connection')
                    safe_conn_list_2 = _safe_signal_filtered_list_2[0].findall('safe-connection')
                    '''print('i1: ', _normalized_file_list[i][:3])
                    print(num_saf_con[i][index_safe_signal])
                    print('j2: ', _normalized_file_list[j][:3])
                    print(num_saf_con[j][index_safe_signal])'''
                    if len(safe_conn_list_1) == len(safe_conn_list_2):
                        # print('SAFE-CONN POOL Match')
                        # For each signal pool, check if variables are the same
                        _flag_different_signals = False
                        for k in range(0, len(safe_conn_list_1)):
                            # If safe-conn pool signal names do not match:
                            print(safe_conn_list_1[k].get('variable'))
                            print(safe_conn_list_2[k].get('variable'))
                            print('status first round', is_first_round)
                            print('status first add', is_first_add)
                            if (safe_conn_list_1[k].get('variable') != safe_conn_list_2[k].get('variable')) \
                                    or (safe_conn_list_1[k].get('member') != safe_conn_list_2[k].get('member')):
                                _flag_different_signals = True
                                print('zero if')
                                if is_first_round is True:
                                    print('primeiro if true')
                                    if (len(safe_conn_list_1) != 0) and (is_first_add is True):
                                        num_saf_con[i][index_safe_signal] = num_saf_con[i][index_safe_signal] + 1
                                        print('primeiro if')
                                        # is_first_add = False
                                    if len(safe_conn_list_2) != 0:
                                        print('seg if')
                                        num_saf_con[j][index_safe_signal] = num_saf_con[j][index_safe_signal] + 1

                                    # is_first_round = False
                                _out(' Info: Different safe-connection signals for safe-signal: '
                                     + _safe_signal_variable_1 + ' while comparing projects '
                                     + _normalized_file_list[i][:3] + '-' + _normalized_file_list[j][:3])
                            else:
                                print('primeiro else')
                                if is_first_round is True:
                                    print('seg if true')
                                    if (len(safe_conn_list_1) != 0) and (is_first_add is True):
                                        print('terceiro if')
                                        num_saf_con[i][index_safe_signal] = num_saf_con[i][index_safe_signal] + 1
                                        # is_first_add = False
                                    if len(safe_conn_list_2) != 0:
                                        print('quarto if')
                                        num_saf_con[j][index_safe_signal] = num_saf_con[j][index_safe_signal] + 1
                                num_saf_con[i][index_safe_signal] = num_saf_con[i][index_safe_signal] + 1
                                num_saf_con[j][index_safe_signal] = num_saf_con[j][index_safe_signal] + 1
                                    # is_first_round = False
                                # num_saf_con[i][index_safe_signal] = num_saf_con[i][index_safe_signal] + 1
                                # num_saf_con[j][index_safe_signal] = num_saf_con[j][index_safe_signal] + 1
                                # print(' -- ' + _normalized_file_list[j])
                                # print(' [!] safe-connection does not match for signal ' + safe_conn_list_2[k].get('variable'))
                        print('i: ', _normalized_file_list[i][:3])
                        print(num_saf_con[i][index_safe_signal])
                        print('j: ', _normalized_file_list[j][:3])
                        print(num_saf_con[j][index_safe_signal])
                        print('status add', is_first_add)
                        '''if index_safe_signal == 254:
                            # if _safe_signal_variable_1 == 'STCC_X_CabStatus':
                            input('sinal pause2')'''
                        # if _safe_signal_variable_1 == 'STCC_X_CabStatus':
                        # if _safe_signal_variable_1 == 'MIO_S_BrApBg1Car1':
                        if _safe_signal_variable_1 == 'SMH_S_TcmsHltCar1':
                            # print(index_safe_signal)
                            input('sinal pause1')
                        # For safe_conn_list ends
                        # input('stop')
                        if _flag_different_signals:
                            _different_safe_signals.add(_safe_signal_variable_1)
                            break
                    # If safe-conn pool size does not match:
                    else:
                        print('seg else')
                        if is_first_round is True:
                            print('seg if true')
                            if (len(safe_conn_list_1) != 0) and (is_first_add is True):
                                print('terceiro if')
                                num_saf_con[i][index_safe_signal] = num_saf_con[i][index_safe_signal] + 1
                                # is_first_add = False
                            if len(safe_conn_list_2) != 0:
                                print('quarto if')
                                num_saf_con[j][index_safe_signal] = num_saf_con[j][index_safe_signal] + 1
                        # print(' -- ' + _normalized_file_list[j])
                        # print(' [!] Connection pool size does not match for signal: ' + _safe_signal_variable_1)
                        _different_safe_signals.add(_safe_signal_variable_1)
                        _out('    Info: Different safe-connection signal pool size for safe-signal: '
                             + _safe_signal_variable_1 + ' while comparing projects '
                             + _normalized_file_list[i][:3] + '-' + _normalized_file_list[j][:3])
                        # return False
                # If the signal in file tree i is not found in file tree j:
                print('i: ', _normalized_file_list[i][:3])
                print(num_saf_con[i][index_safe_signal])
                print('j: ', _normalized_file_list[j][:3])
                print(num_saf_con[j][index_safe_signal])
                print('status add', is_first_add)
                '''if index_safe_signal == 254:
                    # if _safe_signal_variable_1 == 'STCC_X_CabStatus':
                    input('sinal pause2')'''
                # if _safe_signal_variable_1 == 'STCC_X_CabStatus':
                # if _safe_signal_variable_1 == 'MIO_S_BrApBg1Car1':
                if _safe_signal_variable_1 == 'SMH_S_TcmsHltCar1':
                    # print(index_safe_signal)
                    input('sinal pause1')
                else:
                    print('terceiro else')
                    if is_first_round is True:
                        print('terceiro if true')
                        if ((len(safe_conn_list_1) != 0) and (is_first_add is True)):
                            print('quinto if')
                            num_saf_con[i][index_safe_signal] = num_saf_con[i][index_safe_signal] + 1
                            # is_first_add = False
                        if len(safe_conn_list_2) != 0:
                            print('sexto if')
                            num_saf_con[j][index_safe_signal] = num_saf_con[j][index_safe_signal] + 0
                        # is_first_round = False
                    _out('Signal ' + _safe_signal_variable_1 + ' not found in ' + _normalized_file_list[j], OUT_ERR)
                    _different_safe_signals.add(_safe_signal_variable_1)
                    # return False
                # index_safe_signal = aux + 1
                print('i: ', _normalized_file_list[i][:3])
                print(num_saf_con[i][index_safe_signal])
                print('j: ', _normalized_file_list[j][:3])
                print(num_saf_con[j][index_safe_signal])
                print('status add', is_first_add)
                '''if index_safe_signal == 254:
                    # if _safe_signal_variable_1 == 'STCC_X_CabStatus':
                    input('sinal pause2')'''
                # if _safe_signal_variable_1 == 'STCC_X_CabStatus':
                # if _safe_signal_variable_1 == 'MIO_S_BrApBg1Car1':
                if _safe_signal_variable_1 == 'SMH_S_TcmsHltCar1':
                    # print(index_safe_signal)
                    input('sinal pause1')
            is_first_add = False
            '''print('i: ', _normalized_file_list[i][:3])
            print(num_saf_con[i][index_safe_signal])
            print('j: ', _normalized_file_list[j][:3])
            print(num_saf_con[j][index_safe_signal])
            if _safe_signal_variable_1 == 'MIO_S_BrApBg1Car1':
            #if _safe_signal_variable_1 == 'STCC_X_CabStatus':
                input('sinal pause')'''
            # input('check out')
        is_first_round = False
    if len(_different_safe_signals) > 0:
        _out('Different safe-signals across all projects for the current SA: ')
        _out('   ' + '       \n       '.join(_different_safe_signals))

    global safe_signals_global
    safe_signals = [projects_used]
    safe_signals.append([sa_used] * len(name_safe_signals))
    safe_signals.append(name_safe_signals)
    safe_signals.append(num_saf_con)
    safe_signals_global.append(safe_signals)
    return _different_safe_signals


def verify_internal_interface(file_path):
    """
    This functional will load the safe applications external interface file (types.mtx)
    For each safe application external interface, a mini dom will be generated in order to gather all its members.
    The member size in bytes will be collected.
    Next it will be verified if all the members are 32-bytes aligned.
    The member structure shall obey a specific order in its ending
    :return: True if structure is valid. False otherwise
    """

    _types_mtx_file = os.path.join(file_path, TYPES_MTX)
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
                    [d for d in _compound_member_list[len(_compound_member_list) - 1 - i].getAttribute('type') if
                     d.isdigit()]
                ))
                if _compound_member_size != _ending_checker[i]:
                    _flag_ending_meets_standards = False
            if not _flag_ending_meets_standards:
                _out('Ending of the member structure in ' + _compound_name + ' does not meet the standards.', OUT_ERR)

    # FOR compound list ends


def verify_internal_interface_non_connected_signals(file_path, mtx_file_list):
    """
    This function will load the types.mtx internal interface file,
    will look for Safe Application compounds name=DS_SA*,
    for each SA compound, look for members that do NOT contain "padding*", "Reserved*" or "ST_*" on their name.
    For each valid member check safe-signal interface for each Safe application in order to identify connected signals.
    :return: False - If any non-connected signal were found. True - If everything is connected
    """

    INVALID_MEMBER_NAME_PATTERNS = {'ST_', 'padding', 'Reserved', 'SDT_', 'Variable', 'variable'}
    _types_mtx_file = os.path.join(file_path, TYPES_MTX)
    _types_mtx_file_dom = xml.dom.minidom.parse(_types_mtx_file)

    # Parse all the mtx files connection list
    _mtx_doms = [xml.dom.minidom.parse(_mtx_file) for _mtx_file in mtx_file_list]
    all_connections_set = set()

    # Fill a set will all the possible connections
    for _dom in _mtx_doms:
        for _safe_connection in _dom.getElementsByTagName('safe-connection'):
            all_connections_set.add(_safe_connection.getAttribute('member'))
    _out(str(len(all_connections_set)) + ' safe-connections found')

    all_connections_type_set = set()
    _compound_list = _types_mtx_file_dom.getElementsByTagName('compound')
    for _compound in _compound_list:
        _compound_name = _compound.getAttribute('name')
        if 'DS_SA' in _compound_name:
            # Now, it is needed to identify the correct members
            _compound_member_list = _compound.getElementsByTagName('member')
            print(_compound_member_list)
            for _compound_member in _compound_member_list:
                _member_name = _compound_member.getAttribute('name')
                for _member_name_pattern in INVALID_MEMBER_NAME_PATTERNS:
                    if _member_name_pattern in _member_name:
                        break
                else:
                    all_connections_type_set.add(_member_name)
                    # print('Looking for connections on member: ' + _member_name)
                    if _member_name not in all_connections_set:
                        # _out('No connection found for signal: ' + _member_name)
                        _out('No connection found in SA for signal: ' + _member_name)

    difference = list(set(all_connections_type_set) - set(all_connections_set))
    invalid_list = []
    for item in difference:
        for _member_name_pattern in INVALID_MEMBER_NAME_PATTERNS:
            if _member_name_pattern in item:
                invalid_list.append(item)
                print('invalid', _member_name_pattern)
    list_difference = set(difference) - set(invalid_list)
    for _member_name in list_difference:
        _out('No connection found in type for signal: ' + _member_name)
        list_proj_nc_type_global.append(_types_mtx_file.partition("\\")[2].partition("\\")[0])
        list_nc_type_global.append(_member_name)
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


def _write_output_to_file(file_path):
    out_file = open(os.path.join(file_path, OUTPUT_FILENAME), "w+")
    out_file.writelines(output_string)


def _export_excel_file(folder_path):
    file_path = os.path.join(folder_path, XLS_FILENAME)
    if not os.path.isfile(file_path):
        workbook = xlwings.Book()
    else:
        workbook = xlwings.Book(file_path)

    ws_names = [sh.name for sh in workbook.sheets]
    if 'Signals from SA' in ws_names:
        worksheet = workbook.sheets['Signals from SA']
        worksheet.clear_contents()
    else:
        worksheet = workbook.sheets.add('Signals from SA')
    worksheet.range('A1').options(transpose=True).value = [item for sublist in list_signals_global for item in sublist]
    worksheet.range('B1').options(transpose=True).value = [item for sublist in list_sa_global for item in sublist]
    worksheet.range('C1').options(transpose=True).value = [item for sublist in list_project_global for item in sublist]
    worksheet.range('D1').options(transpose=True).value = [item for sublist in list_status_global for item in sublist]
    table = worksheet.range("A1").expand('table')
    worksheet.api.ListObjects.Add(1, worksheet.api.Range(table.address))
    worksheet.range('A1').options(header=True).value = ['Signal', 'SA', 'Project', 'Status']

    if 'Signals comparison table' in ws_names:
        worksheet = workbook.sheets['Signals comparison table']
        worksheet.clear_contents()
    else:
        worksheet = workbook.sheets.add('Signals comparison table')
    worksheet.range('A1').options(transpose=True).value = list_signals_comparison_global
    worksheet.range('B1').options(transpose=True).value = list_comparison_global
    table = worksheet.range("A1").expand('table')
    worksheet.api.ListObjects.Add(1, worksheet.api.Range(table.address))
    proj_list = list(set([item for sublist in list_project_global for item in sublist]))
    proj_list.sort()
    worksheet.range('A1').value = ['Signal'] + proj_list + ['In all projects']
    # workbook.api.RefreshAll()

    if 'Connections comparison table' in ws_names:
        worksheet = workbook.sheets['Connections comparison table']
        worksheet.clear_contents()
    else:
        worksheet = workbook.sheets.add('Connections comparison table')
    sa_safe_signals = []
    name_safe_signals = []
    proj_list = list(set([item for sublist in list_project_global for item in sublist]))
    proj_list.sort()
    num_saf_con_ = [[] for _ in proj_list]
    for i in safe_signals_global:
        sa_safe_signals.append(i[1])
        name_safe_signals.append(i[2])
        if proj_list == i[0]:
            for j, _ in enumerate(proj_list):
                num_saf_con_[j].append(i[3][j])
        else:
            order = 0
            for j, item1 in enumerate(proj_list):
                if item1 in i[0]:
                    num_saf_con_[j].append(i[3][order])
                    order = order + 1
                else:
                    num_saf_con_[j].append(['No'] * len(i[2]))
    num_safe = [[] for _ in proj_list]
    for j, _ in enumerate(proj_list):
        num_safe[j] = [item for sublist in num_saf_con_[j] for item in sublist]
    worksheet.range('A1').options(transpose=True).value = [item for sublist in sa_safe_signals for item in sublist]
    worksheet.range('B1').options(transpose=True).value = [item for sublist in name_safe_signals for item in sublist]
    worksheet.range('C1').options(transpose=True).value = num_safe
    table = worksheet.range("A1").expand('table')
    worksheet.api.ListObjects.Add(1, worksheet.api.Range(table.address))
    worksheet.range('A1').value = ['SA', 'Signal'] + proj_list

    if 'Signals NC in types' in ws_names:
        worksheet = workbook.sheets['Signals NC in types']
        worksheet.clear_contents()
    else:
        worksheet = workbook.sheets.add('Signals NC in types')
    worksheet.range('A1').options(transpose=True).value = list_nc_type_global
    worksheet.range('B1').options(transpose=True).value = list_proj_nc_type_global
    table = worksheet.range("A1").expand('table')
    worksheet.api.ListObjects.Add(1, worksheet.api.Range(table.address))
    worksheet.range('A1').value = ['Signal', "Project"]

    if 'Sheet1' in ws_names:
        worksheet = workbook.sheets['Sheet1']
        worksheet.delete()

    txt_path = os.path.join(folder_path, OUTPUT_FILENAME)
    file1 = open(txt_path, 'r')
    lines = file1.readlines()
    line_nc = []
    project_nc = []
    sa_nc = []
    aligned = []
    project_aligned = []
    sa_aligned = []
    signal_not_aligned = []
    # se o nome dos ficheiros mudar, tem que se trocar os indices utilizados
    for line in lines:
        if "Checking for non-connected signals on file:" in line:
            info_line = line.split(": ")[1].partition("\\")[2]
        if "[!] [NC]:" in line:
            line_nc.append(line.split(": ")[1].split("\n")[0])
            project_nc.append(info_line.split("_")[0])
            sa_nc.append(info_line.split("_")[2])
        if "For project" in line:
            actual_project = line.split(": ")[1]
        if "Checking alignment for :" in line:
            info_line = line.split(": ")[1].partition("_")[2].partition("_")[0]
            sa_aligned.append(info_line)
            project_aligned.append(actual_project)
            aligned.append('Yes')
            signal_not_aligned.append('None')
        if "Invalid alignment detected" in line:
            del aligned[-1]
            del signal_not_aligned[-1]
            aligned.append('No')
            info_line = line.split("at ")[1].partition("\n")[0]
            signal_not_aligned.append(info_line)
    file1.close()

    if 'Signals NC in SA' in ws_names:
        worksheet = workbook.sheets['Signals NC in SA']
        worksheet.clear_contents()
    else:
        worksheet = workbook.sheets.add('Signals NC in SA')
    worksheet.range('A1').options(transpose=True).value = line_nc
    worksheet.range('B1').options(transpose=True).value = project_nc
    worksheet.range('C1').options(transpose=True).value = sa_nc
    table = worksheet.range("A1").expand('table')
    worksheet.api.ListObjects.Add(1, worksheet.api.Range(table.address))
    worksheet.range('A1').value = ['Signal', 'Project', 'SA']

    if 'Alignment' in ws_names:
        worksheet = workbook.sheets['Alignment']
        worksheet.clear_contents()
    else:
        worksheet = workbook.sheets.add('Alignment')
    worksheet.range('A1').options(transpose=True).value = project_aligned
    worksheet.range('B1').options(transpose=True).value = sa_aligned
    worksheet.range('C1').options(transpose=True).value = aligned
    worksheet.range('D1').options(transpose=True).value = signal_not_aligned
    table = worksheet.range("A1").expand('table')
    worksheet.api.ListObjects.Add(1, worksheet.api.Range(table.address))
    worksheet.range('A1').value = ['Project', 'SA', 'Aligned', 'Signal not aligned']

    workbook.save(file_path)


def _comparison_between_projects():
    global list_signals_global
    global list_project_global
    global list_sa_global
    global list_status_global
    global list_signals_comparison_global
    # create only four lists, one for each project
    list_signals = []
    list_projects = []
    list_sa = []
    list_status = []
    aux_list_signals = []
    aux_list_projects = []
    aux_list_sa = []
    aux_list_status = []
    i = 0
    actual_project = list_project_global[0][0]
    while i < len(list_signals_global):
        if actual_project != list_project_global[i][0]:
            actual_project = list_project_global[i][0]
            aux_list_signals.append(list_signals)
            aux_list_projects.append(list_projects)
            aux_list_sa.append(list_sa)
            aux_list_status.append(list_status)
            list_signals = []
            list_projects = []
            list_sa = []
            list_status = []

        for item in list_signals_global[i]:
            list_signals.append(item)
        for item in list_project_global[i]:
            list_projects.append(item)
        for item in list_sa_global[i]:
            list_sa.append(item)
        for item in list_status_global[i]:
            list_status.append(item)
        i = i + 1
    aux_list_signals.append(list_signals)
    aux_list_projects.append(list_projects)
    aux_list_sa.append(list_sa)
    aux_list_status.append(list_status)
    list_signals_global = aux_list_signals
    list_project_global = aux_list_projects
    list_sa_global = aux_list_sa
    list_status_global = aux_list_status

    # create list of all the signals of all projects
    i = 0
    for list_used in list_signals_global:
        if i == 0:
            list_signals_comparison_global = []
            for item in list_signals_global[0]:
                list_signals_comparison_global.append(item)
        else:
            comp = set(list_signals_comparison_global) - set(list_used)
            for item in comp:
                list_signals_comparison_global.append(item)
        i = i + 1

    # create lists for each project with info of each signals exists or not
    for list_used in list_signals_global:
        list_comparison = ['No'] * len(list_signals_comparison_global)
        for j, item in enumerate(list_signals_comparison_global):
            if item in list_used:
                list_comparison[j] = 'Yes'
        list_comparison_global.append(list_comparison)

    # create list for signals presents in all projects
    list_comparison = ['No'] * len(list_signals_comparison_global)
    for j, item in enumerate(list_signals_comparison_global):
        i = 0
        total_yes = 0
        while i < len(list_comparison_global):
            if list_comparison_global[i][j] == 'Yes':
                total_yes = total_yes + 1
            i = i + 1
        if total_yes == len(list_comparison_global):
            list_comparison[j] = 'Yes'
    list_comparison_global.append(list_comparison)


def main():
    list_actualized = []
    path_input = 'types'
    path_output = 'results'
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
    # TYPES.MTX

    # check folders
    folders_list = os.listdir(path_input)
    for i in folders_list:
        if os.path.isdir(os.path.join(path_input, i)):
            message = "For project: " + i
            _out(message)
            _out('Analysing MTX external interface alignment...')
            # Verifica o alinhamento
            verify_internal_interface(os.path.join(path_input, i))
            # procura na lista de mtx_files apenas os que pertencem ao projecto
            mtx_file_list_project = []
            search_string = ''.join([i, '_'])
            for j in mtx_file_list:
                index = j.find(search_string)
                if not index == -1:
                    mtx_file_list_project.append(j)
                else:
                    continue

            if not len(mtx_file_list_project) == 0:
                list_actualized.append(i)
                # Verifica as ligações entre types.mtx e restantes mtx
                verify_internal_interface_non_connected_signals(os.path.join(path_input, i), mtx_file_list_project)
    _write_output_to_file(path_output)
    del output_string[:]

    _comparison_between_projects()
    _export_excel_file(path_output)

    _out('Finished')
    print('Projects', list_actualized, 'were actualized')
    # Press any key to exit...
    print('\n Press any key to exit...')
    input()


if __name__ == "__main__":
    main()
