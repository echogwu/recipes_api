import boto3
from boto3.dynamodb.conditions import Attr
from constants import DYNAMODB_ACCESS_KEY, DYNAMODB_SECRET_KEY, RECIPE_TABLE_NAME

# Get the service resource.
dynamodb = boto3.resource('dynamodb',
                          region_name='us-west-2',
                          aws_access_key_id=DYNAMODB_ACCESS_KEY,
                          aws_secret_access_key=DYNAMODB_SECRET_KEY)

all_dynamodb_table_names = [table.name for table in dynamodb.tables.all()]
print(all_dynamodb_table_names)

if RECIPE_TABLE_NAME not in all_dynamodb_table_names:
    # Create the DynamoDB table.
    table = dynamodb.create_table(TableName=RECIPE_TABLE_NAME,
                                  AttributeDefinitions=[{
                                      'AttributeName': 'recipeId',
                                      'AttributeType': 'S'
                                  }, {
                                      'AttributeName': 'name',
                                      'AttributeType': 'S'
                                  }],
                                  KeySchema=[
                                      {
                                          'AttributeName': 'recipeId',
                                          'KeyType': 'HASH'
                                      },
                                  ],
                                  GlobalSecondaryIndexes=[
                                      {
                                          'IndexName':
                                          'nameIndex',
                                          'KeySchema': [
                                              {
                                                  'AttributeName': 'name',
                                                  'KeyType': 'HASH'
                                              },
                                          ],
                                          'Projection': {
                                              'ProjectionType': 'ALL',
                                          },
                                          'ProvisionedThroughput': {
                                              'ReadCapacityUnits': 10,
                                              'WriteCapacityUnits': 10
                                          }
                                      },
                                  ],
                                  ProvisionedThroughput={
                                      'ReadCapacityUnits': 10,
                                      'WriteCapacityUnits': 10
                                  })

    # Wait until the table exists.
    table.wait_until_exists()

    # Print out some data about the table.
    print(table.item_count)

table = dynamodb.Table(RECIPE_TABLE_NAME)
response = table.scan(Limit=10,
                      Select='ALL_ATTRIBUTES',
                      ReturnConsumedCapacity='TOTAL',
                      FilterExpression=Attr('name').contains('saag'),
                      ConsistentRead=True)

response = table.scan(Limit=10,
                      Select='ALL_ATTRIBUTES',
                      ReturnConsumedCapacity='TOTAL',
                      FilterExpression=Attr('ingredients').contains("garlic"),
                      ConsistentRead=True)

print(response)
