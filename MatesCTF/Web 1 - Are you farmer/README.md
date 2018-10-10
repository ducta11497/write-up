## ARE YOU FARMER?
```http://125.235.240.166:5000/```

<p align="center">
  <img src="https://i.imgur.com/Lr7STAT.png">
</p>

Vào web, việc đầu tiên mình làm là thử ngay SQL Injection. Thử với payload ```' or 1=1-- -``` thì đăng nhập thành công

<p align="center">
  <img src="https://i.imgur.com/VN7VjGl.png">
</p>

Sau khi đăng nhập thành công thì web không còn chức năng gì khác, không hiển thị thông tin gì trong database nên đoán rằng SQLi Blind.
Captcha nhìn đơn giản, dễ dàng bypass bằng pytesseract.

Vậy kịch bản sẽ như sau:<br/>
	* Request đến trang login, lấy ảnh captcha về
	* Dùng pytesseract để lấy ra chuỗi captcha
	* Request lại vào trang login với ```username = payload``` để kiểm tra đúng sai
	
Mình dùng binary search để giảm thời gian blind. Và cuối cùng là code ở đây: [solve.py](solve.py)

<p align="center">
  <img src="https://i.imgur.com/G9k3nXh.png">
</p>