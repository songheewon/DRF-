1. product라는 앱을 새로 생성해주세요
2. product 앱에서 <작성자, 제목, 썸네일, 설명, 등록일자, 노출 시작 일, 노출 종료일>가 포함된 product 테이블을 생성해주세요

3. django serializer에서 기본적으로 제공하는 validate / create / update 기능을 사용해 event 테이블의 생성/수정 기능을 구현해주세요
   * postman으로 파일을 업로드 할 때는 raw 대신 form-data를 사용하고, Key type을 File로 설정해주세요

4. 등록된 이벤트 중 현재 시간이 노출 시작 일과 노출 종료 일의 사이에 있거나, 로그인 한 사용자가 작성한 product 쿼리셋을 직렬화 해서 리턴해주는 serializer를 만들어주세요

5. product field를 admin에서 관리할 수 있도록 등록해주세요
