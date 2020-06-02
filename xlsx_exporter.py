"""

"""
import os
import xlsxwriter as xlsxwriter


class XLSXExporter:

    FILENAME = 'workitems_export'

    def __init__(self, filename):
        output_filename = filename + '.xlsx'
        output_filepath = os.path.join(os.getcwd(), output_filename)

        self.workbook = xlsxwriter.Workbook(output_filepath)

    def export_signal_comparison_among_projects(self, export_data, sheet_name):
        """
        :param export_data:
            { *SA_name_key* :
                { *signal_name_key*:
                    { *project_name_key*: # Each project in which this signal was found
                        set { each project with the same signal structure }
                    }
                }
            }
        :param sheet_name: sheet name in workbook
        :return:
        """

        worksheet = self.workbook.add_worksheet(sheet_name)

        ##### HEADER #####

        worksheet.write(0, 0, 'SA')
        worksheet.write(0, 1, 'Signal')

        OFFSET_DICTIONARY = {
            'LOT': 2,
            'EEA': 3,
            'SWR': 4,
            'WML': 5
        }

        for _offset_key in OFFSET_DICTIONARY.keys():
            worksheet.write(0, OFFSET_DICTIONARY[_offset_key], _offset_key)

        ##### HEADER ENDS #####

        row = 1
        for _sa_key in export_data.keys():
            for _signal_name_key in export_data[_sa_key].keys():
                for _project_key in export_data[_sa_key][_signal_name_key].keys():
                    _project_set_for_signal = export_data[_sa_key][_signal_name_key][_project_key]

                    col = 0
                    worksheet.write(row, col, _sa_key)

                    col += 1
                    worksheet.write(row, col, _signal_name_key)

                    worksheet.write(row, OFFSET_DICTIONARY[_project_key],
                                    str(len(_project_set_for_signal)+1) + ": " + str(_project_set_for_signal))
                row += 1

    def save(self):
        self.workbook.close()

