## ARE YOU FARMER?

![Image 1](https://i.imgur.com/Lr7STAT.png)

Vào web, việc đầu tiên mình làm là thử ngay SQL Injection. Thử với payload ```' or 1=1-- -``` thì đăng nhập thành công

![Image 2](https://i.imgur.com/VN7VjGl.png)

Sau khi đăng nhập thành công thì web không còn chức năng gì khác, không hiển thị thông tin gì trong database nên đoán rằng SQLi Blind.
Captcha nhìn đơn giản, dễ dàng bypass bằng pytesseract.

Vậy kịch bản sẽ như sau:
	- Request đến trang login, lấy ảnh captcha về
	- Dùng pytesseract để lấy ra chuỗi captcha
	- Request lại vào trang login với ```username = payload``` để kiểm tra đúng sai
	
Mình dùng binary search để giảm thời gian blind. Và cuối cùng là code ở đây: [solve.py](solve.py), các bạn tự edit payload để lấy ra flag nhé

![Image 3](https://i.imgur.com/G9k3nXh.png)