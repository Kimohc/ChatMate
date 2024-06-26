import models
import ai
from db import engine, SessionLocal
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import uuid
import base64
import io
import random
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


class GebruikerBase(BaseModel):
    e_mail: Union[str, None] = None
    gebruikersnaam: Union[str, None] = None
    wachtwoord: Union[str, None] = None
    foto: Union[str, None] = None
    beschrijving: Union[str, None] = None


class BotsBase(BaseModel):
    bot_naam: str
    bot_foto: str
    bot_beschrijving: str
    bot_oud: str
    bot_geslacht: str
    bot_land: str


class BerichtenBase(BaseModel):
    gesprek_id: Union[int, None] = None
    verstuurder_id: Union[str, None] = None
    bericht: Union[str, None] = None


class GesprekkenBase(BaseModel):
    gebruiker_id: str
    bot_id: str


class Bots_GezienBase(BaseModel):
    gebruiker_id: str
    bot_id: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 0.5

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]


class UserInDB(GebruikerBase):
    user_id: int


def verify_password(plain_wachtwoord, hashed_wachtwoord):
    return pwd_context.verify(plain_wachtwoord, hashed_wachtwoord)


def get_user_by_username(db: Session, gebruikersnaam: str):
    return db.query(models.Gebruiker).filter(models.Gebruiker.gebruikersnaam == gebruikersnaam).first()


def authenticate_user(db: Session, gebruikersnaam: str, wachtwoord: str):
    gebruiker = get_user_by_username(db, gebruikersnaam)
    if not gebruiker:
        return False
    if not verify_password(wachtwoord, gebruiker.wachtwoord):
        return False
    return gebruiker


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        gebruikersnaam: str = payload.get("sub")
        if gebruikersnaam is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db = SessionLocal()
    gebruiker = get_user_by_username(db, gebruikersnaam)
    db.close()
    if gebruiker is None:
        raise credentials_exception
    return gebruiker


@app.post('/gebruiker/', status_code=status.HTTP_201_CREATED)
async def create_user(gebruiker: GebruikerBase, db: db_dependency):
    db_user = models.Gebruiker(**gebruiker.dict())
    db_user.wachtwoord = pwd_context.hash(db_user.wachtwoord)
    db_user.gebruiker_id = uuid.uuid4()

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get('/gebruiker/{gebruiker_id}', status_code=status.HTTP_200_OK)
async def get_user_by_id(gebruiker_id: str, db: db_dependency):
    return db.query(models.Gebruiker).where(models.Gebruiker.gebruiker_id == gebruiker_id).first()


@app.post("/gebruiker/login")
async def login(gebruiker: GebruikerBase):
    db = SessionLocal()
    gebruiker = authenticate_user(db, gebruiker.gebruikersnaam, gebruiker.wachtwoord)
    if not gebruiker:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": gebruiker.gebruikersnaam}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": gebruiker.gebruiker_id,
        "username": gebruiker.gebruikersnaam,
        "password": gebruiker.wachtwoord,
        "beschrijving": gebruiker.beschrijving,
        "e_mail": gebruiker.e_mail
    }


@app.get("/users/me")
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user


@app.get('/refresh')
async def get_new_acces_token(gebruikersnaam: str):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": gebruikersnaam}, expires_delta=access_token_expires)
    return {"access_token": access_token}


@app.delete('/gebruiker/{id}', status_code=status.HTTP_200_OK, )
async def delete_user(id: str, db: db_dependency, current_user: UserInDB = Depends(get_current_user)):
    db.query(models.Gebruiker).where(models.Gebruiker.gebruiker_id == id).delete()
    db.commit()
    return True


@app.post('/gebruiker/image/{id}', status_code=status.HTTP_200_OK)
async def add_foto(id: str, db: db_dependency, file: UploadFile = File(...),
                   current_user: UserInDB = Depends(get_current_user)):
    user_to_upload = db.query(models.Gebruiker).filter(models.Gebruiker.gebruiker_id == id).first()

    if not user_to_upload:
        raise HTTPException(status_code=404, detail="Gebruiker not found")
    if not file:
        return 'test , there is no image'

    file.filename = f"{uuid.uuid4()}.png"
    contents = await file.read()
    file_path = f"images/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(contents)

    # Update the user object
    user_to_upload.foto = file.filename

    db.add(user_to_upload)
    db.commit()
    db.refresh(user_to_upload)

    return {"filename": file.filename, "file_path": file_path}


@app.get('/gebruiker/{id}/image', status_code=status.HTTP_200_OK)
async def get_image_user(id: str, db: db_dependency, current_user: UserInDB = Depends(get_current_user)):
    user = db.query(models.Gebruiker).where(models.Gebruiker.gebruiker_id == id).first()
    foto = user.foto
    path = f'images/{foto}'
    if path == "images/None":
        return
    return FileResponse(path)


@app.patch('/gebruiker/{id}', status_code=status.HTTP_200_OK)
async def update_user(id: str, gebruiker: GebruikerBase, db: db_dependency,
                      current_user: UserInDB = Depends(get_current_user)):
    db_gebruiker = db.query(models.Gebruiker).filter(models.Gebruiker.gebruiker_id == id).first()

    if db_gebruiker is None:
        raise HTTPException(status_code=404, detail="Gebruiker not found")

    update_data = gebruiker.dict()
    for key, value in update_data.items():
        setattr(db_gebruiker, key, value)
    db_gebruiker.wachtwoord = pwd_context.hash(db_gebruiker.wachtwoord)
    db.add(db_gebruiker)
    db.commit()
    db.refresh(db_gebruiker)

    return db_gebruiker


@app.get('/gesprekken/{user_id}', status_code=status.HTTP_200_OK)
async def get_gesprekken(user_id: str, db: db_dependency, current_user: UserInDB = Depends(get_current_user)):
    return db.query(models.Gesprekken).where(models.Gesprekken.gebruiker_id == user_id).all()


@app.post('/gesprek', status_code=status.HTTP_201_CREATED)
async def create_gesprek(gesprek: GesprekkenBase, db: db_dependency,
                         current_user: UserInDB = Depends(get_current_user)):
    db_gesprek = models.Gesprekken(**gesprek.dict())
    db.add(db_gesprek)
    db.commit()
    db.refresh(db_gesprek)
    return db_gesprek


@app.delete('/gesprek/{gesprek_id}', status_code=status.HTTP_200_OK)
async def delete_gesprek(gesprek_id: int, db: db_dependency, current_user: UserInDB = Depends(get_current_user)):
    db.query(models.Gesprekken).where(models.Gesprekken.gesprek_id == gesprek_id).delete()
    db.commit()
    return True


@app.get('/bots', status_code=status.HTTP_200_OK)
async def get_bots(db: db_dependency):
    alle_bots = db.query(models.Bots).all()
    geziene_bots = await get_alle_geziene_bots(db)
    geziene_bots_ids = {bot.bot_id for bot in geziene_bots}
    unseen_bots = [bot for bot in alle_bots if bot.bot_id not in geziene_bots_ids]
    print(f'unseen bots: {len(unseen_bots)}')
    return unseen_bots


@app.get('/randombot', status_code=status.HTTP_200_OK)
async def get_random_bot(db: db_dependency, current_user: UserInDB = Depends(get_current_user)):
    alle_bots = await get_bots(db)
    length = len(alle_bots)
    print(f'length: {length}')
    random_bot_index = random.randint(0, length)
    if length < 1:
        print('geen mensen meer beschikbaar')
        return False
    return alle_bots[random_bot_index]


@app.get('/bot/{bot_id}', status_code=status.HTTP_200_OK)
async def get_bot_by_id(bot_id: str, db: db_dependency):
    return db.query(models.Bots).where(models.Bots.bot_id == bot_id).first()


@app.get('/gesprek/{gebruiker_id}/{bot_id}', status_code=status.HTTP_200_OK)
async def get_gesprek_gebruiker_bot(gebruiker_id: str, bot_id: str, db: db_dependency,
                                    current_user: UserInDB = Depends(get_current_user)):
    bot = await get_bot_by_id(bot_id, db)
    beschrijving = f'You are on a dating app. Your bio is: {bot.bot_beschrijving} Use this information in your answers and remember to mention your name, passions, and interests when appropriate.'
    ai.bot_description = beschrijving
    return db.query(models.Gesprekken).where(models.Gesprekken.gebruiker_id == gebruiker_id) and db.query(
        models.Gesprekken).where(models.Gesprekken.bot_id == bot_id).first()


@app.get('/berichten/{gesprek_id}', status_code=status.HTTP_200_OK)
async def get_berichten_gesprek(gesprek_id: int, db: db_dependency, current_user: UserInDB = Depends(get_current_user)):
    return db.query(models.Berichten).where(models.Berichten.gesprek_id == gesprek_id).all()


@app.post('/berichten/', status_code=status.HTTP_201_CREATED)
async def make_bericht(berichten: BerichtenBase, db: db_dependency, current_user: UserInDB = Depends(get_current_user)):
    db_bericht = models.Berichten(**berichten.dict())
    db.add(db_bericht)
    db.commit()
    db.refresh(db_bericht)
    return {
        "user_bericht": db_bericht,
    }


@app.post('/request/ai', status_code=status.HTTP_200_OK)
async def send_request(berichten: BerichtenBase, current_user: UserInDB = Depends(get_current_user)):
    db_bericht = models.Berichten(**berichten.dict())
    ai_response = ai.send_request_to_ai(db_bericht.bericht)
    return ai_response


@app.delete('/bericht/{bericht_id}', status_code=status.HTTP_200_OK)
async def delete_bericht(bericht_id: int, db: db_dependency, current_user: UserInDB = Depends(get_current_user)):
    db.query(models.Berichten).where(models.Berichten.bericht_id == bericht_id).delete()
    db.commit()
    return True


@app.post('/bots/gezien', status_code=status.HTTP_201_CREATED)
async def bot_is_gezien(db: db_dependency, bot_gezien: Bots_GezienBase,
                        current_user: UserInDB = Depends(get_current_user)):
    db_gezien_bot = models.Bots_Gezien(**bot_gezien.dict())
    db.add(db_gezien_bot)
    db.commit()
    db.refresh(db_gezien_bot)
    return db_gezien_bot


async def get_alle_geziene_bots(db: db_dependency):
    return db.query(models.Bots_Gezien).all()


@app.patch('/bericht/{bericht_id}', status_code=status.HTTP_200_OK)
async def update_bericht(bericht: BerichtenBase, bericht_id: int, db: db_dependency,
                         current_user: UserInDB = Depends(get_current_user)):
    db_bericht = db.query(models.Berichten).filter(models.Berichten.bericht_id == bericht_id).first()

    if db_bericht is None:
        raise HTTPException(status_code=404, detail="Gebruiker not found")

    update_data = bericht.dict()
    for key, value in update_data.items():
        setattr(db_bericht, key, value)

    db.add(db_bericht)
    db.commit()
    db.refresh(db_bericht)

    return db_bericht
