## ✍🏻 2022.06.15 과제
------------------
<p align="center"><b>< 문제 ></b></p>
  
<p align="center">1. args, kwargs를 사용하는 예제 코드 짜보기</p>
<p align="center">2. mutable과 immutable은 어떤 특성이 있고, 어떤 자료형이 어디에 해당하는지 서술하기</p>
<p align="center">3. DB Field에서 사용되는 Key 종류와 특징 서술하기</p>
<p align="center">4. django에서 queryset과 object는 어떻게 다른지 서술하기</p>

------------------
<br><br>
  

### 1. args, kwargs 연습해보기
args는 여러 개의 인자를 함수로 받고자 할 때 쓰인다. 예를 들어, 스파르타캠프에서 각 조마다 팀원들의 이름을 출력하고자 한다. 그런데 팀원이 몇 명인지는 정해져 있지 않다. *args가 아닌 매개변수로 def team(name1, name2) 와 같은 방식을 이용할 경우, 매개변수의 개수가 정해져 있고 이를 맞춰주어야 한다. 그러나 *args를 사용하게 되면 매개변수의 개수를 정해두지 않고 입력을 받을 수 있다. 코드를 작성해보자!
<br><br>
```
def make_team(teamname, *args):
    print("팀명:", teamname)
    print("팀원:", args)
    
make_team("머선12조", "송히", "규민", "철현", "재완")
```
<p align="center"><img src='https://blog.kakaocdn.net/dn/HatED/btrESIMoKVH/kSrpyFzQxeCynZ8l4dEtJk/img.png'></p>
<br><br>
그냥 args를 출력하게 되면 tuple 형태로 출력이 되는 것을 확인할 수 있다. 이를 활용해 예쁘게 작성해볼 수도 있다.

```
def make_team(teamname, *args):
    print("팀명:", teamname)
    print("팀원:", ", ".join(args))
    
make_team("머선12조", "송히", "규민", "철현", "재완")
```
<p align="center"><img src='https://blog.kakaocdn.net/dn/cwsUN2/btrESmQqw1c/q8f6a6NHMc6Yoh20lLr7Bk/img.png'></p>
<br><br>
 
kwargs도 여러 개의 인자를 받을 수 있다는 점에서 args와 유사하다. 차이점이 있다면 kwargs는 함수 호출 시 'keyword=특정 값' 의 형태를 이용하여 호출한다는 것이다. 그리고 함수 내에서 kwargs.items()를 이용하여 이를 조회할 수 있다. 코드를 작성해보자!
<br><br>
```
def make_team(**kwargs):
    print(kwargs)

make_team(머선12조="송히, 규민, 철현, 재완", 옆조="슬기, 주현, 경수, 대근")
```

<p align="center"><img src='https://blog.kakaocdn.net/dn/xqMwp/btrEQSigaRm/DSVKxUZzpYQRUxNaZHQIa0/img.png'></p>
<br><br>

이와 같은 결과 값을 가지게 되는데, kwargs의 경우 dictionary의 형태를 지니기 때문에 items() 메소드를 통해 key와 value로도 나눌 수 있다.
<br><br>
```
def make_team(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

make_team(머선12조="송히, 규민, 철현, 재완", 옆조="슬기, 주현, 경수, 대근")
```

<p align="center"><img src='https://blog.kakaocdn.net/dn/bx9hZy/btrERmi7uSQ/QtkWA0JqMAel6IdqpZ8TO0/img.png'></p>
<br><br><br><br><br>

### 2. mutable과 immutable의 특성과 해당하는 자료형
mutable은 값이 변한다는 뜻이고, immutable은 값이 변하지 않는다는 뜻이다. 값이 변한다는 것과 변하지 않는다는 것은 다른 변수에 복사를 했을 경우 확인할 수 있다. 코드를 작성해보자!
<br><br>
```
team_name = "머선12조"
team_member = ['송히', '규민', '철현', '재완']
```
이렇게 되면 'team_name' 이라는 변수에는 '머선12조' 라는 문자열형의 값이, 'team_member' 라는 ['송히', '규민', '철현', '재완'] 이라는 리스트형의 값이 저장된다. 이 두 변수를 다른 변수에 저장해보자.
<br><br>
```
team_name_copy = team_name
team_member_copy = team_member
```
이렇게 되면 'team_name_copy' 에는 'team_name' 의 값인 '머선12조'가, 'team_member_copy'에는 'team_member' 변수의 값인 ['송히', '규민', '철현', '재완'] 이 저장될 것이다. 그럼 이제 'team_name_copy'와 'team_member_copy' 는 값을 복사한 것이니까 수정해도 'team_name'과 'team_member' 에도 영향을 안 주지 않을까? 코드를 작성해보자!
<br><br>
```
team_name_copy = "저희의 팁명은 머선12조 입니다!"

print('team_name의 값:', team_name)
print('team_name_copy의 값:', team_name_copy)
```
우선, 'team_name_copy' 를 수정하여 본 것이다. 예상하기에는 'team_name'은 '머선12조', 'team_name_copy'는 '저희의 팀명은 머선12조 입니다!' 라고 출력될 것이다. 확인해보자.
<br>
<p align="center"><img src='https://blog.kakaocdn.net/dn/FeQj5/btrEOHaO2Sh/7Z1guRKPhbLNNwqdJrJPjk/img.png'></p>
예상과 동일한 결과를 얻을 수 있었다.
<br><br><br>

그렇다면 'team_member_copy'를 수정해보면 어떨까? 같은 결과를 가져올지 코드를 작성해보자!
```
team_member_copy.append('아무개')

print('team_member의 값', team_member)
print('team_member_copy의 값', team_member_copy)
```
team_member_copy에 '아무개' 라는 원소를 추가했다. 예상대로 'team_member_copy' 에만 '아무개'가 추가되었을 지 확인해보자.
<br>
<p align="center"><img src='https://blog.kakaocdn.net/dn/GZAc2/btrEND7jWyi/He8a8hwWT8odA1dvvNTDz0/img.png'></p>
이번엔 'team_member_copy' 의 변화가 'team_member' 에도 영향을 준 것을 확인할 수 있다.
<br><br><br>

이처럼 그냥 다른 변수에 값을 복사하더라도 원래의 변수에 변화를 끼칠 수 있는 자료형을 mutable한 자료형, 변화를 끼치지 않는 자료형을 immutable한 자료형이라 한다. mutable한 자료형에는 list, dictionary 등이 있고, immutable한 자료형에는 문자열형, 숫자형, boolean형 등이 있다.

 

mutable한 자료형을 복사할 때는 이전 변수에 영향을 끼칠 수 있기 때문에 주의해야하는데, 그렇다면 mutable한 자료형을 immutable하게 복사하는 방법은 없을까? 그렇지 않다. deepcopy() 메소드를 통해 복사하거나, 리스트의 경우 [:] 를 통해 복사하게 되면 이제 두 변수는 mutable한 관계에 놓이지 않게 된다.
<br><br><br><br><br>

### 3. DB field 내 key의 종류 
* Primary Key (기본키): 유일무이한 값이다. 예를 들어, 우리 나라에서 '원송희'라는 이름은 기본키로 사용될 수 없다. 동명이인이 존재할 가능성이 있기 때문이다. 그래서 신분을 확인하기 위해 주민등록번호를 부여하는데, 주민등록번호는 개인의 고유한 번호이기 때문에 다른 사람과 중복될 수 없다. 그러므로 주민등록번호는 기본키가 될 수 있는 것이다. 

 

* Candidate Key (후보키): 기본키가 될 수 있는 키를 후보키라고 한다. 예를 들어, 주민등록번호 이외에도 핸드폰 번호는 유일한 값일 것이다. 이처럼 기본키처럼 사용될 수 있는 키를 후보키라 한다.

 

* Foreign Key (외래키): 두 개의 테이블을 이어주면서 관계를 맺어주는 기준이 되는 키를 외래키라 한다. 예를 들어, 저번 프로젝트의 경우, Animation 테이블에는 title, genre_id가 속성으로 존재했고, Genre 테이블에는 genre_id, genre_name(한글)이 존재했다. 이와 같은 경우, Animation 테이블의 genre_id를 통해 genre_name을 조회할 수 있기 때문에 genre_id는 외래키로서 작용하는 것이다.
<br><br><br><br><br>

### 4. Django에서 Queryset과 Object의 차이
Queryset은 filter() 메소드를 사용했을 때 불러와지고, Object는 get() 메소드를 사용했을 때 불러와진다. Object는 말 그대로 객체를 가리키기 때문에 바로 원하는 column에 접근이 가능하지만, Queryset은 객체를 바로 가리키는 것이 아니라 dictionary형태로 반환은 하기 때문에 values() 메소드를 통해야만 비로소 원하는 column에 접근이 가능하다. 
