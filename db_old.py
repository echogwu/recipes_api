from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()
engine = create_engine(
    f"amazondynamodb:///?Access Key={DYNAMODB_ACCESS_KEY}&Secret Key={DYNAMODB_SECRET_KEY}&Domain=amazonaws.com&Region=OREGON"
)
