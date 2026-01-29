import sys

class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}
        self.type_converters = {}
        self.initialize_converters()

    def parse_arguments(self, command_string):
        tokens = command_string.split()
        # skip the command name
        idx = 1
        while idx < len(tokens):
            word = tokens[idx]
            if word.startswith("--"):
                key_value = word[2:]
                if "=" in key_value:
                    key, value = key_value.split("=", 1)
                else:
                    key, value = key_value, ""
                self.arguments[key] = self.convert_type(
                    key, value if value else "1"
                )
                idx += 1
            elif word.startswith("-") and not word.startswith("--"):
                key = word[1:]
                # look ahead to see if next token is a value
                if idx + 1 < len(tokens) and not tokens[idx + 1].startswith("-"):
                    value = tokens[idx + 1]
                    idx += 2
                else:
                    value = "1"
                    idx += 1
                self.arguments[key] = self.convert_type(key, value)
            else:
                idx += 1  # ignore unrecognized tokens

        missing_args = {req for req in self.required if req not in self.arguments}
        return (len(missing_args) == 0, missing_args)

    def get_argument(self, key):
        return self.arguments.get(key, "")

    def add_argument(self, arg, required=False, type="string"):
        if required:
            self.required.add(arg)
        self.types[arg] = type

    def convert_type(self, arg, value):
        if arg not in self.types:
            return value
        converter = self.type_converters.get(self.types[arg])
        if converter:
            return converter(value)
        return value

    def initialize_converters(self):
        def int_converter(value):
            try:
                return str(int(value))
            except Exception:
                return value

        def bool_converter(value):
            if value == "True":
                return "1"
            if value == "False":
                return "0"
            return value

        self.type_converters["int"] = int_converter
        self.type_converters["bool"] = bool_converter
