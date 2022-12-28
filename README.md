# 프로젝트<br>
![image](https://user-images.githubusercontent.com/96002337/209745854-ca814f62-5c92-438d-be80-584cbeb69111.png)

프로젝트 일정 : 22.12.02 ~ 22.12.28<br>
Thumbook : https://www.thumbookfe.ml/<br>

Backend git: https://github.com/ksykma/Book_Space <br>
Frontend git : https://github.com/ksykma/Book_Space_Front<br>
S.A : https://www.notion.so/A1-c8728c9326d147d3b8dae30a8eba570c <br>

# 📖 프로젝트
머신러닝을 통한 책 추천 및 리뷰 인증 커뮤니티 플랫폼<br>
(밀러의 서재를 참고해서 만튼 북 커뮤니티 사이트입니다.)

##  팀원소개 + 팀원들간의 약속
### 팀원 역할

- 서장원(팀장) : 게시물 작성 페이지, 백엔드 배포, 프론트 배포
- 김남훈(팀원) : 메인 페이지, 추천 페이지, 회원가입시 이메일 인증, 페이지네이션
- 김서영(팀원) : 상세 페이지, 이메일 인증 페이지
- 천승현(팀원) : 피드 페이지, 메인 페이지, 크롤링, 좋아요 기능
- 최윤선(팀원) : 게시물 작성 페이지, 마이페이지, 토큰관련 유효성 검사, 검색기능

### 팀원간의 약속
<details>
    <summary>자세히</summary>

1. 정해진 시간에 모여서 진행사항 토의하기
- 아침(9시) : 당일 진행할 계획 얘기
- 저녁(7시) : 7시까지 진행한 내용 정리하기
- 저녁(9시) : 최종적으로 코드전부 합치고 기능작동확인
- 저녁(10시) : 작동이 안되는부분 수정하고 코드리뷰
2. GIT HUB Name-Convention 설정해서 지키기
- [ADD] appname.filename  (ex [user.serializer.py](http://user.serializer.py) ) #file 추가
- [MOD] appname.filename (ex [user.serializer.py](http://user.serializer.py) 수정내용) #file에서 기능 추가/수정
- [DEL] appname.filename (ex [user.serializer.py](http://user.serializer.py) 삭제내용) #file에서 기능 삭제
- [Comment] appname.filename (ex [user.serializer.py](http://user.serializer.py) 수정내용) #코멘트 관련
- [Design] css 수정
- [FIX] 수정한 에러
</details>

## 프로젝트 기능 
#### 기능분류는 페이지별로 나누었습니다
* ####  회원가입/로그인(modal)
    * 회원가입 시 동일 이메일, 유저네임 validation
    * 이메일과 비밀번호는 정규표현식을 통한 validation
    * 회원가입 한 이메일로 이메일 인증 메일을 발송, 권한 승인 후 로그인 가능
    * 로그인 시 JWT토큰에 유저이메일, 유저PK값을 포함시켜 localStorage에 저장
    * 로그인 시 비밀번호는 django의 check_password를 통해 입력한 비밀번호와 DB에 저장된 비밀번호가 일치하는지 체크
    * 로그인 시 이메일 인증 권한 승인을 통해 사용자 아이디의 활성화 유무를 체크
* ####  메인페이지(main)
    * request.GET을 통해 userID값을 받아온 후 DB에 저장된 추천 책 리스트를 통해 추천시스템의 결과 리스트
    * 책 많이 읽은 유저, 게시글이 많이 작성된 책 등 분류 기준을 통해 사용자 데이터 정렬
    * 이미지 Slide를 통해 사용자에게 사이트 정보 제공
    * 로딩 이미지를 넣어서 사용자가 서비스를 이용할때 로딩이 되고있는 상황을 인지시킴 
* ####  기록하기(booklist)
    * yes24 bestseller에 있는 책 데이터(이미지, 제목, 내용, 장르)를 크롤링
    * 독후감을 쓸 책을 검색
    * 페이지네이션
    * 책을 선택 후 선택한 책에 대한 Book_id를 받아와 글쓰기 페이지로 이동
    * 원하는책이 없거나 읽은책에 대한 검색결과가 없을경우 새글쓰기를 통해 독후감 작성 가능
* ####  독후감 작성(post)
    * 책관련 독후감, 책인증 이미지, 별점을 필수로 작성해야 저장이 가능
    * 검색한책이 있을경우 선택한 책에 대한 book_id.title를 받아와 책제목이 자동으로 작성
    * 검색한책이 없을경우 책제목란에 제목을 입력하고 독후감을 작성
    * 게시글에 대한 공개/비공개 선택 가능
* ####  커뮤니티(feed)
    * 셀렉트박스(onchange())를통해 피드를 좋아요순, 댓글순, 별점순으로 나열가능
    * 좋아요기능 
    * 별점, 댓글, 좋아요 수 실시간으로 출력
    * 프로필사진을 누를 시 user_id를 가지고 마이페이지로 이동
    * 더보기버튼을 누를 시 article_id를 가지고 상세페이지로 이동
* ####  상세페이지(detail)
    * article_id를 받아와 글쓴이가 쓴 독후감의 이미지, 내용, 제목을 출력
    * 게시글작성자 기준에서 자신이 쓴 글만 수정, 삭제, 댓글삭제 가능
    * 댓글작성자 기준에서 댓글 작성/수정/삭제 가능
* ####  추천도서(customlist)
    * 책 10권을 랜덤으로 리스트를 나타냄
    * 셀렉트박스를 통해 장르별로 선택가능(특정장르 책10권 랜덤)
    * request.data.get을 통해 사용자가 선택한 책 리스트를 DB에 저장 후 결과는 메인페이지에 출력 
* ####  마이페이지(userpage)
    * 자신이 쓴 게시글, 좋아요 누른 글을 모아서 볼 수 있음
    * 회원정보 수정을 한가지만 수정해도 가능하도록 request받은 data에 따라 딕셔너리 표현식으로 구분지어서 put시킴

## 기술 스택
* ### Backend
    <details>
        <summary></summary>

      - Django
      - Django Rest Framework
      - Django Rest Framework simple-jwt 
      - Python
      - SMTP
    </details> 

* ### Frontend
     <details>
          <summary></summary>

    * HTML
    * Javascript
    * CSS
     </details> 
* ### DB
     <details>
            <summary></summary>
     * Sqlite3
     * PostgreSQL 
     * AWS S3 
     </details> 
* ### 배포
     <details>
              <summary></summary>
     * docker 
     * AWS EC2
     * AWS Route53
     * gunicorn
     * Nginx
     * cloudFront
    </details>
    
## 스택사용배경
* **Django / DRF**
    * Serializer, 유저 관리, REST API 등 Django에서 제공하는 기능들을 사용하기위해서 사용하였다.
* **Django Rest Framework simple-jwt**
    * 유저 인증을 토큰방식으로 암호화하기 위해 사용하였다
* **AWS EC2**
    * 사용한만큼 지불하므로 저렴하다는 장점이있고, 사용자가 인스턴스를 완전히 제어할 수 있다. 보안 및 네트워크 구성, 스토리지 관리 효과적이다.
* **AWS S3**
    * 서비스에서 이미지를 업로드 할때, EC2에 저장을 하게되면 용량이 부족해지고 파일들을 관리하기가 어렵습니다. 그래서 파일 저장에 최적화 되어있고, 저장용량이 무한대에 가까운 S3를 사용해서 이미지 파일들을 저장하고 관리 했습니다
* **Docker**
  * Docker는 소프트웨어를 컨테이너라는 표준화된 유닛으로 패키징하는데, 컨테이너에는 라이브러리, 시스템 도구, 코드, 런타임 등 소프트웨어를 실행하는데 필요한 모든것이 포함되어 있습니다. Docker를 사용하면 코드를 더 빨리 전달하고, 애플리케이션 운영을 표준화하고, 코드를 원활하게 이동하고, 리소스 사용률을 높여 비용을 절감할 수 있습니다.
* **Gunicorn**
  * Django의 runserver과 똑같은 역할로 수행하지만 보안적으로나 성능적으로 검증이 되지 않아 사용할 수 없다. 그러한 단점을 보안을 시켜 웹서버와 Django사이에서 Request를 처리해주는 역할을 수행하기위해 사용하였다. 
* **Nginx**
  * Nginx는 경량의 자원 활용과 물리적인 하드웨어로 쉽게 확장할 수 있다. 정적인 컨텐츠들을 빠르게 처리하며, 동적 처리를 별도로 담당하는 소프트웨어 스택들과 연계해서 고성능 서버를 제공하는 데 적합하다고 알려졌다. 또한 Nginx는 프록시 서버 기능도 제공한다
* **beautifurSoup**
  * 텍스트형태의 데이터에서 원하는 html 태그를 쉽게추출할 수 있게금 해주는 기능이라서 크롤링할때 사용하기에 적합하였다.

## 아키텍쳐
## 피드백

 
