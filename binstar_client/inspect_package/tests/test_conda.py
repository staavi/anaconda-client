from __future__ import print_function, unicode_literals

# Standard libary imports
from os import path
import unittest

# Local imports
from binstar_client.inspect_package import conda
from binstar_client.utils.notebook.data_uri import data_uri_from


def data_path(filename):
    return path.join(path.dirname(__file__), 'data', filename)


expected_package_data = {
    'home': None,
    'description': '',
    'dev_url': None,
    'doc_url': None,
    'license': None,
    'license_url': None,
    'source_git_url': None,
    'name': 'conda_gc_test',
    'summary': 'This is a simple meta-package',
}

expected_version_data_121 = {
    'source_git_tag': None,
    'description': '',
    'home_page': None,
    'icon': None,  # The icon if found on the conda folder is uplaoded here.
    'version': '1.2.1',
}

expected_version_data_221 = {
    'source_git_tag': None,
    'description': '',
    'home_page': None,
    'icon': None,  # The icon if found on the conda folder is uplaoded here.
    'version': '2.2.1',
    }

expected_file_data_121 = {
    'attrs': {
        'arch': 'x86_64',
        'build': 'py27_3',
        'build_number': 3,
        'depends': ['foo ==3*', 'python ==2.7.8'],
        'license': None,
        'machine': 'x86_64',
        'operatingsystem': 'darwin',
        'platform': 'osx',
        'subdir': 'osx-64',
        'target-triplet': 'x86_64-any-darwin',
        'has_prefix': False,
        },
    'basename': 'osx-64/conda_gc_test-1.2.1-py27_3.tar.bz2',
    'dependencies': {
        'depends': [{'name': 'foo', 'specs': [['==', '3']]},
                    {'name': 'python', 'specs': [['==', '2.7.8']]}],
        },
    }

expected_file_data_221 = {
    'attrs': {
        'arch': 'x86_64',
        'build': 'py27_3',
        'build_number': 3,
        'depends': ['foo ==3*', 'python ==2.7.8'],
        #'license': None,
        'machine': 'x86_64',
        'operatingsystem': 'linux',
        'platform': 'linux',
        'subdir': 'linux-64',
        'target-triplet': 'x86_64-any-linux',
        'has_prefix': False,
        },
    'basename': 'linux-64/conda_gc_test-2.2.1-py27_3.tar.bz2',
    'dependencies': {
        'depends': [{'name': 'foo', 'specs': [['==', '3']]},
                    {'name': 'python', 'specs': [['==', '2.7.8']]}],
        },
    }

# Test package application data
# -----------------------------------------------------------------------------
ICON_B64 = data_uri_from(data_path('43c9b994a4d96f779dad87219d645c9f.png'))
app_expected_package_data = {
    'home': 'http://home.page',
    'description': 'test description',
    'dev_url': 'https://dev.url',
    'doc_url': 'https://doc.url',
    'source_git_url': 'http://git.url',
    'license': 'LICENSE',
    'license_url': 'http://license.url',
    'name': u'test-app-package-icon',
    'summary': u'',
    }

app_expected_version_data = {
    'source_git_tag': 0.1,
    'description': 'test description',
    'home_page': 'http://home.page',
    'icon': ICON_B64,
    'version': u'0.1',
    }


class Test(unittest.TestCase):

    def test_conda_old(self):
        filename = data_path('conda_gc_test-1.2.1-py27_3.tar.bz2')
        with open(filename, 'rb') as fd:
            package_data, version_data, file_data = conda.inspect_conda_package(filename, fd)

        self.assertEqual(expected_package_data, package_data)
        self.assertEqual(expected_version_data_121, version_data)
        self.assertEqual(expected_file_data_121, file_data)

    def test_conda(self):
        filename = data_path('conda_gc_test-2.2.1-py27_3.tar.bz2')
        with open(filename, 'rb') as fd:
            package_data, version_data, file_data = conda.inspect_conda_package(filename, fd)

        self.assertEqual(expected_package_data, package_data)
        self.assertEqual(expected_version_data_221, version_data)
        self.assertEqual(expected_file_data_221, file_data)

    def test_conda_app_image(self):
        filename = data_path('test-app-package-icon-0.1-0.tar.bz2')
        with open(filename, 'rb') as fd:
            package_data, version_data, file_data = conda.inspect_conda_package(filename, fd)

        self.assertEqual(app_expected_package_data, package_data)
        self.assertEqual(app_expected_version_data.pop('icon'), version_data.pop('icon'))
        self.assertEqual(app_expected_version_data, version_data)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
