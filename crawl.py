import boto3
import requests

S3_BUCKET = 'xxxxx'
SERVER = 'http://localhost:9999'
client = boto3.client('s3')


def get_schema_from_s3(schema_name):
    """
    Returns a JSON schema read from an s3 object

    Args:
        schema_name (str): name of schema in s3

    Returns:
        dict: schema
    """
    try:
        response = self.client.get_object(Bucket=S3_BUCKET, Key=schema_name)
        return json.loads(response['Body'].read())
    except Exception as exc:
        print('Error!')
        raise exc


def get_object(obj_id):
    """
    Get an object with given obj_id via requests

    Args:
        obj_id (str): @id value for the object

    Returns:
        dict: object
    """
    resp = requests.get(SERVER + obj_id)
    return resp.json()


def crawl_object(obj_id, path):
    """
    Given an obj_id (@id) and nested path for a field to find, use the object
    schemas and return the desired value of field.

    When encountering arrays, return all values of the array

    Args:
        obj_id (str): @id value for the object
        path(str): path to desired field, separated by dots

    Returns:
        found value for nested field

    Raises:
        Exception: if path contains a field not in schema
    """
    # initialize
    obj = get_object(obj_id)
    obj_schema = get_schema_from_s3(obj['@type'] + '.json')
    found = obj
    found_schema = obj_schema

    # loop through the path, split by dots
    for split_path in path.split('.'):

        # get next level field
        found = obj[split_path]

        # finished?
        if path.split('.').index(split_path) == len(path):
            break

        # handle arrays in schema
        if found_schema['type'] == 'array':
            found_schema = found_schema['items']
            found = found[0]
        # handle objects in schema
        if found_schema['type'] == 'object':
            found_schema = found_schema['properties']
        # get next level schema
        found_schema = found_schema[split_path]

        # see if field is a linkTo and request new object if needed
        if 'linkTo' in found_schema:
            found = get_object(found)
            found_schema = get_schema_from_s3(found_schema['linkTo'] + '.json')

    return found
