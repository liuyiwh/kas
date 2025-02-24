import pytest
from unittest.mock import patch, mock_open
import json
import re
import os
import sys

plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'kas', 'plugins'))

sys.path.append(plugins_dir)

# Assuming the extract_updates function is defined in the Diff class in the diff module
from diff import Diff




@pytest.fixture
def mock_file_content():
    return '''DEBUG: packageFiles with updates (repository=local)
       "config": {
         "dockerfile": [
           {
             "deps": [
               {
                 "depName": "alpine",
                 "packageName": "alpine",
                 "currentValue": "3.13.1",
                 "replaceString": "alpine:3.13.1",
                 "autoReplaceStringTemplate": "{{depName}}{{#if newValue}}:{{newValue}}{{/if}}{{#if newDigest}}@{{newDigest}}{{/if}}",
                 "datasource": "docker",
                 "depType": "final",
                 "updates": [
                   {
                     "bucket": "non-major",
                     "newVersion": "3.21.3",
                     "newValue": "3.21.3",
                     "releaseTimestamp": "2025-02-14T19:25:28.998Z",
                     "newVersionAgeInDays": 8,
                     "newMajor": 3,
                     "newMinor": 21,
                     "newPatch": 3,
                     "updateType": "minor",
                     "libYears": 4.046029154394978,
                     "branchName": "renovate/alpine-3.x"
                   }
                 ],
                 "versioning": "docker",
                 "warnings": [],
                 "registryUrl": "https://index.docker.io",
                 "lookupName": "library/alpine",
                 "currentVersion": "3.13.1",
                 "currentVersionTimestamp": "2021-01-29T00:12:33.585Z",
                 "currentVersionAgeInDays": 1486,
                 "isSingleVersion": true,
                 "fixedVersion": "3.13.1"
               }
             ],
             "packageFile": "bitbake/contrib/hashserv/Dockerfile"
           },
           {
             "deps": [
               {
                 "depName": "alpine",
                 "packageName": "alpine",
                 "currentValue": "3.14.4",
                 "replaceString": "alpine:3.14.4",
                 "autoReplaceStringTemplate": "{{depName}}{{#if newValue}}:{{newValue}}{{/if}}{{#if newDigest}}@{{newDigest}}{{/if}}",
                 "datasource": "docker",
                 "depType": "final",
                 "updates": [
                   {
                     "bucket": "non-major",
                     "newVersion": "3.21.3",
                     "newValue": "3.21.3",
                     "releaseTimestamp": "2025-02-14T19:25:28.998Z",
                     "newVersionAgeInDays": 8,
                     "newMajor": 3,
                     "newMinor": 21,
                     "newPatch": 3,
                     "updateType": "minor",
                     "libYears": 2.89909595728691,
                     "branchName": "renovate/alpine-3.x"
                   }
                 ],
                 "versioning": "docker",
                 "warnings": [],
                 "registryUrl": "https://index.docker.io",
                 "lookupName": "library/alpine",
                 "currentVersion": "3.14.4",
                 "currentVersionTimestamp": "2022-03-23T15:20:38.889Z",
                 "currentVersionAgeInDays": 1067,
                 "isSingleVersion": true,
                 "fixedVersion": "3.14.4"
               }
             ],
             "packageFile": "bitbake/contrib/prserv/Dockerfile"
           },
           {
             "deps": [
               {
                 "depName": "ghcr.io/siemens/kas/kas-isar",
                 "packageName": "ghcr.io/siemens/kas/kas-isar",
                 "currentValue": "<version>",
                 "replaceString": "ghcr.io/siemens/kas/kas-isar:<version>",
                 "autoReplaceStringTemplate": "{{depName}}{{#if newValue}}:{{newValue}}{{/if}}{{#if newDigest}}@{{newDigest}}{{/if}}",
                 "datasource": "docker",
                 "depType": "final",
                 "updates": [],
                 "versioning": "docker",
                 "warnings": [],
                 "skipReason": "invalid-value"
               }
             ],
             "packageFile": "testsuite/dockerdata/Dockerfile"
           }
         ],
         "gitlabci": [
           {
             "packageFile": ".gitlab-ci.yml",
             "deps": [
               {
                 "depName": "ghcr.io/siemens/kas/kas-isar",
                 "packageName": "ghcr.io/siemens/kas/kas-isar",
                 "currentValue": "3.2.3",
                 "replaceString": "ghcr.io/siemens/kas/kas-isar:3.2.3",
                 "autoReplaceStringTemplate": "{{depName}}{{#if newValue}}:{{newValue}}{{/if}}{{#if newDigest}}@{{newDigest}}{{/if}}",
                 "datasource": "docker",
                 "depType": "image",
                 "updates": [
                   {
                     "bucket": "major",
                     "newVersion": "4.3.2",
                     "newValue": "4.3.2",
                     "newMajor": 4,
                     "newMinor": 3,
                     "newPatch": 2,
                     "updateType": "major",
                     "branchName": "renovate/ghcr.io-siemens-kas-kas-isar-4.x"
                   }
                 ],
                 "versioning": "docker",
                 "warnings": [],
                 "sourceUrl": "https://github.com/siemens/kas",
                 "registryUrl": "https://ghcr.io",
                 "lookupName": "siemens/kas/kas-isar",
                 "currentVersion": "3.2.3",
                 "isSingleVersion": true,
                 "fixedVersion": "3.2.3"
               },
               {
                 "depName": "ghcr.io/ilbers/docker-isar",
                 "packageName": "ghcr.io/ilbers/docker-isar",
                 "currentValue": "3.2.3",
                 "replaceString": "ghcr.io/ilbers/docker-isar:3.2.3",
                 "autoReplaceStringTemplate": "{{depName}}{{#if newValue}}:{{newValue}}{{/if}}{{#if newDigest}}@{{newDigest}}{{/if}}",
                 "datasource": "docker",
                 "depType": "image",
                 "updates": [],
                 "versioning": "docker",
                 "warnings": [],
                 "registryUrl": "https://ghcr.io",
                 "lookupName": "ilbers/docker-isar",
                 "currentVersion": "3.2.3",
                 "fixedVersion": "3.2.3"
               }
             ]
           }
         ],
         "pip_requirements": [
           {
             "deps": [
               {
                 "depName": "Django",
                 "packageName": "django",
                 "currentValue": ">4.2,<4.3",
                 "datasource": "pypi",
                 "updates": [
                   {
                     "bucket": "major",
                     "newVersion": "5.1.6",
                     "newValue": ">5.1,<5.2",
                     "releaseTimestamp": "2025-02-05T14:16:00.000Z",
                     "newVersionAgeInDays": 17,
                     "newMajor": 5,
                     "newMinor": 1,
                     "newPatch": 6,
                     "updateType": "major",
                     "isRange": true,
                     "libYears": 0.000026889903602232368,
                     "branchName": "renovate/django-5.x"
                   }
                 ],
                 "versioning": "pep440",
                 "warnings": [],
                 "sourceUrl": "https://github.com/django/django",
                 "registryUrl": "https://pypi.org/pypi",
                 "changelogUrl": "https://docs.djangoproject.com/en/stable/releases/",
                 "currentVersion": "4.2.19",
                 "currentVersionTimestamp": "2025-02-05T14:01:52.000Z",
                 "currentVersionAgeInDays": 17,
                 "isSingleVersion": false
               },
               {
                 "depName": "beautifulsoup4",
                 "packageName": "beautifulsoup4",
                 "currentValue": ">=4.4.0",
                 "datasource": "pypi",
                 "updates": [],
                 "versioning": "pep440",
                 "warnings": [],
                 "registryUrl": "https://pypi.org/pypi",
                 "changelogUrl": "https://git.launchpad.net/beautifulsoup/tree/CHANGELOG",
                 "currentVersion": "4.13.3",
                 "currentVersionTimestamp": "2025-02-04T20:05:03.000Z",
                 "currentVersionAgeInDays": 18
               },
               {
                 "depName": "pytz",
                 "packageName": "pytz",
                 "datasource": "pypi",
                 "updates": [],
                 "versioning": "pep440",
                 "warnings": [],
                 "skipReason": "invalid-value"
               },
               {
                 "depName": "django-log-viewer",
                 "packageName": "django-log-viewer",
                 "currentValue": "==1.1.7",
                 "datasource": "pypi",
                 "currentVersion": "1.1.7",
                 "updates": [],
                 "versioning": "pep440",
                 "warnings": [],
                 "sourceUrl": "https://github.com/agusmakmun/django-log-viewer",
                 "registryUrl": "https://pypi.org/pypi",
                 "currentVersionTimestamp": "2023-01-27T14:07:15.000Z",
                 "currentVersionAgeInDays": 757,
                 "fixedVersion": "1.1.7"
               }
             ],
             "packageFile": "bitbake/toaster-requirements.txt"
           }
         ]
       }
    '''

def test_extract_updates(mock_file_content):
    updates = Diff().extract_updates(mock_file_content)
    print(updates)
    
    expected_updates = [
        {'packageFile': 'bitbake/contrib/hashserv/Dockerfile', 
         'depName': 'alpine', 
         'currentVersion': '3.13.1', 
         'newVersion': '3.21.3'
         },
         {'packageFile': 'bitbake/contrib/prserv/Dockerfile', 
          'depName': 'alpine', 
          'currentVersion': '3.14.4', 
          'newVersion': '3.21.3'
          }, 
          {'packageFile': '.gitlab-ci.yml', 
           'depName': 'ghcr.io/siemens/kas/kas-isar', 
           'currentVersion': '3.2.3', 'newVersion': '4.3.2'
           }, 
           {'packageFile': 'bitbake/toaster-requirements.txt', 
            'depName': 'Django', 'currentVersion': '4.2.19', 'newVersion': '5.1.6'
            }
      ]
    
    assert updates == expected_updates

if __name__ == '__main__':
    pytest.main()