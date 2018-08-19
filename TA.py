import RPi.GPIO as GPIO
import SimpleMFRC522
import urllib
import urllib2
from re import sub
import os
import time

reader = SimpleMFRC522.SimpleMFRC522()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
LED_BIRU = 18
LED_KUNING = 23
GPIO.setup(LED_BIRU,GPIO.OUT)
GPIO.setup(LED_KUNING,GPIO.OUT)

try:
        #Mengambil ID RFID tag
        print("Letakkan RFID tag!")
        id, text = reader.read()
        print(id)
        
        #~~~Melakukan pencarian data pada server~~~
        url ="https://pintarkotakpos.000webhostapp.com/getRFID.php"
        values = {'in_rfid' : id} 
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        #print the_page
        
        #~~~Menyimpan dan melakukan regex pada file datadb.py~~~
        f=open ("datadb.py","w")
        f.write(str(the_page))
        f.close()
        f=open ("datadb.py","r")
        lines = f.read()
        a = lines.replace('{"result":[{"nama_pengirim":', 'pengirim =')
        b = a.replace(',"nomor_pengirim":', '\nnomorpengirim=')
        c = b.replace(',"nomor_penerima":','\nnomorpenerima=')
        d = c.replace('}]}', '')
        e = d.replace(' ', '')
        f=open ("datadb.py","w")
        f.write(str(e))
        #print e
        f.close()

        from datadb import *   
        norumah = '081354543012' #paten
        penerima = 'Zulfahmi_Haeril' #paten 
        kode = '/home/pi/tg/bin/telegram-cli -k server.pub -WR -e '
        msg = '"msg '              
        if (norumah == nomorpenerima):
            GPIO.output(LED_BIRU, GPIO.HIGH)
            time.sleep(2)
            #~~~Mengirim notifikasi ke penerima~~~
            msgtopenerima = ' Paket yang anda pesan telah tiba!"'
            sendtopenerima = kode + msg + penerima + msgtopenerima
            os.system(sendtopenerima)
        		  		
            #~~~Menyimpan Kontak~~~
            add = '"add_contact '
            spasi = " "
            lastname1 = 'User"' 
            add_contact = kode + add + nomorpengirim + spasi + pengirim + spasi + lastname1
            os.system(add_contact)
            #os.system('/home/pi/tg/bin/telegram-cli -k server.pub -WR -e  "contact_list"')
            #~~~Mengirim notifikasi ke pengirim~~~        		
            lastname2 = 'User'
            underline = "_"
            msgtopengirim = ' Paket yang anda kirim telah sampai di tujuan!"' 
            sendtopengirim = kode + msg + pengirim + underline + lastname2 + msgtopengirim    
            os.system(sendtopengirim)
            GPIO.output(LED_BIRU, GPIO.LOW)
        else:
            #~~~Mengirim notifikasi ke penerima~~~
            GPIO.output(LED_KUNING, GPIO.HIGH)
            time.sleep(2)
            msgtopenerima = ' Anda menerima paket bukan milik anda!"'
            sendtopenerima = kode + msg + penerima + msgtopenerima
            os.system(sendtopenerima)
            GPIO.output(LED_KUNING, GPIO.LOW)
            
finally:
        GPIO.cleanup()