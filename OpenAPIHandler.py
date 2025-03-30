import yaml
from flask import request, jsonify
from jsonschema import validate, ValidationError, RefResolver
from Exceptions import InvalidIDException

class OpenAPIHandler():
    def __init__(self, app, openAPI_path):
        self.app = app
        self.operations = {}
        with open(openAPI_path, "r") as file:
            self.openAPI_spec = yaml.safe_load(file)
        self.resolver = RefResolver.from_schema(self.openAPI_spec)
    
    def operation(self, operation_id):
        def wrapper(func):
            self.operations[operation_id] = func
            return func
        return wrapper
    
    def get_params(self, request, type, name):
        if type == "array":
            return request.args.getlist(name)
        if type == "integer":
            arg = request.args.get(name)
            if not isinstance(arg, int):
                raise InvalidIDException
            return int(arg)

    def set_routes(self):
        for operation_id, func in self.operations.items():
            page, method, spec = self.find_spec(operation_id)
            
            def app_exec(page=page, method=method, spec=spec, func=func):
                if request.method == "PUT":
                    schema = spec["requestBody"]["content"]["application/json"]["schema"]
                    try:
                        # instance=request.get_json()
                        # print(f'instance: {instance}, schema = {schema}')
                        validate(instance=request.get_json(), schema=schema, resolver=self.resolver)
                    except ValidationError as e:
                        return jsonify({"error": "Validation exception"}), 405
                elif request.method == "POST":
                    schema = spec["requestBody"]["content"]["application/json"]["schema"]
                    try: 
                        validate(instance=request.get_json(), schema=schema, resolver=self.resolver)
                    except ValidationError as e:
                        return jsonify({"error": "Invalid input"}), 405
                elif request.method == "GET":
                    # print(spec)
                    schema = spec["parameters"][0]["schema"]
                    # print(f'schema: {schema}')
                    try:
                        params = self.get_params(request, type=schema["type"], name=spec["parameters"][0]["name"])
                    except InvalidIDException as e:
                        return jsonify({"error": "Invalid ID supplied"}), 400

                
                # print(f'request: {request}')
                # print(f'request method: {request.method}')
                # print(f'request args: {request.args}')
                # print(f'request values: {request.values}')
                # print(f'request path: {request.path}')
                # print(f'request url: {request.url}')
                # print(f'request host: {request.host}')
                # print(f'request scheme: {request.scheme}')
                # context = {"body": request.get_json()}
                return func(request)
            app_exec.__name__ = f"{page}_{method}" # Prevent "view function mapping is overwriting an existing endpoint function" error
            self.app.add_url_rule(f"{page}", methods=[method], view_func=app_exec)

  
    def find_spec(self, operation_id):
        for page, methods in self.openAPI_spec["paths"].items():
            for method, spec in methods.items():
                if spec["operationId"] == operation_id:
                    return page, method, spec