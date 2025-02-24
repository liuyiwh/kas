# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2025
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import os
import subprocess
import re
import json


class Diff:
    name = 'diff'
    helpmsg = (
        'Show the update of the dependencies of the current project'
    )

    @classmethod
    def setup_parser(cls, parser):
        pass

    def extract_updates(self, result_string):
        def find_matching_brace(s, start):
            depth = 0
            for i, char in enumerate(s[start:], start=start):
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        return i
            return -1
        
        debug_pos = result_string.find('DEBUG: packageFiles with updates')
        if debug_pos == -1:
            logging.info("The 'DEBUG: packageFiles with updates' section was not found.")
            return []

        # Search for "config" starting from the position of "DEBUG: packageFiles with updates"
        match = re.search(r'"config": \{', result_string[debug_pos:])      

        results = []

        if match:
            start = debug_pos + match.start()
            end = find_matching_brace(result_string, start)

            if end !=-1:
                config_json_str = result_string[start:end+1]

                try:

                    data = json.loads("{"+config_json_str+"}")
                    
                    for config_type in data["config"]:
                        for item in data["config"][config_type]:
                            package_file = item["packageFile"]
                            for dep in item["deps"]:
                                if dep["updates"]:
                                    dep_name = dep["depName"]
                                    current_version = dep["currentVersion"]
                                    new_version = dep["updates"][0]["newVersion"]
                                    results.append({
                                        "packageFile": package_file,
                                        "depName": dep_name,
                                        "currentVersion": current_version,
                                        "newVersion": new_version
                                    })
                except json.JSONDecodeError as e:
                    logging.error(f"JSON parsing error: {e}")
        else:
                logging.info("The JSON data for the 'config' section was not found.")
        return results

    def run(self, args):

        env = os.environ.copy()
        env['LOG_LEVEL'] = 'debug' 

        command = [
            'renovate',
            '--platform=local'
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True, env=env)
            updates = self.extract_updates(result.stdout)
            
            for update in updates:
                logging.info(f"Package File: {update['packageFile']}, Dep Name: {update['depName']}, Current Version: {update['currentVersion']}, New Version: {update['newVersion']}")

        except subprocess.CalledProcessError as e:

            logging.error(f"Error running renovate: {e}")
            logging.error(e.stderr)


__KAS_PLUGINS__ = [Diff]

