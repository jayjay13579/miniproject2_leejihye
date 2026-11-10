# Mini Project 02 : 온라인 쇼핑몰 장바구니 만들기 (AX3기 이지혜)

#---------------------------------초기화면 표출---------------------------------

# 초기 화면 작성 함수
def show_title():
    print("-"*50)
    print("1.상품목록 2.담기 3.빼기 4.장바구니 5.쿠폰 6.결제 q.종료")
    print("-"*50)

# 메뉴(카테고리) 선택 함수
def category_select():
    while True: # while문을 통해 종료(q)전에는 계속 항목 선택 가능하도록 제어
        category_num = input("선택 : ").strip()
        if category_num not in ("1","2","3","4","5","6","q"): # 1~6번,q 중 하나를 선택하지 않으면
            print("1 ~ 6 사이의 숫자나 q를 입력하세요.") # 안내문구 출력
            continue # 다시 선택 항목 입력할 수 있도록 continue
        elif category_num == "1": # feat1. 상품목록보기
            items_list_print()
        elif category_num == "2": # feat2. 담기
            shoppingcart_item_add()
        elif category_num == "3": # feat3. 빼기
            shoppingcart_item_remove()
        elif category_num == "4": # feat4. 장바구니 보기
            shoppingcart_show()
        elif category_num == "5": # feat5. 쿠폰
            coupon_select()
        elif category_num == "6": # feat6. 결제
            pay()
        elif category_num == "q": # 종료
            break
        print("\n")
        
#---------------------------------feature 1. 상품목록---------------------------------

# 상품목록 생성 함수
def items_list():

    items_list = [] # 함수 실행 즉시 상품목록 넣을 리스트 먼저 설정
    # 결제 후 목록에 재고 반영되려면 이 함수가 한번만 실행되어야 함 -> main 함수 전 먼저 선언!
    # 만약 반복되어 실행되도록 하면 목록이 계속 처음부터 만들어지고 이전 재고 변경 반영 불가

    # 상품정보 클래스 만들기
    class Item:

        item_number = 0 # 클래스 변수(상품 번호 설정을 위해)

        def __init__(self, name, price, stock): # 상품명, 가격, 재고를 기본 속성으로 받기
            Item.item_number += 1  # init 밖에서 선언한 변수는 클래스 명 붙여줘야 함!! 변수이름만 딸랑 쓰면 X 🚨
            self.number = Item.item_number 
            self.name = name
            self.price = price
            self.stock = stock

        # 혹시 몰라서 __str__, __repr__를 넣긴 했지만 과연 필요한 부분인지..?
        def __str__(self): 
            return f"{self.name:<20} {self.price:<15} {self.stock:<10}"
        
        def __repr__(self): 
            return f"{self.name:<20} {self.price:<15} {self.stock:<10}"

        # 상품목록 리스트에 상품 객체 추가하기
        def add_list(self):
            items_list.append(self)

        # 재고 변경을 위한 메서드 추가(아래에 결제 후 재고 변경할때 쓰려고)
        def change_stock(self, qty):
            self.stock -= qty

    # 상품 객체 만들기
    item_1 = Item("무선 이어폰", 89_000, 3)
    item_2 = Item("텀블러", 15_000, 10)
    item_3 = Item("보조배터리", 32_000, 5)
    item_4 = Item("마우스패드", 9_000, 0)
    item_5 = Item("USB허브",18_000, 4)

    # 상품 객체를 목록에 추가하기
    items_list.append(item_1)
    items_list.append(item_2)
    items_list.append(item_3)
    items_list.append(item_4)
    items_list.append(item_5)

    return items_list # 상품목록 생성함수는 상품 객체들이 들어있는 리스트를 반환

# 상품목록을 보여주기 위한 함수
def items_list_print():
    print(f"{'번호':<10} {'상품명':<20} {'가격':<15} {'재고':<10}")
    for item in products_list: # products_list 전역변수에 아까 return한 객체들의 리스트 값(상품목록)을 저장해놓은 상태
        if item.stock ==0: # 만약 재고가 0 이라면
            print(f"{item.number:<10} {item.name:<20} {item.price:<15} {item.stock:<10}(품절)") # 발제문 예시와 똑같이 (품절) 표시
            # 하지만 더 간소화 할 수 있을 것 같은 코드
        else:
            print(f"{item.number:<10} {item.name:<20} {item.price:<15} {item.stock:<10}")
            # 근데 이렇게 정렬을 사용했는데도 줄마다 정렬이 살짝씩 틀어져서 출력됨ㅠㅠ

#---------------------------------feature 2/3. 상품 담기/빼기---------------------------------

# 장바구니(쇼핑카트) 클래스 추가
class Shoppingcart:
    def __init__(self):
        self.shoppingcart = []  # 빈 쇼핑카트 최초 생성

    def in_cart(self, number, qty): # 상품번호와 수량을 받아 쇼핑카트에 추가하는 메서드
        
        # 기존에 이미 들어있던 상품이 또 담길 때
        for item_in_cart in self.shoppingcart: #쇼핑카트 리스트 내 추가된 상품 딕셔너리들에 대해
            if item_in_cart.number == number: # 번호로 해당 상품을 찾고
                if qty + item_in_cart.qty <= item_in_cart.stock: # 추가 수량+기존 수량이 재고를 넘지 않을 때
                    item_in_cart.qty += qty # 이미 담긴 상품이면 기존 수량에 숫자만 더하고
                    return item_in_cart.name # 상품 이름만(장바구니 목록, 영수증 출력용) 반환
                else: # 만약 재고보다 더 추가하려고 하는 상황이면?
                    print(f"재고가 부족합니다. (담을 수 있는 수량 : {item_in_cart.stock-item_in_cart.qty}개)") # 재고 - 기존 장바구니 수량
                    return False # 아무것도 실행x

        # 처음 담길 때
        for item in products_list: # 상품 리스트 내 상품 하나의 딕셔너리 = item
            if item.number == number: # 입력받은 번호와 상품 딕셔너리의 번호값이 일치하는 것이 있다면
                if qty <= item.stock: 
                    item.qty = qty 
                    self.shoppingcart.append(item) # 쇼핑카트에 상품 객체를 추가하고
                    return item.name # 상품 이름만 반환
                else:
                    print(f"재고가 부족합니다. (담을 수 있는 수량 : {item.stock}개)")
                    return False # 아무것도 실행x

    def out_cart(self, number, qty): # 쇼핑카트에서 제외하는 메서드
        for item_in_cart in self.shoppingcart: #쇼핑카트 리스트 내 추가된 상품 딕셔너리들에 대해
            if item_in_cart.number == number: # 기존에 있는 상품을 뺄 때
                item_in_cart.qty -= qty # 수량만 줄이기
                if item_in_cart.qty <= 0: # 혹시 가지고 있는 것보다 많이 빼려할 때도 어쨌든 그냥 삭제 처리
                    self.shoppingcart.remove(item_in_cart) # 기존 쇼핑카트 리스트에서 해당 객체 제거
                return item_in_cart.name
        # 없는거 뺄때 (위에서 걸러져서 함수 탈출하지 못해야 아래가 실행됨)
        print(f"장바구니에 해당 상품이 없습니다.")
        return False # 아무것도 실행x

# 쇼핑카트에 담는 함수(번호, 수량받기)
def shoppingcart_item_add():
    number = int(input("상품번호: ")) 
    qty = int(input("수량 : "))
    item = cart.in_cart(number, qty) # 객체를 카트에 추가
    if item: # 담기 메서드 반환값이 False(재고 부족으로 못담는 등 상태)가 아닐때! 즉 True 일때
        print(f"{item} {qty}를 담았습니다.") # 출력은

# 쇼핑카트에서 빼는 함수(번호, 수량받기)
def shoppingcart_item_remove(): 
    number = int(input("상품번호: "))
    qty = int(input("수량 : "))
    item = cart.out_cart(number, qty) # 객체를 카트에 추가
    if item: # 빼기 메서드 반환값이 True 일때
        print(f"{item} {qty}를 뺐습니다.")

#---------------------------------feature 4. 장바구니---------------------------------

# 쇼핑카트 보기
def shoppingcart_show():

    # 상품 합계 계산
    print("-"*50)
    total_price = 0
    for item in cart.shoppingcart: # 쇼핑카트 리스트에 있는 상품 객체들에 대해 반복
        subtotal = item.qty * item.price # 상품별 합계
        total_price += subtotal # 전체 합계
        print(f"{item.name} x {item.qty}       {subtotal}") # 출력
    print("-"*50)
    print(f"상품 합계 {total_price}원")

    # coupon 적용
    discount_price = coupon(selected_coupon_number, total_price)
    print(f"할인 -{discount_price}원 : {selected_coupon_name}")

    # 배송비
    if total_price - discount_price >= 30000 or not cart.shoppingcart: # 총액 3만원 넘거나 카트에 아무것도 없을 때
        # 처음에 cart.shoppingcart==False라고 했다가 계속 오류났었음..
        delivery_fee = 0
    else:
        delivery_fee = 3_000
    print(f"배송비 {delivery_fee}")

    # 결제금액
    final_price = total_price - discount_price + delivery_fee
    print(f"결제금액 {final_price}")

#---------------------------------feature 5. 쿠폰---------------------------------

# 쿠폰 선택하기 함수
def coupon_select():
    global selected_coupon_number # 전역 변수를 가져와서 활용해야해서
    global selected_coupon_name
    coupon_dict = {1:"쿠폰 없음", 2:"10% 할인(최대 5,000원)", 3:"3,000원 할인(20,000원 이상 구매 시)"} # 번호:쿠폰내용 매치
    for number, coupon in coupon_dict.items(): # 쿠폰에 있는 항목들을 하나씩 출력해서 보여줌
        print(f"{number}. {coupon}")
    selected_coupon_number = int(input("쿠폰 번호 : ")) # 쿠폰번호를 입력받아 전역변수로 저장
    selected_coupon_name = coupon_dict[selected_coupon_number] # 쿠폰번호에 대한 쿠폰 내용(이름) 입력받아 전역변수로 저장

def coupon(coupon_number, total_price=0): 
    # 혹시 장바구니 빈 상태에서 쿠폰 항목 선택해도 오류 생기지 않도록 total_price 기본값 0으로 설정

    # 발제문에서 클래스 형태가 이미 명시되어 있길래 가져와서 썼는데 상속을 여기에 쓰는 것이었는지는 잘 모르겠음..
    class Discount: # 부모 클래스 
        def __init__(self):
            self.discount_amount = 0 # 만약 쿠폰이 없다면 할인 금액은 0

    class RateDiscount(Discount): # 자식 클래스 1
        def __init__(self, total_price, rate=0.1, max_amount=5000): # 발제문 기 제시
            super().__init__() # 부모 클래스에 정의된게 거의 없어서 딱히 의미가 없는 것 같기도...
            if total_price * rate >= max_amount:
                self.discount_amount = 5000 # 계산한 할인액이 5000원 넘어버리는건 모두 할인금액 5000으로 한정
            else:
                self.discount_amount = int(total_price * rate) # 5000원을 넘지 않으면 계산된 할인액 만큼

    class FixedDiscount(Discount): # 자식 클래스 2
        def __init__(self, total_price, amount=3000, min_amount=20000):  # 발제문 기 제시
            super().__init__()
            if total_price >= min_amount: # 전체 금액이 20000원 이상이면
                self.discount_amount = amount # 3000원 할인
            else:
                self.discount_amount = 0 # 넘지 않으면 0원 할인

    # 다음의 코드는 함수 하나로 기능을 묶어서 간소화할 수도 있을것 같은데(다마고치 각 게이지 변경 함수처럼..?)
    if coupon_number == 1: # 1번 쿠폰 선택시
        coupon = Discount() # Discount 객체 -> 할인 0원
        discount_amount = coupon.discount_amount
        return discount_amount # 할인액 반환

    elif coupon_number == 2: # 2번 쿠폰 선택시
        coupon = RateDiscount(total_price) # RateDiscount 객체 -> 비율 할인액 계산
        discount_amount = coupon.discount_amount
        return discount_amount # 할인액 반환

    elif coupon_number == 3: # 3번 쿠폰 선택시
        coupon = FixedDiscount(total_price) # FixedDiscount 객체 -> 고정할인액 계산
        discount_amount = coupon.discount_amount
        return discount_amount # 할인액 반환
    
#---------------------------------feature 6. 결제---------------------------------

# 결제 함수
def pay():
    
    # 초기화해야해서 전역변수들 가져옴
    global cart 
    global selected_coupon_number 
    global selected_coupon_name

    if not cart.shoppingcart: # 만약 장바구니가 비어있다면
        print("결제할 상품이 없습니다.")
        return False

    # 영수증(쇼핑카트 목록 활용) 출력
    print("-"*50)
    print(f"{'영수증':>30}")
    shoppingcart_show()

    # 재고 삭제
    for item in cart.shoppingcart: # 카트에 있는 상품들에 대해 상품의 재고량을 변경
        item.change_stock(item.qty) # 재고변경 메서드 활용
        # print(item.stock) 확인용 출력

    # 카트 초기화
    cart = Shoppingcart()

    # 쿠폰 삭제(초기화)
    selected_coupon_number = 1
    selected_coupon_name = ""

    print("결제가 완료되었습니다. 감사합니다!")

#---------------------------------프로그램 실행하기---------------------------------

# 장바구니 main 로직 함수
def main():
    show_title() # 초기화면 보여주기
    category_select() # 메뉴(카테고리) 선택(안에 while문이 포함되어 자동으로 계속 반복됨) -> 다시 while문으로 함수 돌리지 X

# 사전에 미리 선언해야하는 내용들(최초 1회만 필요, 저장하지 않으면 실행마다 값이 바뀌는 경우)
products_list = items_list() # 최초 1회만 생성 -> 저장하지 않으면 재고 변화가 반영 X ㅠㅠ 계속 목록이 새로 만들어지기때문
cart = Shoppingcart() # 최초 1회만 생성 -> 저장하지 않으면 쇼핑카트가 계속 초기화됨
selected_coupon_number = 1 # 쿠폰 초기값, 혹시 쿠폰을 선택하지 않은 상태에서 결제하는 경우도 있을 것이라 먼저 선언 한번함
selected_coupon_name = "" # 쿠폰이름 초기값

# 장바구니 프로그램 실행
main()
