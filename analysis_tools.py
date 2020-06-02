"""

"""
from lxml import etree


class AnalysisTools:


    #def compare_project_safe_connection_structure(self):
        #self.model = dict()

    def compare_signals_among_projects(self, ccus_data):
        analysis_results = dict()
        sa_dict = dict()

        for _file_data in ccus_data:
            _sa = _file_data['sa']
            if _sa not in sa_dict:
                sa_dict[_sa] = list()
            sa_dict[_sa].append(_file_data)

        for _sa_key in sa_dict.keys():
            analysis_results[_sa_key] = self._compare_sa_signals_among_projets(sa_dict[_sa_key])
        return analysis_results

    def _compare_sa_signals_among_projets(self, sa_list):
        sa_analysis_results = dict()

        # Compare signals against each other
        for i in range(0, len(sa_list) - 1):
            for j in range(i + 1, len(sa_list)):

                print(' -- Comparing :' + sa_list[i]['filename'] + ' against ' + sa_list[j]['filename'])

                # Get all safe-signals from i file tree
                _safe_signal_list = sa_list[i]['etree'].findall('safe-signal')
                for _safe_signal_1 in _safe_signal_list:

                    # Gets all signal names from i file tree
                    _safe_signal_variable_1 = _safe_signal_1.get('variable')

                    # if this signal is not registered
                    if _safe_signal_variable_1 not in sa_analysis_results:
                        sa_analysis_results[_safe_signal_variable_1] = dict()

                    # if the signal is registered but the project is not...
                    if sa_list[i]['project'] not in sa_analysis_results[_safe_signal_variable_1]:
                        sa_analysis_results[_safe_signal_variable_1][sa_list[i]['project']] = set()

                    # Check if signal exists in second (j) file tree (the file that i is being compared with)
                    _safe_signal_filtered_list_2 = sa_list[j]['etree'].findall(
                        'safe-signal[@variable="' + _safe_signal_variable_1 + '"]')

                    if len(_safe_signal_filtered_list_2) > 0:
                        _safe_signal_variable_2 = _safe_signal_filtered_list_2[0].get('variable')

                        # Ok, the signal exists in the second file (j)...
                        # Check if safe-connection pool size match
                        safe_conn_list_1 = _safe_signal_1.findall('safe-connection')
                        safe_conn_list_2 = _safe_signal_filtered_list_2[0].findall('safe-connection')
                        if len(safe_conn_list_1) == len(safe_conn_list_2):

                            # For each signal pool, check if variables are the same
                            for k in range(0, len(safe_conn_list_1)):
                                # If safe-conn pool signal names do not match:
                                if (safe_conn_list_1[k].get('variable') != safe_conn_list_2[k].get('variable')) \
                                        or (safe_conn_list_1[k].get('member') != safe_conn_list_2[k].get('member')):
                                    break
                            else:
                                # Signal pool is the same, register...
                                # Register for project i, equivalence to project j
                                if sa_list[i]['project'] not in sa_analysis_results[_safe_signal_variable_1]:
                                    sa_analysis_results[_safe_signal_variable_1][sa_list[i]['project']] = set()
                                sa_analysis_results[_safe_signal_variable_1][sa_list[i]['project']] \
                                    .update({sa_list[j]['project']})

                                # Register for project j, equivalence to project i
                                if sa_list[j]['project'] not in sa_analysis_results[_safe_signal_variable_1]:
                                    sa_analysis_results[_safe_signal_variable_1][sa_list[j]['project']] = set()
                                sa_analysis_results[_safe_signal_variable_1][sa_list[j]['project']] \
                                    .update({sa_list[i]['project']})
        return sa_analysis_results
