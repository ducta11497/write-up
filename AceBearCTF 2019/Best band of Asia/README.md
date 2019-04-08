## Best band of Asia
```http://3.0.183.241/```

Sau khi vào website, mình thấy tác giả là 1 fan chân chính của nhóm nhạc "Đen Hồng", trên menu có 4 mục chính như trong ảnh.
<p align="center">
  <img src="https://i.imgur.com/LFeOAxL.png">
</p>

Cụ thể chức năng của từng mục như sau:<br/>
	- Image: Để xem ảnh của của các idol<br/>
	- Fetch Image Page: Điền vào 1 URL website và in ra những ảnh có website đấy<br/>
	- Upload: Khi ấn vào thì chỉ hiện lên "Permission denied" và ảnh của idol nào đấy cũng xinh phết<br/>
	- Audio: Để set default video trên trang web, set xong thì video sẽ hiện ở góc phải dưới trang web<br/>

Đầu tiên sau khi nhìn qua 1 lượt tổng thể của trang web thì mình nghĩ ngay đến việc tấn công vào trang Fetch Image, có thể ở đây dính SSRF hoặc LFI.<br/>
Thử scheme file và các php wrapper vào thì đều báo invalid url, chỉ có chấp nhận những URL hợp lệ với scheme là http hoặc https

<p align="center">
  <img src="https://i.imgur.com/00yj59t.png">
</p>

Cảm thấy có vẻ không ổn, mình chuyển qua tìm cách tấn công khác, chú ý đến trang Image nhìn có vẻ bình thường, nhưng URL ảnh thì có vẻ không bình thường lắm. Ảnh đc get ra từ PHP chứ không phải link trực tiếp của ảnh

<p align="center">
  <img src="https://i.imgur.com/8TabYkg.png">
</p>

Mình liền thử SQL injection ở parameter id thì thấy đúng là đoạn này dính SQLi blind thật. Quăng vào sqlmap cho nó chạy, sau một hồi lần mò thì nhận được cái kết khá đắng
<p align="center">
  <img src="https://i.imgur.com/QiYecsu.png">
</p>

Act cool, đứng hình mất hơn 30 phút thì thằng em trong đội có ý kiến là thử đọc file hay ghi file xem có được không. Oke thử liền và công nhận là đọc được thật nhưng không ghi được.<br/>
F12 lên xem request thì biết được website đang chạy Apache, vậy thì nhiều khả năng là web vẫn ở folder default. Đọc thử file **"/var/www/html/index.php"** và đọc được, từ đây là mình có thể đọc được source của web rồi.
<p align="center">
  <img src="https://i.imgur.com/sw0omVS.png">
</p>

Nhìn vào đây thì thấy **controller_image.php** là 1 file khá quan trọng, mình lại dùng sqlmap get file này về để đọc tiếp<br/>
Sau khi get về thì mình thấy có một số function cần lưu ý.<br/>
Đầu tiên là function **detail:**
<p align="center">
  <img src="https://i.imgur.com/vKE225a.png">
</p>

Có thể thấy đây là đoạn code bị dính SQLi ở phía trên, không những thế mình còn có thể kiếm soát được biến $filename bằng cách union filename. Cụ thể payload đoạn này như sau: "http://3.0.183.241/index.php?controller=image&act=detail&id=0 union select '/etc/passwd'"
<p align="center">
  <img src="https://i.imgur.com/fbSokIB.png">
</p>
Thế là mình có thể đọc được source code của website thông qua đoạn này không cần chờ sqlmap nữa.<br/>
Tiếp theo là function **upload:**
<p align="center">
  <img src="https://i.imgur.com/MQG1CXc.png">
</p>
Ở function này thì nếu có $_SESSION['admin'] thì mới được vào trang upload, nhưng trang này đâu có chức năng login đâu. Ngồi nghĩ 1 hồi thì mình chợt nhận ra là mình có thể truy cập thẳng vào cái link view/view_upload.php mà, hơn nữa đoạn code upload file ở phía trên không hề bị check admin nên có thể upload hoàn toàn bình thường.
<p align="center">
  <img src="https://i.imgur.com/Z4iN82A.png">
</p>
File sau khi upload lên content của file hoàn toàn giữ nguyên còn file name sẽ bị rename thành đuôi jpg, vậy thì không thể up shell php ở đây được. Mình nghĩ chắc nó sẽ cần dùng đến sau nên tạm bỏ lại đấy.

Cuối cùng là function **fetchImagePage:**
<p align="center">
  <img src="https://i.imgur.com/NdCYOiy.png">
</p>
Ở đây thì cũng chả có gì đặc sắc, chỉ có chỗ lưu ý là nó sẽ load tất cả src của thẻ img có trong url input vào và dùng function **@getimagesize** để check xem có phải ảnh hay không, nếu là ảnh thì in ra.<br/>
Sau một hồi đọc code mỏi hết mắt hình mình nhận ra là flag không hề xuất hiện trong 1 file php nào cả. Nhiều khả năng là file flag là 1 file txt hay gì đó, muốn biết tên file thì chắc là phải RCE.<br/>
Tiếp tục thì mình đọc file **controller_audio.php.**
<p align="center">
  <img src="https://i.imgur.com/lTYM6p8.png">
</p>
Ở đây có function **_destruct** nhìn có vẻ nguy hiểm, mình nghĩ ngay đến Object injection. Lại tiếp tục đọc code tiếp thì thấy có 2 file **application/image.php** và **application/audio.php** đều có function **save.** Và function **save** của **image.php** có khả năng có thể write shell được
<p align="center">
  <img src="https://i.imgur.com/4DKDg2D.png">
</p>
Vậy là mình bắt đầu có ý tưởng là phải control được biến **$file** và biến **$data** của object **image,** sau đấy lại control biến **$default_audio** của **controller_audio** để gọi đến function **save** của **image.**<br/>
Lúc này mình nghĩ ngay đến **phar unserialize** vì ở đây đã có chức năng upload rồi, lại còn là object injection thì nhiều khả năng là phar.<br/>
Sau một hồi search về phar thì mình tìm được 1 bài như sau: https://srcincite.io/blog/2018/10/02/old-school-pwning-with-new-school-tricks-vanilla-forums-remote-code-execution.html<br/>
Vector tấn công khá giống với bài mình đang làm, thế là mình chỉnh sửa code đôi chút để inject vào object **image** và **controller_audio,** cụ thể như sau:
<p align="center">
  <img src="https://i.imgur.com/tSRt8N7.png">
</p>
Ở đây chú ý đến biến **$file** và **$data** của object **image** mình hoàn toàn control được, sau đấy thì mình lại tiếp tục inject biến **$default_audio** của object **controller_audio** bằng chính object **image** mà mình tạo ở trên. Vậy là xong bước tạo phar, upload lên website. Giờ sẽ cần tìm đến một function nào đấy có thể gọi đến wrapper phar để unserialize object. Như trong bài viết mình đề cập trên thì người ta lợi dùng **@getimagesize** để gọi đến phar unserialize. Nhìn lại function **fetchImagePage** thì có function **@getimagesize** thật.<br/>
Vậy là vector tấn công của mình sẽ như sau: Tạo file phar với object đã bị inject -> Upload file phar vừa tạo lên website qua chức năng upload -> Tạo 1 file html có tag img với src là payload wrapper phar -> Dùng fetch để get image trên trang html vừa tạo, từ đấy src sẽ được truyền vào **@getimagesize** và unserialize object.<br/>
Boom, đúng là mình đã write shell được, nhưng nhìn vào phpinfo thì các function để chạy lệnh hệ thống đều đã bị disable.
<p align="center">
  <img src="https://i.imgur.com/tSRt8N7.png">
</p>

Phải tìm các khác để list file trong folder. Search google thì tìm ra function **scandir** có thể list file được.<br/>
Thế là mình list hết các file trong folder "/var/www/html/" và có kết quả như sau:
<p align="center">
  <img src="https://i.imgur.com/O51PAeA.png">
</p>

Tà đà, cuối cùng cũng ra được tên file flag rồi, **286473nfdfy72634734_flagggflag,** giờ chỉ việc vào file này và lấy flag thôi
<p align="center">
  <img src="https://i.imgur.com/r1ddOLa.png">
</p>

Tổng kết lại bài này khá là hay, kết hợp giữa SQLi và phar unserialize.<br/>
Cảm ơn AceBear đã mang đến cho bọn mình một cuộc chơi khá là bổ ích, mong các bạn sẽ tổ chức thêm những giải chất lượng như thế này nữa.