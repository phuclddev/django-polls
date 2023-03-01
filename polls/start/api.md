# Rout url api/
## user/get/
  
method: GET
### Request

### Response
  
```json
{
    "status": "successful",
    "payload": {
        "user": {
            "id": 3,
            "last_login": "2023-02-22 01:38:39",
            "username": "user2",
            "first_name": "",
            "last_name": "",
            "email": "",
            "is_staff": false,
            "is_active": true,
            "date_joined": "2023-02-20 08:59:53",
            "type": 2
        },
        "question": [
            {
                "id": 2,
                "question_text": "updated sixth question",
                "pub_date": "2023-02-22 01:38:15",
                "expire_date": "2023-03-22 09:28:14",
                "status": true,
                "user_created": 3,
                "type": 1,
                "pass_code": 812929
            }
        ],
        "vote_history": [
            {
                "id": 1,
                "question": 8,
                "user_voted": 3,
                "choice_text": "first choice"
            }
        ]
    }
}
```
## user/createQuestion/
  
method: POST
### Request

|Param|Type|Required|
| :---: | :---: | :---: |
|type|integer|True|
```json
{
	"question_text": "sixth question",
	"expire_date": "2023-03-22 09:28:14",
	"status": true,
	"type": 1,
    "choice": ["first choice", "second choice"]
}
```
### Response
```json
{
    "status": "successful",
    "payload": {
        "question_created": {
            "id": 10,
            "question_text": "sixth question",
            "pub_date": "2023-02-22 07:43:49",
            "expire_date": "2023-03-22 09:28:14",
            "status": true,
            "user_created": 3,
            "type": 1,
            "pass_code": 502517
        }
    }
}
```

## user/createQuestion/<int:id>/
method: PUT
### Request

|Param|Type|Required|
| :---: | :---: | :---: |
|type|integer|True|
```json
{
	"question_text": "updated sixth question",
	"expire_date": "2023-03-22 09:28:14",
	"status": true,
	"type": 2
}
```
### Response
```json
{
    "status": "successful",
    "payload": {
        "question_updated": [
            {
                "id": 10,
                "question_text": "updated sixth question",
                "pub_date": "2023-02-22 07:43:49",
                "expire_date": "2023-03-22 09:28:14",
                "status": true,
                "user_created": 3,
                "type": 2,
                "pass_code": 502517
            }
        ]
    }
}
```

## user/vote/
method: POST
### Request

|Param|Type|Required|
| :---: | :---: | :---: |
|type|integer|True|
```json
{
	"question_id": 8,
	"choice_id": 1
}
```
### Response
```json
{
    "status": "successful",
    "payload": {
        "vote_created_info": {
            "id": 1,
            "question": 8,
            "user_voted": 3,
            "choice_text": "first choice"
        }
    }
}
```

## question/get/
method: GET
### Request

### Response
```json
{
    "status": "successful",
    "payload": {
        "question_active_public": [
            {
                "id": 1,
                "question_text": "abc",
                "pub_date": "2023-02-21 10:58:50",
                "expire_date": "2023-03-20 09:28:14",
                "status": true,
                "user_created": 2,
                "type": 1,
                "pass_code": 423345
            },
            {
                "id": 2,
                "question_text": " 2",
                "pub_date": "2023-02-22 01:38:15",
                "expire_date": "2023-03-21 09:28:14",
                "status": true,
                "user_created": 3,
                "type": 1,
                "pass_code": 812929
            }
        ]
    }
}
```

## question/search/
method: GET
### Request

key: question_text

### Response
```json
{
    "status": "successful",
    "payload": {
        "search_results": [
            {
                "id": 5,
                "question_text": "fourth question",
                "pub_date": "2023-02-22 01:51:52",
                "expire_date": "2023-03-22 09:28:14",
                "status": true,
                "user_created": 3,
                "type": 1,
                "pass_code": 220920
            },
            {
                "id": 8,
                "question_text": "fourth question",
                "pub_date": "2023-02-22 02:00:30",
                "expire_date": "2023-03-22 09:28:14",
                "status": true,
                "user_created": 3,
                "type": 1,
                "pass_code": 466906
            }
        ]
    }
}
```

## <int:id>/result/
method: GET
### Request


### Response
```json
{
    "status": "successful",
    "payload": {
        "question_result": {
            "id": 8,
            "question_text": "fourth question",
            "pub_date": "2023-02-22 02:00:30",
            "expire_date": "2023-03-22 09:28:14",
            "status": true,
            "user_created": 3,
            "type": 1,
            "pass_code": 466906
        },
        "vote_result": [
            {
                "id": 1,
                "question": 8,
                "user_voted": 3,
                "choice_text": "first choice"
            }
        ]
    }
}
```