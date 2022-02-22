# Summary
This file is aimed to document the final data structure returned by each API endpoint.

# Endpoint Request and Response Example

## get all recipes
Method: GET
URL: `http://127.0.0.1:5000/recipes`
Response:

    {
      "recipes":[
          {
            "id":1,
            "name":"saag",
            "description": "This recipe is all about work in parallel",

            // default unit is minute, if it goes over 1 hour, front end should convert it into x hour(s) y minute(s)
            "active_time":10,
            "total_time":20,

            // "tags" might be null
            "tags":[
                "non_dairy",
                "non_wheat",
                "comfort_food"
            ],

            // "ingredients" might be null. But if it is not, "unit" is required for each ingredient but "prep" is optional 
            "ingredients":[
              {
                "name":"celery",
                "quantity":1,
                "unit":"cup",
                "prep":"cut into nail size pieces"
              },
              {
                "name":"spinach",
                "quantity":5,
                "unit":"cup"
              }
            ],

            // "instructions" might be null
            "instructions":[
                "step 1 instruction",
                "step 2 instruction",
                "step 3 instruction"
            ]
          },
          {
            "id": 2,
            ...
          }
      ]
    }


## get recipes by tags
Method: GET
URL: http://127.0.0.1:5000/recipes?tags=avery_safe&comfort_food
Response: same as responses from [above](#get-all-recipes) url

## get all tags
Method: GET
URL: http://127.0.0.1:5000/recipes/tags
Response:

    {
      "tags": [
        "comfort_food",
        "easy_make",
        "non_wheat",
        "non_dairy",
        "avery_safe"
      ]
    }

## create a new recipe
Method: POST
URL: http://127.0.0.1:5000/recipes
Request Body:

    {
        "name": "saag",
        "active_time": 10,
        "total_time": 20,
        "ingredients": "carrots",
        "instructions": "instructions placeholder"
    }
Response: 

    {
      "id":1,
      "name":"saag",
      "description": "This recipe is all about work in parallel",

      // default unit is minute, if it goes over 1 hour, front end should convert it into x hour(s) y minute(s)
      "active_time":10,
      "total_time":20,

      // "tags" might be null
      "tags":[
          "non_dairy",
          "non_wheat",
          "comfort_food"
      ],

      // "ingredients" might be null. But if it is not, "unit" is required for each ingredient but "prep" is optional 
      "ingredients":[
        {
          "name":"celery",
          "quantity":1,
          "unit":"cup",
          "prep":"cut into nail size pieces"
        },
        {
          "name":"spinach",
          "quantity":5,
          "unit":"cup"
        }
      ],

      // "instructions" might be null
      "instructions":[
          "step 1 instruction",
          "step 2 instruction",
          "step 3 instruction"
      ]
    }

## update a recipe
Method: PUT
URL: http://127.0.0.1:5000/recipes
Request Body:

    {
      "id":1,
      "name":"saag",
      "description": "This recipe is all about work in parallel",

      // default unit is minute, if it goes over 1 hour, front end should convert it into x hour(s) y minute(s)
      "active_time":10,
      "total_time":20,

      // "tags" might be null
      "tags":[
          "non_dairy",
          "non_wheat",
          "comfort_food"
      ],

      // "ingredients" might be null. But if it is not, "unit" is required for each ingredient but "prep" is optional 
      "ingredients":[
        {
          "name":"celery",
          "quantity":1,
          "unit":"cup",
          "prep":"cut into nail size pieces"
        },
        {
          "name":"spinach",
          "quantity":5,
          "unit":"cup"
        }
      ],

      // "instructions" might be null
      "instructions":[
          "step 1 instruction",
          "step 2 instruction",
          "step 3 instruction"
      ]
    }

Response:
None
