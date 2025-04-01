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
        self.route_to_operation_id = {}
    
    def operation(self, operation_id):
        def wrapper(func):
            self.operations[operation_id] = func
            return func
        return wrapper
    
    def get_params(self, params_spec, kwargs):
        params = {}
        for param in params_spec:
            if param["in"] == "query":
                params[param["name"]] = request.args.getlist(param["name"])
            elif param["in"] == "path":
                params[param["name"]] = kwargs.get(param["name"])
        return params

    def set_routes(self):
        
        for operation_id, func in self.operations.items():
            path, method, spec = self.find_spec(operation_id)
            if path.find('{') != -1:
                path = path.replace("{", "<").replace("}", ">")
            self.route_to_operation_id[f'{path}:{method}'] = operation_id
            

            def app_exec(*args, **kwargs):
                context = {}
                context["body"] = {}


                operation_id = self.route_to_operation_id[f'{str(request.url_rule)}:{str(request.method).lower()}']
                _, _, spec = self.find_spec(operation_id)

                if request.method == "PUT":
                    schema = spec["requestBody"]["content"]["application/json"]["schema"]
                    try:
                        validate(instance=request.get_json(), schema=schema, resolver=self.resolver)
                        context["body"] = request.get_json()
                    except ValidationError as e:
                        return jsonify({"error": "Validation exception"}), 405
                elif request.method == "POST":
                    if "application/json" in spec["requestBody"]["content"]:
                        schema = spec["requestBody"]["content"]["application/json"]["schema"]
                        try:
                            validate(instance=request.get_json(), schema=schema, resolver=self.resolver)
                            context["body"] = request.get_json()
                        except ValidationError as e:
                            return jsonify({"error": "Invalid input"}), 405
                    elif "application/x-www-form-urlencoded" in spec["requestBody"]["content"]: 
                        schema = spec["requestBody"]["content"]["application/x-www-form-urlencoded"]["schema"]
                        for property in schema["properties"]:
                            context["body"][property] = {request.form.get(property)}
                            # print(f'Add property: {property}->{context["body"][property]}')
                            # print(f'Test {context["body"][property]} in schema: {schema["properties"][property]}')
                    
                    if "parameters" in spec:
                        context["body"] = context["body"] | self.get_params(spec["parameters"], kwargs)


                elif request.method == "GET" or request.method == "DELETE":
                    if "parameters" in spec:
                        context["body"] = context["body"] | self.get_params(spec["parameters"], kwargs)


                
                return self.operations[operation_id](context)
            app_exec.__name__ = f"{operation_id}_{method}"
            
            self.app.add_url_rule(path, methods=[method], view_func=app_exec)
            # print(f"Registered route: {method} {path} -> {app_exec.__name__}")

            
  
    def find_spec(self, operation_id):
        for page, methods in self.openAPI_spec["paths"].items():
            for method, spec in methods.items():
                if spec["operationId"] == operation_id:
                    return page, method, spec
    