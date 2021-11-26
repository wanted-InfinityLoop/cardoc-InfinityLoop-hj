# 🎊 Wanted X Wecode PreOnBoarding Backend Course | 카닥

원티드 4주차 기업 과제 : Cardoc Corporation Assignment Project
✅ 카닥 기업 과제입니다.

- [카닥 사이트](https://www.cardoc.co.kr/)
- [카닥 채용공고 링크](https://www.wanted.co.kr/wd/57545?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic)

<br>

# 🔖 목차

- [소개]()
- [과제 내용]()
- [기술 환경 및 tools]()
- [모델링 ERD]()
- [API 명세서]()
- [기능 구현 추가설명]()
- [설치 및 실행 방법]()

<br>

# :person_curly_hair:  소개

- 일정 : 2021년 11월 23일 ~ 2021년 11월 26일
- 개별 과제 진행 : [손희정](https://github.com/heejung-gjt) 

<br>


# 📖 과제 내용


> 😁 카닥에서 실제로 사용하는 프레임워크를 토대로 타이어 API를 설계 및 구현합니다.

<br>

- 데이터베이스 환경은 별도로 제공하지 않습니다.
 **RDB중 원하는 방식을 선택**하면 되며, sqlite3 같은 별도의 설치없이 이용 가능한 in-memory DB도 좋으며, 가능하다면 Docker로 준비하셔도 됩니다.  
 
- 단, 결과 제출 시 README.md 파일에 실행 방법을 완벽히 서술하여 DB를 포함하여 전체적인 서버를 구동하는데 문제없도록 해야합니다.

- 데이터베이스 관련처리는 raw query가 아닌 **ORM을 이용하여 구현**합니다.

- Response Codes API를 성공적으로 호출할 경우 200번 코드를 반환하고, 그 외의 경우에는 아래의 코드로 반환합니다.

<br>

### **[기능 개발]**


#### 사용자 생성 API(회원가입/로그인)    
ID/Password로 사용자를 생성하는 API.    
인증 토큰을 발급하고 이후의 API는 인증된 사용자만 호출할 수 있다.


#### 사용자가 소유한 타이어 정보를 저장하는 API   
자동차 차종 ID(trimID)를 이용하여 사용자가 소유한 자동차 정보를 저장한다.    
한 번에 최대 5명까지의 사용자에 대한 요청을 받을 수 있도록 해야한다.


#### 사용자가 소유한 타이어 정보 조회 API     
사용자 ID를 통해서 2번 API에서 저장한 타이어 정보를 조회할 수 있어야 한다.

<br>
<br>

## ➡️ Build(AWS EC2)

API URL : http://52.78.100.243:8000

<br>
<br>

# ⚒️ 기술 환경 및 tools

- Back-End: `Python 3.9.7`, `Django 3.2.9`
- Deploy: AWS `EC2`, `Sqlite3`
- ETC: `Git`, `Github`, `Postman`

<br>
<br>


# 📋 모델링 ERD

![d](https://user-images.githubusercontent.com/64240637/143538061-e5127fb5-07a9-4d0a-b727-f6ab276f2142.png)


<br>
<br>

# 🌲 디렉토리 구조

```
├── config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── CONVENTION.md
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── utils.py
│   ├── validator.py
│   └── views.py
├── manage.py
├── my_settings.py
├── PULL_REQUEST_TEMPLATE.md
├── README.md
├── requirements.txt
├── users
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── cars
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

<br>
<br>

# 🔖 API 명세서

[Postman API Document 보러가기](https://documenter.getpostman.com/view/16088238/UVJbGx4q)

<br>

### 👉 회원가입/로그인

[회원가입]

1. 유저 인증 처리를 위해 회원가입 API
2. 유저의 아이디와 비밀번호를 요청 body에 담으면 가입된다.
3. ID, PWD 타입이 틀릴 경우 에러를 

- Method: POST

```
http://52.78.100.243:8000/user/signup
```

<br>

- parameter : request_body

```
{
    "id": "test7",
    "password": "test2@"
}
```

<br>

- response

```
{
    "message": "SUCCUESS"
}
```

<br>

[로그인]

1. 유저의 아이디와 비밀번호를 통해서 User Auth 검증 한다.
2. 로그인 성공 시, user_id 정보를 담은 access_token을 반환한다.
3. 회원가입 정보와 다를시 에러를 반환한다

- Method: POST

```
http://52.78.100.243:8000/user/signin
```

<br>

- parameter : request_body

```
{
    "id": "test7",
    "password": "test2@"
}
```

<br>

- response

```
{
    "message": "SUCCESS",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdDIifQ.p7zpPEIdG3WIEYJyNaIXLiUqEEYvnkDna75WXtmKtjY"
}
```

<br>

### 👉 유저의 타이어 정보 저장

최대 5명의 유저의 타이어 정보를 저장할 수 있다
(타이어 정보 타입이 {폭}/{편평비}R{18}아닌 정보는 저장되지 않는다)

1. 타이어 정보를 저장할 유저의 id와 trimId를 body에 담아 요청한다
2. 정보 저장 성공시 유저의 타이어 정보에 저장된다
3. 요청을 보내는 유저가 5명을 넘을 시 에러를 반환한다
4. 올바르지 않은 KEY값일 시 에러를 반환한다
5. 회원가입 되어 있지 않은 유저가 존재시 해당 유저를 제외하고 타이어 정보를 저장한다

<br>

- Method: POST

```
http://52.78.100.243:8000/car/tire
```

<br>

- parameter : request_body

```
[
    {
        "id": "test1",
        "trimId": 72
    },
    {
        "id": "test2",
        "trimId": 7000
    },
        {
        "id": "test3",
        "trimId": 30
    },
        {
        "id": "test4",
        "trimId": 9000
    }
]
```

<br>

- response

```
{
    "USER TIRE SAVED": [
        "test1",
        "test2",
        "test3",
        "test4"
    ],
    "USER TIRE UNSAVED": []
}
```

<br>

### 👉 유저의 타이어 정보 조회

1. 타이어 정보를 조회할 유저의 id를 쿼리 스트링으로 전송한다
2. 로그인 한 유저의 토큰값과 조회하려는 유저의 ID값의 정보가 다를 경우 에러를 반환한다
3. 정보를 조회하려는 유저의 타이어 정보가 없을시 에러를 반환합니다
4. 정보 조회 성공시 타이어 정보를 반환한다

<br>

- Method: GET

```
http://52.78.100.243:8000/car/tire?id=test1
```

<br>

- parameter : query string

<br>

- response

```
{
    "test1 TIRE INFORMATION": [
        {
            "name": "리오 SF 전 타이어",
            "width": 175,
            "aspect_ratio": 65,
            "wheel_size": 14
        },
        {
            "name": "리오 SF 전 타이어",
            "width": 175,
            "aspect_ratio": 65,
            "wheel_size": 14
        }
    ]
}
```

<br>

# ➕ 기능 구현 추가설명

### [카닥의 url 통해 데이터 조회]
https://dev.mycar.cardoc.co.kr/v1/trim/{id} 를 통해 trimId에 해당하는 자동차의 정보를 조회한다.    
requests를 사용해 spec → driving → frontTire/rearTire 에서 필요한 타이어 정보를 가져온다.    

이때 __{폭}/{편평비}R{18}__ 포맷의 데이터일 경우만 DB에 저장하기 위해 re를 사용해 데이터를 포맷에 맞게 분리하여 저장한다
(앞에 P가 붙는 형식이 존재해 P를 추가했다)    

```python
car_info   = requests.get(f"https://dev.mycar.cardoc.co.kr/v1/trim/{trim_id}").json()
front_tire = re.split("[P/R]",car_info.get("spec")["driving"]["frontTire"]["value"].replace(" ", ""))
rear_tire  = re.split("[P/R]", car_info.get("spec")["driving"]["rearTire"]["value"].replace(" ", ""))

info_dic = {
    "trim_id"   : trim_id,
    "car_brand" : car_info.get("brandName", None),
    "year_type" : car_info.get("yearType", None),
    "car_name"  : car_info.get("submodelGroupName", None),
    "front_tire": front_tire,
    "rear_tire" : rear_tire
}
```

<br>

### [MTV 디자인 패턴]

> 회원가입/로그인

- request 요청이 들어오면 이에 해당하는 특정 url이 urlConf를 통해 매핑되는 View를 호출한다
- View에서는 요청에 맞게 로직을 실행한다. 이 과정에서 id와 pwd의 유효성 검증을 utils의 함수를 호출하여 판별한다
- 판별이 끝난 값은 view에서 model에게 유저 create를 지시 ,유저에 대한 토큰 발급을 한 후 유저에 response한다

<br>

> 타이어 정보 저장
- request요청이 들어오면 마찬가지로 url에 매핑되는 View를 호출한다
- View에서는 요청에 맞게 로직을 실행한다. 이 과정에서 tire create의 중복을 줄이기 위해 utils의 함수를 호출하여 각각의 tire정보를 저장한다
- car, tire, spec에 대한 데이터가 model에 저장된 후 성공/실패에 대한 정보를 유저에 response한다

<br>

> 타이어 정보 조회

- request요청이 들어오면 마찬가지로 url에 매핑되는 View를 호출한다
- View에서는 유저의 인증을 위한 데코레이터가 실행되며 유저를 판별한다
- 유저가 인가 되면 유저의 자동차 타이어 정보를 가져오는 로직이 실행된다
- 이후 타이어 정보를 유저에 response한다

<br>

# 🔖 설치 및 실행 방법

### 로컬 및 테스트용

1. 해당 프로젝트를 clone하고, 프로젝트로 들어간다.

```
https://github.com/wanted-InfinityLoop/cardoc-InfinityLoop-hj.git .
cd cardoc
```

2. 가상환경으로 miniconda를 설치한다. [Go](https://docs.conda.io/en/latest/miniconda.html)

```
conda create -n deer python=3.9
conda actvate deer
```

3. 가상환경 생성 후, requirements.txt를 설치한다.

```
pip install -r requirements.txt

Django==3.2.9
django-cors-headers==3.10.0
gunicorn==20.1.0
mysqlclient==2.1.0
PyMySQL==1.0.2
bcrypt==3.2.0
PyJWT==2.3.0
requests==2.26.0

```

4. migrate 후 로컬 서버 가동

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

<br>

### 배포용

1. ec2 생성 후 ec2를 실행시킨다
```
ssh -i ~/Desktop/AWS_키페어/cardoc.pem ubuntu@52.78.100.243
```

2. ec2안에서 conda 가상환경을 생성하여 실행시킨다(개발용과 동일)

3. ec2의 가상환경 안에서 해당 프로젝트를 clone하고, 프로젝트로 들어간다.

4. requirements.txt안에 있는 패키지를 설치한 후 migrate를 진행한다

5. gunicorn을 실행시킨다. 이때 config가 있는 디렉토리 안에서 아래의 명령어를 실행시킨다
```
nohup gunicorn --bind=0.0.0.0:8000 config.wsgi &
```




