"""

"""
import os
import xml

from lxml import etree

from config.config_loader import ConfigLoader


class CcusProjectData:

    def __init__(self):
        self.mtx_file_data = None

    def load_local_mtx_files(self):
        """

        :return:
        """
        if self.mtx_file_data is None:

            mtx_file_dir = ConfigLoader.getinstance().config_section_map('local')['project_sa_mtx']
            self.mtx_file_data = list()

            for file in os.listdir(mtx_file_dir):
                if file.endswith(".mtx"):
                    _file_dir = os.path.join(mtx_file_dir, file)
                    if '_SA' in file:
                        _file_data = {
                            'filename': file,
                            'project': file.split("_")[0],
                            'sa': file.split("_")[2],
                            'component': file.split("_")[3],
                            'file_dir': _file_dir,
                            'etree': etree.parse(_file_dir)
                            #'dom': xml.dom.minidom.parse(_file_dir)
                        }
                        self.mtx_file_data.append(_file_data)
        return self.mtx_file_data

    def download_data_from_rtc_stream(self):
        # TODO: Future feature
        pass
