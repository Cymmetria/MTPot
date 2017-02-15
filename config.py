###
# MTPot is a simple open source honeypot, released under the MIT license for the use of the community.
#
# Cymmetria Research, 2016.
# http://www.cymmetria.com/
#
# Please consider trying out the MazeRunner Community Edition, the free version of our cyber deception platform.
#
# Written by: Itamar Sher (@itamar_sher), Dean Sysman (@DeanSysman), Imri Goldberg (@lorgandon)
# Contact: research@cymmetria.com
###
import json

MANDATORY_FIELDS = ["port", "commands", "ddos_name", "ip", "pool"]
OPTIONAL_FIELDS = ["syslog_address", "syslog_port", "syslog_protocol", "timeout", "overwrite_commands"]

class InvalidConfiguration(Exception):
    pass

class MissingConfigField(Exception):
    pass

class HoneyConfig(object):
    def __init__(self, conf_path):
        with open(conf_path, "rb") as config_file:
            self.config = json.load(config_file)
        self.validate_config()

    def __getattr__(self, name):
        try:
            return self.config[name]
        except KeyError:
            raise MissingConfigField("{} is missing from the configuration".format(name))

    def validate_config(self):
        missing_fields = []
        for f in MANDATORY_FIELDS:
            if not self.config.has_key(f):
                missing_fields.append(f)
        if missing_fields:
            raise InvalidConfiguration("Missing fields in the configuration: {}".format(",".join(missing_fields)))
