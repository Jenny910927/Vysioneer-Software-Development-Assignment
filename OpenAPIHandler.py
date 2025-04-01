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
            # print(f'GET receive param: {param}')
            if param["in"] == "query":
                params[param["name"]] = request.args.getlist(param["name"])
                # context["body"][param["name"]] = request.args.getlist(param["name"])
            elif param["in"] == "path":
                # print(f'kwargs: {kwargs}, param["name"]: {param["name"]}')
                # print(kwargs.get(param["name"]))
                params[param["name"]] = kwargs.get(param["name"])
        return params

    def set_routes(self):
        
        

        for operation_id, func in self.operations.items():
            path, method, spec = self.find_spec(operation_id)
            if path.find('{') != -1:
                path = path.replace("{", "<").replace("}", ">")
                # path = path.replace("petId", "int:petId")
            self.route_to_operation_id[f'{path}:{method}'] = operation_id
            print(f'match route to operation: {path}:{method} = {operation_id}')
            

            print(f'Set route for {path} method: {method}, spec: {spec}, url: {path}')
            def app_exec(*args, **kwargs):
            # def app_exec(page=page, method=method, spec=spec, func=func):
                context = {}
                context["body"] = {}
                print(f'request: {request}')
                print(f'request method: {request.method}')
                print(f'request args: {request.args}')
                print(f'request values: {request.values}')
                print(f"Matched Rule: {request.url_rule}")
                print(f'request path: {request.path}')
                print(f'request url: {request.url}')


                operation_id = self.route_to_operation_id[f'{str(request.url_rule)}:{str(request.method).lower()}']
                _, _, spec = self.find_spec(operation_id)

                # if path.find('{') != -1:
                #     path = path.replace("{", "<").replace("}", ">")
                #     path = path.replace("petId", "int:petId")

                if request.method == "PUT":
                    schema = spec["requestBody"]["content"]["application/json"]["schema"]
                    try:
                        # instance=request.get_json()
                        # print(f'instance: {instance}, schema = {schema}')
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
                        print(f'schema: {schema}')
                        try: 
                            for property in schema["properties"]:
                                context["body"][property] = {request.form.get(property)}
                                print(f'Add property: {property}->{context["body"][property]}')
                                print(f'Test {context["body"][property]} in schema: {schema["properties"][property]}')
                                # validate(instance=context["body"][property], schema=schema["properties"][property], resolver=self.resolver)
                        except ValidationError as e:
                            return jsonify({"error": "Invalid input"}), 405
                    
                    if "parameters" in spec:
                        context["body"] = context["body"] | self.get_params(spec["parameters"], kwargs)
                    print(f'POST context body: {context["body"]}')


                elif request.method == "GET" or request.method == "DELETE":
                    try:
                        if "parameters" in spec:
                            for param in spec["parameters"]:
                                # print(f'GET receive param: {param}')
                                if param["in"] == "query":
                                    context["body"][param["name"]] = request.args.getlist(param["name"])
                                elif param["in"] == "path":
                                    print(f'kwargs: {kwargs}, param["name"]: {param["name"]}')
                                    print(kwargs.get(param["name"]))
                                    context["body"][param["name"]] = kwargs.get(param["name"])
                                
                                print(f'Validate: {context["body"][param["name"]]}, schema: {param["schema"]}')
                                # validate(instance=context["body"][param["name"]], schema=param["schema"], resolver=self.resolver)
                    except ValidationError as e:
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
                
                return self.operations[operation_id](context)
            app_exec.__name__ = f"{operation_id}_{method}"
            
            self.app.add_url_rule(path, methods=[method], view_func=app_exec)
            print(f"Registered route: {method} {path} -> {app_exec.__name__}")

            # print(f"Registered route: {method} {path}")

            # app_exec.__name__ = f"{operation_id}_{method}" # Prevent "view function mapping is overwriting an existing endpoint function" error
            # path = page.replace("{", "<").replace("}", ">")
            # self.app.add_url_rule(f"{path}", methods=[method], view_func=app_exec)
            # print(f'!!! Set path for {path}')
            
  
    def find_spec(self, operation_id):
        for page, methods in self.openAPI_spec["paths"].items():
            for method, spec in methods.items():
                if spec["operationId"] == operation_id:
                    return page, method, spec
    