import inspect
import json
import os
from jsonschema import validate
from jsonschema import RefResolver
from jsonschema.exceptions import ValidationError
from ga4gh.htsget.compliance.config import constants as c

class SchemaValidator(object):

    SUCCESS = 1
    FAILURE = -1

    def __init__(self):
        self.schema_file = c.SCHEMA_HTSGET_RESPONSE
        self.schema_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(inspect.getmodule(self).__file__)
            ),
            "schemas"
        )
        self.schema_path = os.path.join(self.schema_dir, self.schema_file)
        self.resolver = RefResolver('file://{}/'.format(self.schema_dir), None)
        self.schema_json = json.loads(open(self.schema_path, 'r').read())
        
    def validate_instance(self, instance_json):
        # test initialized as passing
        validation_result = {
            "status": SchemaValidator.SUCCESS,
            "exception_class": "",
            "message": ""
        }

        try:
            # api method to compare json instance to the schema
            validate(instance=instance_json, schema=self.schema_json,
                     resolver=self.resolver)

        except ValidationError as e:
            # if the api method raises an error, the result dictionary set
            # to include failure status and error message
            validation_result["status"] = SchemaValidator.FAILURE
            validation_result["exception_class"] = str(e.__class__.__name__)
            validation_result["message"] = e.message

        return validation_result

        
        