from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags = ['Auth'])

@router.post('/login', response_model = schemas.Token)
def login(user_creds : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid Credentials')

    if not utils.verify_pass(user_creds.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Invalid Credentials')

    # Create Access Token
    access_token = oauth2.create_access_token(data = {'user_id' : user.id})

    # Return Access Token
    return {'access_token' : access_token, 'token_type' : 'bearer'}
