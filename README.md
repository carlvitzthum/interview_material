# interview_material

This is some dummy code for reading object schemas (sort of like JSON-ld) for different item types from s3 and then traversing given metadata using those schemas. An example schema:

```
### User.json

{
    "@type": "Person",
    "type": "object",
    "properties": {
        "@id": {
            "description": "path to resource"
            "type": "string"
        },
        "name": {
            "type": "string"
        },
        "friends": {
            "type": "array",
            "items": {
                "type": "string",
                "linkTo": "Person"
            }
        },
        "car_owned": {
            "type": "object",
            "properties": {
                "years_owned": {
                    "type": "int"
                } ,
                "car": {
                    "type": "string",
                    "linkTo": "Car"
                }
            }
        }
    }
}
```

Some example data:

```
{
    "@id": "/person/bob/"
    "@type": "Person",
    "name": "Bob",
    "friends": ["/person/joe/", "/person/sally/"],
    "car_owned": {"years_owned": 5, "car": "/car/ford_fusion/"}
}

{
    "@id": "/car/ford_fusion/",
    "@type": "Car",
    "make": "Ford",
    "model": "Fusion",
    "designer": "/person/fabio/"
}
```

Given a starting object, the code in `crawl.py` tries to get the given resource by `@id` and then traverse the object and return the value of a field given by an input path, such as `'car_owned.car.years_owned'` when starting with a `User` object. In the case of an array, return all values of the array (i.e. the result of using `'car_owned.car.designer.friends.name'`).

Assume that you have schemas stored in s3 that are named based off the the `@type` field, for example `User.json`. 
