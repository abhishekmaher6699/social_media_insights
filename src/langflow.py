import requests
import re
import json

def hit_api(input_string):
    url = "https://api.langflow.astra.datastax.com/lf/db79bb5b-44db-4f88-8bd6-aa4f83e3dca1/api/v1/run/social-agent?stream=false"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer AstraCS:rHywnFslQrAEQsiDtptCZdaA:2f197270a75011e755177ada6e494daac93710a92ff6411db5c0d4cb57ee4c58"
    }
    data = {
        "input_value": input_string,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "ChatOutput-GuFRJ": {},
            "File-u5zUE": {},
            "SplitText-yWxWs": {},
            "AstraDB-AL2RZ": {},
            "GoogleGenerativeAIModel-8F8kx": {},
            "TextInput-Wbcgm": {},
            "ParseData-8RPWH": {},
            "Prompt-15S5X": {},
            "ChatInput-ggXWT": {}
        }
    }

    print("fetching data from langflow")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # print("Response:", response.json())
        return response.json()
        pass
    else:
        print(f"Error: {response.status_code}", response.text)


def evaluate_arithmetic_expressions(json_str):
    def replace_expression(match):
        expr = match.group(1)
        try:
            # Only allow basic arithmetic operations
            if not re.match(r'^[\d\s+*/()\.-]+$', expr):
                return match.group(0)
            
            # Remove any extra whitespace and ensure proper multiplication syntax
            cleaned_expr = re.sub(r'\s+', '', expr)
            
            result = eval(cleaned_expr)
            # Format float results to 2 decimal places
            return str(round(result, 2)) if isinstance(result, float) else str(result)
        except:
            return match.group(0)
    
    # Updated pattern to better handle multiplication and nested parentheses
    pattern = r'((?:\()*\d+(?:\.\d+)?(?:\s*[+\-*/]\s*(?:\()*\d+(?:\.\d+)?(?:\))*)+(?:\s*\/\s*\d+(?:\.\d+)?)?)'
    return re.sub(pattern, replace_expression, json_str)

def parse_langflow_response(input_string):

    api_response = hit_api(input_string)
    try:
        # Convert string to dict if needed
        if isinstance(api_response, str):
            api_response = json.loads(api_response)
            print("parsing data")
        
        # Navigate to the model's output
        model_output = (api_response.get('outputs', [])[0]
                       .get('outputs', [])[0]
                       .get('results', {})
                       .get('message', {})
                       .get('text', ''))
        
        # Extract the JSON string from the code block
        json_match = re.search(r'```json\n(.*?)\n```', model_output, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON data found in code block")
        
        json_str = json_match.group(1)
        
        # Evaluate arithmetic expressions
        json_str = evaluate_arithmetic_expressions(json_str)
        
        # Parse the cleaned JSON string
        try:
            parsed_data = json.loads(json_str)
            return parsed_data
        except json.JSONDecodeError as e:
            print(f"Debug - JSON string after evaluation: {json_str}")
            raise ValueError(f"JSON parsing error: {str(e)}")
            
    except Exception as e:
        raise ValueError(f"Failed to parse Langflow response: {str(e)}")

def debug_print_response(api_response):
    """Helper function to debug the API response structure"""
    try:
        if isinstance(api_response, str):
            api_response = json.loads(api_response)
            
        print("\nResponse structure:")
        def print_dict(d, indent=0):
            for key, value in d.items():
                print(" " * indent + str(key) + ":")
                if isinstance(value, dict):
                    print_dict(value, indent + 2)
                else:
                    print(" " * (indent + 2) + str(type(value)))
        
    except Exception as e:
        print(f"Error in debug printing: {str(e)}")

# data  = parse_langflow_response(response.json())

def get_data(input_types):
    text = ", ".join(input_types)
    data = parse_langflow_response(text)
    return data