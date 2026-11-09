
#----------------------------초기 화면
# 초기 출력 화면 작성
def show_title():
    print("-"*50)
    print("1.상품목록 2.담기 3.빼기 4.장바구니 5.쿠폰 6.결제 q.종료")
    print("-"*50)

# 메뉴(카테고리) 선택
def category_select():
    while True:
        category_num = input("선택 : ").strip()
        if category_num not in ("1","2","3","4","5","6","q"): # 1~6번 중 하나를 선택하면
            print("1 ~ 6 사이의 숫자나 q를 입력하세요.") # 다른 숫자나 문자 입력시 안내문구 출력
            continue
        elif category_num == "1": # 상품목록보기
            items_list_print()
        elif category_num == "2": # 담기
            shoppingcart_item_add()
        elif category_num == "3": # 빼기
            shoppingcart_item_remove()
        elif category_num == "4": # 장바구니 보기
            shoppingcart_show()
        elif category_num == "5": #쿠폰
            coupon()
        elif category_num == "6": # 결제
            pay()
        elif category_num == "q": # 종료
            break
        
#----------------------------상품 목록(목록 생성 및 출력)
# 상품목록 만들기

def items_list():

    items_list = []

    # 상품정보 클래스 만들기
    class Item:

        item_number = 0

        def __init__(self, name, price, stock): # 상품명, 가격, 재고를 기본 속성으로
            Item.item_number += 1  # init 밖에서 선언한 변수는 클래스 명 붙여줘야 함!!🚨
            self.number = Item.item_number
            self.name = name
            self.price = price
            # if stock == 0: # 이거 나중에 목록 출력할때 넣어야 함
            #     self.stock = f"{stock} (품절)" # 재고가 0이면 옆에 (품절)까지 출력..인데 여기 넣으면 나중에 값으로 사용 못함!!!
            self.stock = stock

        def __str__(self):
            return f"{self.name:<20} {self.price:<15} {self.stock:<10}"
        
        def __repr__(self):
            return f"{self.name:<20} {self.price:<15} {self.stock:<10}"
        
        def add_list(self):
            items_list.append(self)

    item_1 = Item("무선 이어폰", 89_000, 3)
    item_2 = Item("텀블러", 15_000, 10)
    item_3 = Item("보조배터리", 32_000, 5)
    item_4 = Item("마우스패드", 9_000, 0)
    item_5 = Item("USB허브",18_000, 4)

    items_list.append(item_1)
    items_list.append(item_2)
    items_list.append(item_3)
    items_list.append(item_4)
    items_list.append(item_5)

    return items_list

# 상품 목록 출력 함수 만들기
def items_list_print():
    print(f"{'번호':<10} {'상품명':<20} {'가격':<15} {'재고':<10}")
    for item in items_list():
        if item.stock ==0:
            print(f"{item.number:<10} {item.name:<20} {item.price:<15} {item.stock:<10}(품절)")
        else:
            print(f"{item.number:<10} {item.name:<20} {item.price:<15} {item.stock:<10}")

#----------------------------쇼핑카트 생성 및 물건 담기, 빼기

class Shoppingcart:
    def __init__(self):
        self.shoppingcart = []  # 빈 쇼핑카트 최초 생성

    def in_cart(self, number, qty): # 번호와 수량을 받음

        # 또 담길 때
        for item_in_cart in self.shoppingcart: #쇼핑카트 리스트 내 추가된 상품 딕셔너리들에 대해
            if item_in_cart.number == number: # 이미 담긴 상품이면 수량에 +1 을 더하고
                item_in_cart.qty += qty
                return item_in_cart.name

        # 처음 담길 때
        for item in items_list(): # 상품 리스트 내 상품 하나의 딕셔너리 = item
            if item.number == number: # 입력받은 번호와 상품 딕셔너리의 번호값이 일치하는 것이 있다면
                item.qty = qty
                self.shoppingcart.append(item)
                return item.name

    def out_cart(self, number, qty):
        for item_in_cart in self.shoppingcart: #쇼핑카트 리스트 내 추가된 상품 딕셔너리들에 대해
            if item_in_cart.number == number: # 있는거 뺄 때
                item_in_cart.qty -= qty
                if item_in_cart.qty == 0:
                    self.shoppingcart.remove(item_in_cart)
                return item_in_cart.name
            else: # 없는거 뺄때
                return item_in_cart.name

# 쇼핑카트에 담는 함수
def shoppingcart_item_add():
    number = int(input("상품번호: "))
    qty = int(input("수량 : "))
    item = cart.in_cart(number, qty)
    print(f"{item} {qty}를 담았습니다.")

# 쇼핑카트에서 빼는 함수
def shoppingcart_item_remove(): 
    number = int(input("상품번호: "))
    qty = int(input("수량 : "))
    item = cart.out_cart(number, qty)
    print(f"{item} {qty}를 뺐습니다.")

# 쇼핑카트 보기
def shoppingcart_show():
    print("-"*50)
    total_price = 0
    for item in cart.shoppingcart:
        subtotal = item.qty*item.price
        total_price += subtotal
        print(f"{item.name} x {item.qty}       {subtotal}")
    print("-"*50)
    print(f"상품 합계 {total_price}원")
    print(f"할인 -{discount_price}원") # 할인

    if total_price - discount_price >= 30000 or cart == False:
        delivery_fee = 0
    else:
        delivery_fee = 3,000
    
    print(f"배송비 {delivery_fee}")

    final_price = total_price - discount_price + delivery_fee
    print(f"결제금액 {final_price}")


def pay():
    shoppingcart_show()
    for item in cart:
        item.stock -= item.qty
    cart = Shoppingcart()
    # 쿠폰 삭제
    print()


# ----------------------------할인 쿠폰 


def coupon():

    class Discount:
        def __init__(self):
            self.discount_amount = 0

    class RateDiscount(Discount):
        def __init__(self, total_price, rate=0.1, max_amount=5000):
            super().__init__()
            if total_price * rate >= max_amount:
                self.discount_amount = 5000
            else:
                self.discount_amount = int(total_price * rate)

    class FixedDiscount(Discount):
        def __init__(self, total_price, amount=3000, min_amount=20000):
            super().__init__()
            if total_price >= min_amount:
                self.discount_amount = amount
            else:
                self.discount_amount = 0

    print("1. 쿠폰 없음\n2.10% 할인(최대 5,000원)\n3. 3,000원 할인(20,000원 이상 구매 시)")
    coupon_number = int(input("쿠폰 번호 : "))

    if coupon_number == 1:
        coupon = Discount()
        discount_amount = coupon.discount_amount
        return discount_amount

    elif coupon_number == 2:
        coupon = RateDiscount()
        discount_amount = coupon.discount_amount
        return discount_amount

    elif coupon_number == 3:
        coupon = FixedDiscount()
        discount_amount = coupon.discount_amount
        return discount_amount


def main():
    show_title()
    category_select()


cart = Shoppingcart() # 최초 1회만 생성
discount_price = 0 
main()