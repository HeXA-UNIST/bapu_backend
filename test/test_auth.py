import os
import pytest
from flask import session
from app import socketio, app
from src.middleware import db
from src.model import Auth, User
from src.utils import AuthManager, AuthState

# global test variable
email = "rzbsys@unist.ac.kr"
otp_code = "132435"
nickname = "MeLU"

def create_fake_auth(app):
    with app.app_context():
        Auth().create(email, otp_code)

# Write email in user db
def create_fake_user(app):
    with app.app_context():
        User().create(email, nickname)

def create_user_request_environment(api_client, create_auth : bool = True, create_user : bool = True):
    if create_auth:
        create_fake_auth(app)
    if create_user:
        create_fake_user(app)
    with api_client.session_transaction() as session:
        auth_manager = AuthManager(session)
        auth_manager.update_auth_state(AuthState.OTP_VERIFY)
        auth_manager.enroll_user_info(User(email=email))

def create_user_login_but_not_registered_environment(api_client):
    # create_fake_user(app)
    with api_client.session_transaction() as session:
        auth_manager = AuthManager(session)
        auth_manager.update_auth_state(AuthState.NEED_REGISTER)
        auth_manager.enroll_user_info(User(email=email))

@pytest.fixture(scope="session")
def api():
    app.config["TESTING"] = True
    socketio.test_client(app)
    api_client = app.test_client()
    socketio_client = socketio.test_client(app)
    return api_client, socketio_client

@pytest.fixture(scope="function", autouse=True)
def reset_db(api):
    api_client, socketio_client = api
    with app.app_context():
        db.drop_all()
        db.create_all()
    with api_client.session_transaction() as session:
        session.clear()


# 1. request_verify
def test_valid_email(api):
    api_client, socketio_client = api
    email = "rzbsys@unist.ac.kr"
    res = api_client.post("/api/taxi_auth/request_verify", json={"email": email})
    assert res.status_code == 200

    with app.app_context():
        auth = Auth().select_by_email(email)
        assert auth is not None
        assert auth.email == email

def test_invalid_email(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/request_verify", json={"email": "not valid email"})
    assert res.status_code == 400

def test_blank_email(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/request_verify", json={"email": ""})
    assert res.status_code == 400

def test_not_unist_email(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/request_verify", json={"email": "rzbsys@notunist.ac.kr"})
    assert res.status_code == 400

def test_no_key_in_json(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/request_verify", json={"notemail": "rzbsys@unist.ac.kr"})
    assert res.status_code == 400


# 2. check_verify
# Before start, write data in db

# Failure verifying
def test_wrong_otp(api):
    create_fake_auth(app)
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/check_verify", json={"email": email, "otp": "wrong-otp"})
    assert res.status_code == 401

def test_blank_email_in_verify(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/check_verify", json={"email": "", "otp": otp_code})
    assert res.status_code == 401

def test_blank_otp(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/check_verify", json={"email": email, "otp": ""})
    assert res.status_code == 401

def test_not_enough_keys(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/check_verify", json={"otp": otp_code})
    assert res.status_code == 401
    res = api_client.post("/api/taxi_auth/check_verify", json={"email" : email})
    assert res.status_code == 400

# Success verifying
# Not registered email
def test_valid_otp_but_not_registered(api):
    api_client, socketio_client = api

    create_user_request_environment(api_client, create_user=False)

    res = api_client.post("/api/taxi_auth/check_verify", json={"email": email, "otp": otp_code})
    assert res.status_code == 200
    assert res.get_json().get('registered') == False

    # Should not be logged in
    with api_client.session_transaction() as session:
        assert session.get('is_authenticated') is None
        assert session.get('email') is None


# Now, registered email
def test_valid_otp_and_registered(api):
    api_client, socketio_client = api
    create_user_request_environment(api_client)

    res = api_client.post("/api/taxi_auth/check_verify", json={"otp": otp_code})
    assert res.status_code == 200, res.get_json()
    assert res.get_json().get('registered') == True

    # Should be logged in
    with api_client.session_transaction() as session:
        auth_manager = AuthManager(session)
        assert auth_manager.is_authenticated
        assert auth_manager.email == email

# 3. register
def test_blank_email_in_register(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/register", json={"email": "", "nickname": nickname})
    assert res.status_code == 401

def test_blank_nickname_in_register(api):
    api_client, socketio_client = api
    res = api_client.post("/api/taxi_auth/register", json={"email": email, "nickname": ""})
    assert res.status_code == 401

def test_duplicate_in_register(api):
    api_client, socketio_client = api
    create_user_request_environment(api_client)

    # duplicate email
    res = api_client.post("/api/taxi_auth/register", json={"email": email, "nickname": "NONONO"})
    assert res.status_code == 401
    #duplicate nickname
    res = api_client.post("/api/taxi_auth/register", json={"email": "unknown@unist.ac.kr", "nickname": nickname})
    assert res.status_code == 401

def test_check_login_in_register(api):
    api_client, socketio_client = api
    create_user_login_but_not_registered_environment(api_client)
    res = api_client.post('/api/taxi_auth/register', json={"email": email, "nickname": nickname})
    assert res.status_code == 200, res.get_json()

    with api_client.session_transaction() as session:
        assert session.get('user_info') is not None
        # assert session.get('is_authenticated') == 'True'
        # assert session.get('email') == email


"""
1. User가 email로 otp 보내달라 요청을 날림
    a. 메일 형식이 아님
    b. 유니스트 메일이 아님
    c. request 양식을 안지킴 {"wad" : "adwad"}

2. User가 otp를 보냄
    a. 1번 과정 없이 여기로 요청을 날림
    b. otp코드가 안맞음
    c. request 양식을 안지킴 {"wad" : "adwad"}
    d. otp 요청을 날린뒤 10분 이상 경과
    e. 이미 만료된 otp로 요청
    f. 4번이상 otp를 틀림

3. opt인증이 끝나면 회원가입
    a. request 양식을 안지킴 {"wad" : "adwad"}
    b. 닉네임 길이 제한 test
    c. 닉네임 중복
    d. register되었지만, 여기로 요청을 날림
    
4. 전부 정상적으로 동작할때
    a. 1, 2, 3번 과정으로 회원가입 후 재로그인
    b. 로그아웃 테스트
"""