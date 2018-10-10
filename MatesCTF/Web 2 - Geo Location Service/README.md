## GEO LOCATION SERVICE
```http://125.235.240.169:5000/```

Sau khi đăng nhập bằng username bất kì thì thấy có chức năng sau

<p align="center">
  <img src="https://i.imgur.com/u2Nl712.png">
</p>

Thử nhập IP và captcha vào, chuyển qua burpsuite, thử request lên vài lần thì không thấy báo sai captcha<br/>
Decode flask cookie thử thì nhận được 1 đoạn JSON như sau: ```{"captcha":{" b":"YTA2NmJiNTEyZWQyY2VmOTBiNjE1OGMxMDhiYzkwYjg="},"username":"123"}```

<p align="center">
  <img src="https://i.imgur.com/yDhDs1u.png">
</p>

Ở đây dễ thấy captcha là 1 đoạn base64, decode base64 thì ra 1 đoạn MD5. Thử encode đoạn captcha plain text 2 lần thì chính là đoạn MD5 đã được decode.<br/>
Chứng tỏ captcha đã được chứa ở trong cookie, vậy là có thể bypass được captcha.

<p align="center">
  <img src="https://i.imgur.com/y1bkbOa.png">
</p>

Chú ý đến response, thấy có đoạn HTML cần chú ý là ```...followed by an <!--your--> IP address...```<br/>
Gửi request lên với IP của chính mình vào

<p align="center">
  <img src="https://i.imgur.com/ew7J1wx.png">
</p>

Biết được folder của flag là ```/home/web2/flag.txt```<br/>
Mình đoán bài này là Command Injection, thử vài ký tự cơ bản thì đều đã bị filter, response trả về ```Wrong Input```

<p align="center">
  <img src="https://i.imgur.com/2TENwx2.png">
</p>

Thử 1 hồi thì thấy dấu ```|``` là chưa bị filter, nhưng response trả về là ```Output format is wrong```

<p align="center">
  <img src="https://i.imgur.com/phGoS4z.png">
</p>

Lúc đầu mình định dùng netcat để chuyển file, nhưng nhận ra là server đã bị block outbound, suy nghĩ sang cách khác là cat file ra.<br/>
Mình tìm cách để bypass được ```Output format is wrong```.<br/>
Nhìn lại thì thấy output của ```geoiplookup 74.125.225.33``` là ```GeoIP Country Edition: US, United States``` nhưng trên response của web trả về thì chỉ có ```US, United States```<br/>
Thử echo một đoạn ra xem

<p align="center">
  <img src="https://i.imgur.com/RlANLAt.png">
</p>

Response trả về là đoạn sau của ```GeoIP Country Edition:```, vậy là bypass được format output. Tiếp theo thử cat file flag ra

<p align="center">
  <img src="https://i.imgur.com/XyFuG9F.png">
</p>

Response trả về là nội dung file flag.txt, nhưng không hiển thị hết. Số ký tự output ra bị giới hạn.<br/>
Sau một lúc search các công cụ để xóa bớt chuỗi trên linux thì mình tìm ra ```sed```<br/>
Cuối cùng thì cat ra flag

<p align="center">
  <img src="https://i.imgur.com/ImZgfgW.png">
</p>
